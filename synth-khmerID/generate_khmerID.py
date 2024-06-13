import json
import random
from PIL import Image, ImageDraw, ImageFont

# Import your utilities (assuming these functions are defined in utils module)
from utils import (
    generate_commune_and_district,
    generate_dob,
    generate_gender,
    generate_height,
    generate_place_of_birth,
    generate_address_1,
    generate_address_2,
    generate_id_number,
    generate_issue_and_expiry_dates,
    download_image,
    generate_khmer_name,
    generate_english_name,
    generate_gender_eng,
    generate_9_digit_number,
    generate_mrz_1,
    generate_mrz_2,
    generate_mrz_3,
)

from pykhmernlp.number import to_khmer_num

# Define the font path and size
font_bokor_path = "fonts/ocr_b.ttf"
font_content_bold_path = "fonts/content_bold.ttf"
font_dejavu_path = "fonts/DejaVuSansMono.ttf"
font_khmeros_path = "fonts/Khmer OS Content.ttf"
font_khmer_moul_path = "fonts/khmer_moul.ttf"
font_ocrb_path = "fonts/ocr_b.ttf"

font_size = 12
font_bokor = ImageFont.truetype(font_bokor_path, font_size)
font_content_bold = ImageFont.truetype(font_content_bold_path, 55)
font_dejavu = ImageFont.truetype(font_dejavu_path, font_size)
font_khmeros = ImageFont.truetype(font_khmeros_path, font_size)
font_khmer_moul = ImageFont.truetype(font_khmer_moul_path, font_size)
font_ocrb = ImageFont.truetype(font_ocrb_path, font_size)

mrz_font = ImageFont.truetype(font_ocrb_path, 50)

# Create a blank white image
"""
Ratio : 1.5385
400 x 260 : original ID CARD
1575   x 1024 : scale with the same ratio
"""
width, height = 1575, 1024
image = Image.new('RGB', (width, height), 'white')

# Create a drawing context
draw = ImageDraw.Draw(image)



photo_path = "./photos/000002.png"
photo = Image.open(photo_path).resize((320, 500))
image.paste(photo, (55, 80))


# Function to draw a bounding box with text
def draw_bbox(draw, x1, y1, text, font):
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Add padding
    padding_x = 10
    padding_y = 10
    
    x2 = x1 + text_width + 2 * padding_x
    y2 = y1 + text_height + 2 * padding_y
    
    draw.rectangle([x1, y1, x2, y2 ], outline='red')
    
    # Center text vertically and add padding from the left
    text_x = x1 + padding_x
    text_y = y1 + (y2 - y1 - text_height) // 2
    
    draw.text((text_x, text_y), text, font=font, fill='black')
    
    return x2, y2

def draw_bbox_mrz(draw, x1, y1, text, font):
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Add padding
    padding_x = 10
    padding_y = 10
    
    x2 = x1 + text_width + 2 * padding_x
    y2 = y1 + text_height + 2 * padding_y
    
    draw.rectangle([x1, y1, x2, y2 + 15], outline='red')
    
    # Center text vertically and add padding from the left
    text_x = x1 + padding_x
    text_y = y1 + (y2 - y1 - text_height) // 2
    
    draw.text((text_x, text_y), text, font=font, fill='black')
    
    return x2, y2


# List to hold the bounding box data
bbox_data = {"id_card": []}

# Function to add bounding box data to JSON
def add_bbox_data(bbox_id, x1, y1, x2, y2, text):
    bbox_data["id_card"].append({
        f"{bbox_id}": {
            "bbox": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            },
            "text": text
        }
    })


# Draw 12 bounding boxes with independent functions

# Line 1 | ID Number 
font_id_num = ImageFont.truetype(font_ocrb_path, 50)
text_id_num = generate_id_number()
def id_num_bbox():
    x1, y1 = 1100, 20
    x2, y2 = draw_bbox_mrz(draw, x1, y1, text_id_num, font_id_num)
    add_bbox_data("id_num", x1, y1, x2, y2-10, text_id_num)

# Line 2 : Khmer Name 
font_khmer_name = ImageFont.truetype(font_khmeros_path, 34)
text_khmer_name = f"គោត្តនាមនិងនាម: {generate_khmer_name()[:random.randint(6, 11)]} {generate_khmer_name()[:random.randint(6, 16)]}"
def khm_name_bbox():
    x1, y1 = 400, 110
    x2, y2 = draw_bbox(draw, x1, y1, text_khmer_name, font_khmer_name)
    add_bbox_data("khm_name", x1, y1, x2, y2, text_khmer_name)

# Line 3 : English Name 
font_eng_name = ImageFont.truetype(font_ocrb_path, 40)
text_eng_name = generate_english_name()
def eng_name_bbox():
    x1, y1 = 600, 190
    x2, y2 = draw_bbox_mrz(draw, x1, y1, text_eng_name, font_eng_name)
    add_bbox_data("eng_name", x1, y1, x2, y2, text_eng_name)

