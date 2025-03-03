import os
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from utils import (
    generate_dob,
    generate_gender,
    generate_height,
    generate_place_of_birth,
    generate_address_1,
    generate_address_2,
    generate_id_number,
    generate_issue_and_expiry_dates,
    generate_khmer_name,
    generate_english_name,
    generate_mrz_1,
    generate_mrz_2,
    generate_mrz_3,
    get_random_image_path,
)
from pykhmernlp.number import to_khmer_num

blur_probability = 0.8


def load_font(path, size):
    return (
        ImageFont.truetype(path, size)
        if os.path.exists(path)
        else ImageFont.load_default()
    )


def draw_bbox(draw, x, y, text, font, label, fixed_height=None):
    default_height = font.getmetrics()[0] + font.getmetrics()[1]
    text_height = fixed_height if fixed_height is not None else default_height
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    pad_x, pad_y = 4, 4
    x2 = x + text_width + 2 * pad_x
    y2 = y + text_height + 2 * pad_y
    if DRAW_LABEL:
        label_font = load_font(font_bokor_path, label_font_size)
        draw.text((x, y - 20), label, font=label_font, fill="blue")
    if DRAW_BBOX:
        draw.rectangle([x, y, x2, y2], outline="red")
    v_offset = (text_height - default_height) // 2
    draw.text((x + pad_x, y + pad_y + v_offset), text, font=font, fill="black")
    return x2, y2


