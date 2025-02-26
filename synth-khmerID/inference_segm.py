#!/usr/bin/env python3
"""
Updated inference code for Mask R-CNN, drawing ground-truth and predicted masks/boxes
on the same image, using a single color string so we avoid errors about color list length.

1) Loads a checkpoint (possibly partially if mismatch).
2) Feeds a test image through the model.
3) Draws GT in green, predictions in red.
4) Saves the final result.
"""

import random
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

import torchvision
import torchvision.transforms.v2 as transforms
from torchvision.utils import draw_segmentation_masks, draw_bounding_boxes
from torchvision.tv_tensors import BoundingBoxes, Mask
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor


##################################################
# 1) HELPER FUNCTIONS
##################################################
def resize_img(pil_img, target_sz=512, divisor=1):
    """
    Resize a PIL Image so that its smaller side is `target_sz`.
    Keeps aspect ratio. 'divisor' is unused except as placeholder.
    """
    w, h = pil_img.size
    min_side = min(w, h)
    scale = target_sz / float(min_side)
    new_w, new_h = int(w * scale), int(h * scale)
    return pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

def draw_bboxes(image, boxes, labels=None, colors=None, width=2):
    """
    Custom bounding box drawer using torchvision's draw_bounding_boxes.
    image: (C,H,W) Tensor
    boxes: Nx4 in xyxy
    labels: list of strings
    colors: single string (e.g. "red") or list of length >= Nx4
    width: bounding box line width
    """
    if hasattr(boxes, "data"):
        boxes_tensor = boxes.data
    else:
        boxes_tensor = boxes

    annotated = draw_bounding_boxes(
        image=image,
        boxes=boxes_tensor,
        labels=labels,
        colors=colors,
        width=width
    )
    return annotated

def create_polygon_mask(image_size, vertices):
    """
    Create a single-channel (L-mode) mask with a polygon in white(255) on black(0).
    image_size: (width, height)
    vertices: list of (x,y)
    """
    mask_img = Image.new('L', image_size, 0)
    draw = ImageDraw.Draw(mask_img, 'L')
    draw.polygon(vertices, fill=255)
    return mask_img

def move_data_to_device(data, device):
    """
    Recursively move data to 'device'.
    """
    if isinstance(data, dict):
        return {k: move_data_to_device(v, device) for k, v in data.items()}
    elif isinstance(data, list):
        return [move_data_to_device(el, device) for el in data]
    elif isinstance(data, tuple):
        return tuple(move_data_to_device(el, device) for el in data)
    elif isinstance(data, torch.Tensor):
        return data.to(device)
    else:
        return data

##################################################
# 2) MODEL CREATION & PARTIAL LOAD
##################################################
def create_maskrcnn(num_classes):
    """
    Create a Mask R-CNN model with ResNet50 FPN.
    'num_classes' includes background class as index 0.
    """
    model = maskrcnn_resnet50_fpn_v2(weights="DEFAULT")

    # Replace classification head
    in_features_box = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features_box, num_classes)

    # Replace mask head
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    dim_reduced = model.roi_heads.mask_predictor.conv5_mask.out_channels
    model.roi_heads.mask_predictor = MaskRCNNPredictor(
        in_features_mask, dim_reduced, num_classes
    )
    return model

def load_checkpoint_partial(checkpoint_path, model, device):
    """
    Load a checkpoint, skipping layers that mismatch shape.
    Useful if the old checkpoint had fewer classes.
    """
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model_dict = model.state_dict()

    filtered_dict = {}
    mismatch_keys = []
    for k, v in checkpoint.items():
        if k in model_dict:
            if model_dict[k].shape == v.shape:
                filtered_dict[k] = v
            else:
                mismatch_keys.append(k)
        else:
            mismatch_keys.append(k)

    model_dict.update(filtered_dict)
    model.load_state_dict(model_dict)
    print("Partial load completed.")
    if mismatch_keys:
        print("Skipped keys (shape mismatch or missing):", mismatch_keys)
    return model

##################################################
# 3) ENVIRONMENT / CLASSES
##################################################
# Example class names (1 background + your real ones):
class_names = [
    'background', 'address1', 'address2', 'dob', 'eng-fname', 'eng-lname',
    'expire-date', 'gender', 'height', 'id_number', 'identity', 'khm-fname',
    'khm-lname', 'mrz1', 'mrz2', 'mrz3', 'photo', 'pob', 'pre-address',
    'pre-dob', 'pre-expire-date', 'pre-gender', 'pre-height', 'pre-identity',
    'pre-khm-name', 'pre-pob', 'signature'
]
num_classes = len(class_names)

# Color for GT is green, predictions is red
gt_color   = "green"
pred_color = "red"  # single string color, so no error about multiple instances

# Demo environment
val_keys = ["img_000"]
img_dict = { "img_000": "output_image_segment.png" }

# A dummy annotation for GT
annotation_data = {
    "img_000": {
        "shapes": [
            {
                "label": "student_id",
                "points": [(50, 50), (200, 50), (200, 100), (50, 100)]
            }
        ]
    }
}
annotation_df = pd.DataFrame.from_dict(annotation_data, orient="index")


