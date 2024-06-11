import cv2
import numpy as np
from typing import Optional, Tuple


def resize_h_128(roi: np.ndarray, save: bool = False, save_path: Optional[str] = None) -> Optional[np.ndarray]:
    if not isinstance(roi, np.ndarray):
        print("Error: The input must be a numpy ndarray.")
        return None

    if roi.ndim != 3 or roi.shape[2] not in {1, 3, 4}:
        print("Error: The input image must have 3 dimensions (H, W, C) with 1, 3, or 4 channels.")
        return None

    h, w, c = roi.shape
    if h == 0 or w == 0:
        print("Error: The input image dimensions must be greater than zero.")
        return None

    x = int((128 * w) / h)
    try:
        out = cv2.resize(roi, (x, 128), interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(f"Error during resizing: {e}")
        return None

    if save:
        if save_path is None:
            save_path = "resized_image.jpg"
        try:
            cv2.imwrite(save_path, out)
        except Exception as e:
            print(f"Error saving the resized image: {e}")
            return None

    return out



def resize_image(image_path: str, height: Optional[int] = None, width: Optional[int] = None,
                 save: bool = False, save_path: Optional[str] = None) -> Optional[np.ndarray]:

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image.")
        return None

    orig_height, orig_width = image.shape[:2]

    # Set default height and width if not provided
    if height is None:
        height = orig_height
    if width is None:
        width = orig_width

    # Resize the image based on the provided dimensions
    try:
        if height != orig_height and width == orig_width:
            aspect_ratio = orig_width / orig_height
            width = int(height * aspect_ratio)
        elif width != orig_width and height == orig_height:
            aspect_ratio = orig_height / orig_width
            height = int(width * aspect_ratio)

        resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(f"Error during resizing: {e}")
        return None

    # Save the image if required
    if save:
        if save_path is None:
            save_path = f"{image_path.rsplit('.', 1)[0]}_resized.{image_path.rsplit('.', 1)[1]}"
        cv2.imwrite(save_path, resized_image)

    return resized_image


def to_grayscale(image_path: str, save: bool = False, save_path: Optional[str] = None) -> Optional[np.ndarray]:
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to read the image from the specified path.")
        return None
    
    # Convert the image to grayscale
    try:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        print(f"Error during conversion to grayscale: {e}")
        return None

    # Save the image if required
    if save:
        if save_path is None:
            save_path = "gray_image." + image_path.split('.')[-1]
        try:
            cv2.imwrite(save_path, gray_image)
        except Exception as e:
            print(f"Error saving the grayscale image: {e}")
            return None

    return gray_image

