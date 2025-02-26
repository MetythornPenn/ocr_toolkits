import os
import json
from PIL import Image, ImageDraw, ImageFont
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

def load_font(path, size):
    return ImageFont.truetype(path, size) if os.path.exists(path) else ImageFont.load_default()

# Define the font paths and sizes
font_bokor_path = "fonts/ocr_b.ttf"
font_content_bold_path = "fonts/content_bold.ttf"
font_dejavu_path = "fonts/DejaVuSansMono.ttf"
font_khmeros_path = "fonts/Khmer OS Content.ttf"
font_khmer_moul_path = "fonts/khmer_moul.ttf"
font_ocrb_path = "fonts/ocr_b.ttf"

font_size = 12
label_font_size = 12  # Define the size for label text
font_bokor = ImageFont.truetype(font_bokor_path, font_size)
font_content_bold = ImageFont.truetype(font_content_bold_path, 55)
font_dejavu = ImageFont.truetype(font_dejavu_path, font_size)
font_khmeros = ImageFont.truetype(font_khmeros_path, font_size)
font_khmer_moul = ImageFont.truetype(font_khmer_moul_path, font_size)
font_ocrb = ImageFont.truetype(font_ocrb_path, font_size)

mrz_font = ImageFont.truetype(font_ocrb_path, 50)

width, height = 1575, 1024
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Flags to control drawing of bounding boxes and labels
DRAW_BBOX = 1  # Set to False to disable bounding boxes
DRAW_LABEL = 1  # Set to False to disable labels

photo_path = get_random_image_path("./photos")
if photo_path:
    photo = Image.open(photo_path).resize((320, 500))
    image.paste(photo, (55, 80))

signature_path = get_random_image_path("./signatures")
if signature_path:
    signature = Image.open(signature_path).resize((200, 50))
    # Place signature below the photo (aligned with photo's left edge at x=55, below y=580)
    image.paste(signature, (55, 600))