##################################################
# 4) MAIN SCRIPT
##################################################
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint_path = "../weights/sample.pth"

    # 4.1 Create & partial load model
    model = create_maskrcnn(num_classes=num_classes).to(device)
    model = load_checkpoint_partial(checkpoint_path, model, device)
    model.eval()

    if not val_keys:
        print("No validation keys found.")
    else:
        file_id = random.choice(val_keys)
        img_path = img_dict[file_id]
        print(f"Using test image: {img_path}")

        test_img = Image.open(img_path).convert("RGB")
        w0, h0 = test_img.size
        # Resize
        train_sz = 512
        input_img = resize_img(test_img, target_sz=train_sz)
        # scale factor to bring predictions back to original size
        scale_factor = min(w0,h0) / float(min(input_img.size))

        # Build dummy GT mask
        shapes = annotation_df.loc[file_id]["shapes"]
        mask_list = []
        for shp in shapes:
            mask_img = create_polygon_mask((w0,h0), shp["points"])
            m_t = transforms.PILToTensor()(mask_img)[0].bool()
            mask_list.append(m_t)
        if len(mask_list)>0:
            gt_masks_2d = torch.stack(mask_list,dim=0)
        else:
            gt_masks_2d = torch.zeros((0,h0,w0), dtype=torch.bool)
        gt_masks = Mask(gt_masks_2d)
        gt_labels = [s["label"] for s in shapes]

        # bounding boxes from GT
        gt_bboxes = BoundingBoxes(
            data=torchvision.ops.masks_to_boxes(gt_masks),
            format="xyxy",
            canvas_size=(h0,w0)
        )

        # Model input
        to_model_tf = transforms.Compose([
            transforms.ToImage(),
            transforms.ToDtype(torch.float32, scale=True)
        ])
        input_tensor = to_model_tf(input_img)[None].to(device)
        print("Input tensor shape:", input_tensor.shape)

        # 5) Inference
        with torch.no_grad():
            outputs = model(input_tensor)

        outputs = move_data_to_device(outputs, 'cpu')
        pred = outputs[0]
        print("Output keys:", list(pred.keys()))

        # Filter by confidence
        scores = pred.get("scores", torch.tensor([]))
        boxes  = pred.get("boxes", torch.tensor([]))
        labels = pred.get("labels", torch.tensor([]))

        keep = scores>0.5
        boxes  = boxes[keep] * scale_factor
        scores = scores[keep]
        labels = labels[keep]

        # If 'masks' not present => skip segmentation masks
        if "masks" in pred:
            masks_4d = pred["masks"][keep]
            # scale up
            masks_up = F.interpolate(masks_4d, size=(h0, w0), mode="bilinear", align_corners=False)
            mask_list2 = []
            for pm in masks_up:
                bin_mask = pm[0]>=0.5
                mask_list2.append(bin_mask.bool())
            if len(mask_list2)>0:
                pred_masks_2d = torch.stack(mask_list2, dim=0)
            else:
                pred_masks_2d = torch.zeros((0,h0,w0),dtype=torch.bool)
            pred_masks = Mask(pred_masks_2d)
        else:
            print("No 'masks' in output => skipping segmentation masks.")
            pred_masks = None

        # bounding boxes
        pred_bboxes = BoundingBoxes(
            data=boxes,
            format="xyxy",
            canvas_size=(h0,w0)
        )
        pred_labels = []
        for lbl_id in labels:
            idx = int(lbl_id.item())
            name = class_names[idx] if idx<len(class_names) else f"class_{idx}"
            pred_labels.append(name)

        label_strs = [f"{nm}\n{sc.item()*100:.2f}%" for nm,sc in zip(pred_labels, scores)]

        # 7) Draw GT + Pred
        img_tensor = transforms.PILToTensor()(test_img).clone()

        # (a) Draw GT in green
        annotated_img = draw_segmentation_masks(
            image=img_tensor,
            masks=gt_masks,
            alpha=0.3,
            colors=gt_color  # a single string "green"
        )
        annotated_img = draw_bboxes(
            image=annotated_img,
            boxes=gt_bboxes,
            labels=gt_labels,
            colors=gt_color
        )

        # (b) Draw Pred in red
        if pred_masks is not None and pred_masks.shape[0]>0:
            annotated_img = draw_segmentation_masks(
                image=annotated_img,
                masks=pred_masks,
                alpha=0.3,
                colors="green"  # single string "red"
            )
        annotated_img = draw_bboxes(
            image=annotated_img,
            boxes=pred_bboxes,
            labels=label_strs,
            colors=pred_color
        )

        # 8) Save final
        from torchvision.transforms.functional import to_pil_image
        final_pil = to_pil_image(annotated_img)
        save_path = "inference_result.jpg"
        final_pil.save(save_path)
        print(f"Saved annotated image to {save_path}")

        # 9) Print
        print("\n=== GROUND TRUTH ===")
        for l,bx in zip(gt_labels, gt_bboxes.numpy()):
            print(f"{l} => {bx}")

        print("\n=== PREDICTIONS ===")
        for nm,bx,sc in zip(pred_labels, pred_bboxes.numpy(), scores):
            print(f"{nm} => {bx}, {sc.item()*100:.2f}%")