# Line 4 : DOB and Gender
font_dob = ImageFont.truetype(font_khmeros_path, 34)
text_dob = f"ថ្ងៃខែឆ្នាំកំណើត: {generate_dob()}  ភេទ: {generate_gender()}  កំពស់: {generate_height()}"
def dob_bbox():
    x1, y1 = 400, 260
    x2, y2 = draw_bbox(draw, x1, y1, text_dob, font_dob)
    add_bbox_data("dob", x1, y1, x2, y2, text_dob)

# Line 5 : Place of Birth
font_pob = ImageFont.truetype(font_khmeros_path, 34)
text_pob = f"ទីកន្លែងកំណើត: {generate_place_of_birth()}"
def pob_bbox():
    x1, y1 = 400, 340
    x2, y2 = draw_bbox(draw, x1, y1, text_pob, font_pob)
    add_bbox_data("pob", x1, y1, x2, y2, text_pob)

# Line 6 : Address Line 1
font_address_1 = ImageFont.truetype(font_khmeros_path, 34)
text_address_1 = f"អាសយដ្ឋាន: {generate_address_1()}"
def address_1_bbox():
    x1, y1 = 400, 410
    x2, y2 = draw_bbox(draw, x1, y1, text_address_1, font_address_1)
    add_bbox_data("address_1", x1, y1, x2, y2, text_address_1)


# Line 7 : Address Line 2
font_address_2 = ImageFont.truetype(font_khmeros_path, 34)
text_address_2 = f"{generate_address_2()}"
def address_2_bbox():
    x1, y1 = 400, 480
    x2, y2 = draw_bbox_mrz(draw, x1, y1, text_address_2, font_address_2)
    add_bbox_data("address_2", x1, y1, x2, y2, text_address_2)

# Line 8 : Issue and Expiry Dates
font_expire = ImageFont.truetype(font_khmeros_path, 34)
text_expire = f"សុពលភាព: {to_khmer_num(str(generate_dob()))} ដល់ថ្ងៃ {to_khmer_num(str(generate_dob()))}"
def issue_expire_date_bbox():
    x1, y1 = 400, 550
    x2, y2 = draw_bbox(draw, x1, y1, text_expire, font_expire)
    add_bbox_data("issue_expire_date", x1, y1, x2, y2, text_expire)

# Line 9 : Identity Info
font_identity = ImageFont.truetype(font_khmeros_path, 34)
text_identity = "ភិនភាគ: ប្រច្រុយចុងភ្នែកស្តាំ"
def identify_bbox():
    x1, y1 = 400, 620
    x2, y2 = draw_bbox(draw, x1, y1, text_identity, font_identity)
    add_bbox_data("identify", x1, y1, x2, y2, text_identity)

# Line 10 : MRZ Line 1
font_mrz_1 = ImageFont.truetype(font_ocrb_path, 75)
text_mrz_1 = generate_mrz_1()
def mrz_1_bbox():
    x1, y1 = 50, 700
    x2, y2 = draw_bbox_mrz(draw, x1, y1, generate_mrz_1(), font_mrz_1)
    add_bbox_data("mrz_1", x1, y1, x2, y2, generate_mrz_1())

# Line 11 : MRZ Line 2
font_mrz_2 = ImageFont.truetype(font_ocrb_path, 75)
text_mrz_2 = generate_mrz_2()
def mrz_2_bbox():
    x1, y1 = 50, 800
    x2, y2 = draw_bbox_mrz(draw, x1, y1, text_mrz_2, font_mrz_2)
    add_bbox_data("mrz_2", x1, y1, x2, y2, text_mrz_2)

# Line 12 : MRZ Line 3
font_mrz_3 = ImageFont.truetype(font_ocrb_path, 75)
text_mrz_3 = generate_mrz_3()
def mrz_3_bbox():
    x1, y1 = 50, 900
    x2, y2 = draw_bbox_mrz(draw, x1, y1, text_mrz_3, font_mrz_3)
    add_bbox_data("mrz_3", x1, y1, x2, y2, text_mrz_3)

# Draw the bounding boxes and add data to JSON
id_num_bbox()
khm_name_bbox()
eng_name_bbox()
dob_bbox()
pob_bbox()
address_1_bbox()
address_2_bbox()
issue_expire_date_bbox()
identify_bbox()
mrz_1_bbox()
mrz_2_bbox()
mrz_3_bbox()

# Save or display the image
# image.show()  # This will open the image in the default image viewer
image.save('output_image.png')  # This will save the image to a file

# Export the coordinates to a JSON file
with open('bboxes.json', 'w', encoding='utf-8') as json_file:
    json.dump(bbox_data, json_file, ensure_ascii=False, indent=4)

print("Bounding box coordinates have been exported to bboxes.json")