def draw_bbox_mrz(draw, x, y, text, font, label):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pad_x, pad_y = 10, 10
    x2 = x + text_width + 2 * pad_x
    y2 = y + text_height + 2 * pad_y
    if DRAW_LABEL:
        label_font = load_font(font_ocrb_path, label_font_size)
        draw.text((x, y - 20), label, font=label_font, fill="blue")
    if DRAW_BBOX:
        draw.rectangle([x, y, x2, y2 + 15], outline="red")
    draw.text(
        (x + pad_x, y + (y2 - y - text_height) // 2), text, font=font, fill="black"
    )
    return x2, y2


bbox_data = {"id_card": []}


def add_bbox_data(bbox_id, x1, y1, x2, y2, text):
    bbox_data["id_card"].append(
        {bbox_id: {"bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, "text": text}}
    )


font_bokor_path = "fonts/bokor.ttf"
font_content_bold_path = "fonts/content_bold.ttf"
font_dejavu_path = "fonts/DejaVuSansMono.ttf"
font_khmeros_path = "fonts/Khmer OS Content.ttf"
font_khmer_moul_path = "fonts/khmer_moul.ttf"
font_khmer_moul_light_path = "fonts/khmer_moulight.ttf"
font_ocrb_path = "fonts/ocr_b.ttf"
font_size = 12
label_font_size = 12
DRAW_BBOX = 0
DRAW_LABEL = 0


def draw_photo(image, draw):
    photo_path = get_random_image_path("./photos")
    if photo_path:
        try:
            photo = Image.open(photo_path).resize((320, 500)).convert("RGB")
            x, y = 55, 80
            image.paste(photo, (x, y))
            if DRAW_LABEL:
                label_font = load_font(font_bokor_path, label_font_size)
                draw.text((x, y - 20), "Photo", font=label_font, fill="blue")
            if DRAW_BBOX:
                draw.rectangle([x, y, x + 320, y + 500], outline="red")
            add_bbox_data("photo", x, y, x + 320, y + 500, "Photo")
        except Exception as e:
            print(f"Error loading photo: {e}")


def draw_signature(image, draw):
    signature_path = get_random_image_path("./signatures")
    if signature_path:
        try:
            signature = Image.open(signature_path).resize((200, 50))
            x, y = 115, 600 if signature.mode == "RGBA" else 580
            if signature.mode == "RGBA":
                image.paste(signature.convert("RGBA"), (x, y), signature.split()[3])
            else:
                image.paste(signature.convert("RGB"), (x, y))
            if DRAW_LABEL:
                label_font = load_font(font_bokor_path, label_font_size)
                draw.text((x, y - 20), "Signature", font=label_font, fill="blue")
            if DRAW_BBOX:
                draw.rectangle([x, y, x + 200, y + 50], outline="red")
            add_bbox_data("signature", x, y, x + 200, y + 50, "Signature")
        except Exception as e:
            print(f"Error loading signature: {e}")


def draw_segments():
    draw_photo(image, draw)
    draw_signature(image, draw)
    font_id = load_font(font_ocrb_path, 50)
    x, y = 1100, 20
    x2, y2 = draw_bbox(draw, x, y, text_id_num, font_id, "ID Number")
    add_bbox_data("id_number", x, y, x2, y2, text_id_num)

    font_pre = load_font(font_bokor_path, 34)
    font_content = load_font(font_khmer_moul_light_path, 34)
    fixed = font_content.getmetrics()[0] + font_content.getmetrics()[1]
    x, y = 400, 110
    x_pre, y_pre = draw_bbox(
        draw, x, y, "គោត្តនាមនិងនាម:", font_pre, "Pre Kh Name", fixed
    )
    add_bbox_data("pre_khm_name", x, y, x_pre, y_pre, "គោត្តនាមនិងនាម:")
    fname, lname = khmer_name.split(" ", 1)

    x_fname = x_pre + 10
    x_fname_end, y_fname_end = draw_bbox(
        draw, x_fname, y, fname, font_content, "Kh fn", fixed
    )
    add_bbox_data("khm_fname", x_fname, y, x_fname_end, y_fname_end, fname)

    x_lname = x_fname_end + 1
    x_lname_end, y_lname_end = draw_bbox(
        draw, x_lname, y, lname, font_content, "Kh ln", fixed
    )
    add_bbox_data("khm_lname", x_lname, y, x_lname_end, y_lname_end, lname)

    font_eng = load_font(font_ocrb_path, 40)
    eng_fname, eng_lname = english_name.split(" ", 1)
    x, y = 600, 190
    x_eng, y_eng = draw_bbox_mrz(draw, x, y, eng_fname, font_eng, "Eng fn")
    add_bbox_data("eng_fname", x, y, x_eng, y_eng, eng_fname)

    x_eng_lname = x_eng + 10
    x_eng_lname_end, y_eng_lname_end = draw_bbox_mrz(
        draw, x_eng_lname, y, eng_lname, font_eng, "Eng ln"
    )
    add_bbox_data(
        "eng_lname", x_eng_lname, y, x_eng_lname_end, y_eng_lname_end, eng_lname
    )

    font_pre = load_font(font_bokor_path, 34)
    font_content = load_font(font_khmeros_path, 34)
    fixed = font_content.getmetrics()[0] + font_content.getmetrics()[1]
    y = 260
    x = 400
    x_pre_dob, y_pre_dob = draw_bbox(
        draw, x, y, "ថ្ងៃខែឆ្នាំកំណើត:", font_pre, "Pre DOB", fixed
    )
    add_bbox_data("pre_dob", x, y, x_pre_dob, y_pre_dob, "ថ្ងៃខែឆ្នាំកំណើត:")
    x_dob = x_pre_dob + 10
    x_dob_end, y_dob_end = draw_bbox(draw, x_dob, y, dob, font_content, "DOB", fixed)
    add_bbox_data("dob", x, y, x_dob_end, y_dob_end, dob)
    x_pre_gender = x_dob_end + 10
    x_pre_gender_end, y_pre_gender_end = draw_bbox(
        draw, x_pre_gender, y, "ភេទ:", font_pre, "Pre gender", fixed
    )
    add_bbox_data(
        "pre_gender", x_pre_gender, y, x_pre_gender_end, y_pre_gender_end, "ភេទ:"
    )
    x_gender = x_pre_gender_end + 10
    x_gender_end, y_gender_end = draw_bbox(
        draw, x_gender, y, gender, font_content, "Gender", fixed
    )
    add_bbox_data("gender", x_gender, y, x_gender_end, y_gender_end, gender)
    x_pre_height = x_gender_end + 10
    x_pre_height_end, y_pre_height_end = draw_bbox(
        draw, x_pre_height, y, "កំពស់:", font_pre, "Pre height", fixed
    )
    add_bbox_data(
        "pre_height", x_pre_height, y, x_pre_height_end, y_pre_height_end, "កំពស់:"
    )
    x_height = x_pre_height_end + 10
    x_height_end, y_height_end = draw_bbox(
        draw, x_height, y, height_val, font_content, "Height", fixed
    )
    add_bbox_data("height", x_height, y, x_height_end, y_height_end, height_val)

    x, y = 400, 340
    x_pre_pob, y_pre_pob = draw_bbox(
        draw, x, y, "ទីកន្លែងកំណើត:", font_pre, "Pre POB", fixed
    )
    add_bbox_data("pre_pob", x, y, x_pre_pob, y_pre_pob, "ទីកន្លែងកំណើត:")
    x_pob = x_pre_pob + 10
    x_pob_end, y_pob_end = draw_bbox(draw, x_pob, y, pob, font_content, "POB", fixed)
    add_bbox_data("pob", x_pob, y, x_pob_end, y_pob_end, pob)

    x, y = 400, 410
    x_pre_address, y_pre_address = draw_bbox(
        draw, x, y, "អាសយដ្ឋាន:", font_pre, "Pre address", fixed
    )
    add_bbox_data("pre_address", x, y, x_pre_address, y_pre_address, "អាសយដ្ឋាន:")
    x_address1 = x_pre_address + 10
    x_address1_end, y_address1_end = draw_bbox(
        draw, x_address1, y, address1, font_content, "Address1", fixed
    )
    add_bbox_data("address1", x_address1, y, x_address1_end, y_address1_end, address1)

    x, y = 400, 480
    x_address2_end, y_address2_end = draw_bbox(
        draw, x, y, address2, font_content, "Address2", fixed
    )
    add_bbox_data("address2", x, y, x_address2_end, y_address2_end, address2)

    font_pre_exp = load_font(font_bokor_path, 34)
    font_content_exp = load_font(font_khmeros_path, 34)
    fixed = font_content_exp.getmetrics()[0] + font_content_exp.getmetrics()[1]
    x, y = 400, 550
    x_pre_exp, y_pre_exp = draw_bbox(
        draw, x, y, "សុពលភាព:", font_pre_exp, "Pre Iss Exp Date", fixed
    )
    add_bbox_data("pre_issue_expiry_date", x, y, x_pre_exp, y_pre_exp, "សុពលភាព:")
    x_exp = x_pre_exp + 10
    exp_text = f"{to_khmer_num(issue_date)} ដល់ថ្ងៃ {to_khmer_num(expiry_date)}"
    x_exp_end, y_exp_end = draw_bbox(
        draw, x_exp, y, exp_text, font_content_exp, "expire-date", fixed
    )
    add_bbox_data("expire_date", x_exp, y, x_exp_end, y_exp_end, exp_text)

    x, y = 400, 620
    x_pre_identity, y_pre_identity = draw_bbox(
        draw, x, y, "ភិនភាគ:", font_pre, "Pre identity", fixed
    )
    add_bbox_data("pre_identity", x, y, x_pre_identity, y_pre_identity, "ភិនភាគ:")
    x_identity = x_pre_identity + 10
    x_identity_end, y_identity_end = draw_bbox(
        draw, x_identity, y, identity, font_content, "Identity", fixed
    )
    add_bbox_data("identity", x_identity, y, x_identity_end, y_identity_end, identity)

    font_mrz = load_font(font_ocrb_path, 75)
    x, y = 50, 700
    x_mrz1, y_mrz1 = draw_bbox_mrz(draw, x, y, mrz1, font_mrz, "MRZ1")
    add_bbox_data("mrz1", x, y, x_mrz1, y_mrz1, mrz1)
    x, y = 50, 800
    x_mrz2, y_mrz2 = draw_bbox_mrz(draw, x, y, mrz2, font_mrz, "MRZ2")
    add_bbox_data("mrz2", x, y, x_mrz2, y_mrz2, mrz2)
    x, y = 50, 900
    x_mrz3, y_mrz3 = draw_bbox_mrz(draw, x, y, mrz3, font_mrz, "MRZ3")
    add_bbox_data("mrz3", x, y, x_mrz3, y_mrz3, mrz3)


def generate_txt_output(bbox_data, classes_file, output_file):
    with open(classes_file, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    class_to_index = {cls: idx for idx, cls in enumerate(classes)}
    output_lines = []
    for item in bbox_data["id_card"]:
        for bbox_id, data in item.items():
            class_name = bbox_id
            if class_name in class_to_index:
                class_idx = class_to_index[class_name]
                bbox = data["bbox"]
                x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
                if x2 <= x1 or y2 <= y1:
                    print(f"Warning: Invalid bbox for {class_name}")
                    continue
                line = f"{class_idx} {x1} {y1} {x2} {y2}"
                output_lines.append(line)
            else:
                print(f"Warning: {class_name} not found in classes.txt")
    output_lines.sort(key=lambda x: int(x.split()[0]))
    with open(output_file, "w") as f:
        f.write("\n".join(output_lines))


def generate_id_image(
    image_file, label_txt_file, label_json_file, classes_file, image_size
):
    global image, draw, text_id_num, khmer_name, english_name, dob, gender, height_val, pob, address1, address2, issue_date, expiry_date, identity, mrz1, mrz2, mrz3, bbox_data
    bbox_data = {"id_card": []}
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    text_id_num = generate_id_number()
    khmer_name = generate_khmer_name()
    english_name = generate_english_name()
    dob = generate_dob()
    gender = generate_gender()
    height_val = generate_height()
    pob = generate_place_of_birth()
    address1 = generate_address_1()
    address2 = generate_address_2()
    issue_date, expiry_date = generate_issue_and_expiry_dates()
    identity = "ប្រជ្រុយចុងភ្នែកស្តាំ"
    mrz1 = generate_mrz_1()
    mrz2 = generate_mrz_2()
    mrz3 = generate_mrz_3()
    draw_segments()
    if random.random() < blur_probability:
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
    image.save(image_file)
    with open(label_json_file, "w", encoding="utf-8") as f:
        json.dump(bbox_data, f, ensure_ascii=False, indent=4)
    generate_txt_output(bbox_data, classes_file, label_txt_file)


def synthetic_khmerid(
    size=100,
    image_size=(1575, 1024),
    profile_path="images",
    label_type="None",
    save_json=True,
    output_path="synth_khmerid",
):
    global DRAW_LABEL
    DRAW_LABEL = 0 if label_type != "None" else 0
    os.makedirs(os.path.join(output_path, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "labels"), exist_ok=True)
    classes = [
        "photo",
        "signature",
        "id_number",
        "pre_khm_name",
        "khm_fname",
        "khm_lname",
        "eng_fname",
        "eng_lname",
        "pre_dob",
        "dob",
        "pre_gender",
        "gender",
        "pre_height",
        "height",
        "pre_pob",
        "pob",
        "pre_address",
        "address1",
        "address2",
        "pre_issue_expiry_date",
        "expire_date",
        "pre_identity",
        "identity",
        "mrz1",
        "mrz2",
        "mrz3",
    ]
    classes_file = os.path.join(output_path, "classes.txt")
    with open(classes_file, "w") as f:
        for cls in classes:
            f.write(cls + "\n")
    for i in range(size):
        img_file = os.path.join(output_path, "images", f"{i:03d}.png")
        label_txt = os.path.join(output_path, "labels", f"{i:03d}.txt")
        label_json = os.path.join(output_path, "labels", f"{i:03d}.json")
        generate_id_image(img_file, label_txt, label_json, classes_file, image_size)


if __name__ == "__main__":
    synthetic_khmerid(
        size=100,
        image_size=(1575, 1024),
        profile_path="images",
        label_type="segment-level",
        save_json=True,
        output_path="synth_khmerid",
    )