def draw_bbox(draw, x1, y1, text, font, label):
    ascent, descent = font.getmetrics()
    text_height = ascent + descent
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    pad_x, pad_y = 4, 4
    x2 = x1 + text_width + 2 * pad_x
    y2 = y1 + text_height + 2 * pad_y

    # Draw label if enabled
    if DRAW_LABEL:
        label_font = load_font(font_bokor_path, label_font_size)
        draw.text((x1, y1 - 20), label, font=label_font, fill="blue")

    # Draw bounding box if enabled
    if DRAW_BBOX:
        draw.rectangle([x1, y1, x2, y2], outline="red")
    
    # Always draw the text
    draw.text((x1 + pad_x, y1 + (y2 - y1 - text_height) // 2), text, font=font, fill="black")

    return x2, y2

def draw_bbox_mrz(draw, x1, y1, text, font, label):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pad_x, pad_y = 10, 10
    x2 = x1 + text_width + 2 * pad_x
    y2 = y1 + text_height + 2 * pad_y

    # Draw label if enabled
    if DRAW_LABEL:
        label_font = load_font(font_ocrb_path, label_font_size)
        draw.text((x1, y1 - 20), label, font=label_font, fill="blue")

    # Draw bounding box if enabled
    if DRAW_BBOX:
        draw.rectangle([x1, y1, x2, y2 + 15], outline="red")
    
    # Always draw the text
    draw.text((x1 + pad_x, y1 + (y2 - y1 - text_height) // 2), text, font=font, fill="black")

    return x2, y2

bbox_data = {"id_card": []}
def add_bbox_data(bbox_id, x1, y1, x2, y2, text):
    bbox_data["id_card"].append({bbox_id: {"bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}, "text": text}})

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

def draw_segments():
    font_id_num = load_font(font_bokor_path, 50)
    x1, y1 = 1100, 20
    x2, y2 = draw_bbox(draw, x1, y1, text_id_num, font_id_num, "ID Number")
    add_bbox_data("id_number", x1, y1, x2, y2, text_id_num)

    font_khmer_name = load_font(font_khmeros_path, 34)
    pre_khm = "គោត្តនាមនិងនាម:"
    khm_fname, khm_lname = khmer_name.split(" ", 1)
    x1, y1 = 400, 110
    x2, y2 = draw_bbox(draw, x1, y1, pre_khm, font_khmer_name, "Pre Kh Name")
    add_bbox_data("pre_khm_name", x1, y1, x2, y2, pre_khm)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, khm_fname, font_khmer_name, "Kh fn")
    add_bbox_data("khm_fname", x1, y1, x2, y2, khm_fname)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, khm_lname, font_khmer_name, "Kh ln")
    add_bbox_data("khm_lname", x1, y1, x2, y2, khm_lname)

    font_eng_name = load_font(font_ocrb_path, 40)
    eng_fname, eng_lname = english_name.split(" ", 1)
    x1, y1 = 600, 190
    x2, y2 = draw_bbox_mrz(draw, x1, y1, eng_fname, font_eng_name, "Eng fn")
    add_bbox_data("eng_fname", x1, y1, x2, y2, eng_fname)
    x1 = x2 + 10
    x2, y2 = draw_bbox_mrz(draw, x1, y1, eng_lname, font_eng_name, "Eng ln")
    add_bbox_data("eng_lname", x1, y1, x2, y2, eng_lname)

    font_dob = load_font(font_khmeros_path, 34)
    pre_dob = "ថ្ងៃខែឆ្នាំកំណើត:"
    x1, y1 = 400, 260
    x2, y2 = draw_bbox(draw, x1, y1, pre_dob, font_dob, "Pre DOB")
    add_bbox_data("pre_dob", x1, y1, x2, y2, pre_dob)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, dob, font_dob, "DOB")
    add_bbox_data("dob", x1, y1, x2, y2, dob)

    pre_gender = "ភេទ:"
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, pre_gender, font_dob, "Pre gender")
    add_bbox_data("pre_gender", x1, y1, x2, y2, pre_gender)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, gender, font_dob, "Gender")
    add_bbox_data("gender", x1, y1, x2, y2, gender)

    pre_height = "កំពស់:"
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, pre_height, font_dob, "Pre height")
    add_bbox_data("pre_height", x1, y1, x2, y2, pre_height)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, height_val, font_dob, "Height")
    add_bbox_data("height", x1, y1, x2, y2, height_val)

    pre_pob = "ទីកន្លែងកំណើត:"
    x1, y1 = 400, 340
    x2, y2 = draw_bbox(draw, x1, y1, pre_pob, font_dob, "Pre POB")
    add_bbox_data("pre_pob", x1, y1, x2, y2, pre_pob)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, pob, font_dob, "POB")
    add_bbox_data("pob", x1, y1, x2, y2, pob)

    pre_addr = "អាសយដ្ឋាន:"
    x1, y1 = 400, 410
    x2, y2 = draw_bbox(draw, x1, y1, pre_addr, font_dob, "Pre address")
    add_bbox_data("pre_address", x1, y1, x2, y2, pre_addr)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, address1, font_dob, "Address1")
    add_bbox_data("address1", x1, y1, x2, y2, address1)
    x1, y1 = 400, 480
    x2, y2 = draw_bbox(draw, x1, y1, address2, font_dob, "Address2")
    add_bbox_data("address2", x1, y1, x2, y2, address2)

    font_exp = load_font(font_khmeros_path, 34)
    pre_exp = "សុពលភាព:"
    exp_text = f"{to_khmer_num(issue_date)} ដល់ថ្ងៃ {to_khmer_num(expiry_date)}"
    x1, y1 = 400, 550
    x2, y2 = draw_bbox(draw, x1, y1, pre_exp, font_exp, "Pre Iss Exp Date")
    add_bbox_data("pre_issue_expiry_date", x1, y1, x2, y2, pre_exp)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, exp_text, font_exp, "Iss Exp Date")
    add_bbox_data("issue_expire_date", x1, y1, x2, y2, exp_text)

    pre_id = "ភិនភាគ:"
    x1, y1 = 400, 620
    x2, y2 = draw_bbox(draw, x1, y1, pre_id, font_dob, "Pre identity")
    add_bbox_data("pre_identity", x1, y1, x2, y2, pre_id)
    x1 = x2 + 10
    x2, y2 = draw_bbox(draw, x1, y1, identity, font_dob, "Identity")
    add_bbox_data("identity", x1, y1, x2, y2, identity)

    font_mrz = load_font(font_ocrb_path, 75)
    x1, y1 = 50, 700
    x2, y2 = draw_bbox_mrz(draw, x1, y1, mrz1, font_mrz, "MRZ1")
    add_bbox_data("mrz1", x1, y1, x2, y2, mrz1)
    x1, y1 = 50, 800
    x2, y2 = draw_bbox_mrz(draw, x1, y1, mrz2, font_mrz, "MRZ2")
    add_bbox_data("mrz2", x1, y1, x2, y2, mrz2)
    x1, y1 = 50, 900
    x2, y2 = draw_bbox_mrz(draw, x1, y1, mrz3, font_mrz, "MRZ3")
    add_bbox_data("mrz3", x1, y1, x2, y2, mrz3)

    add_bbox_data("photo", 55, 80, 375, 580, "Photo")
    add_bbox_data("signature", 55, 600, 255, 650, "Signature")  # Updated signature bbox

draw_segments()
image.save('output_image_segm.png')
with open('bboxes_segment.json', 'w', encoding='utf-8') as f:
    json.dump(bbox_data, f, ensure_ascii=False, indent=4)
print("Exported bboxes_segment.json")