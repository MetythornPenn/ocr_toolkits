import json, os
from PIL import Image, ImageDraw, ImageFont

from pykhmernlp.number import to_khmer_num
from pykhmernlp.tokenizer import khmercut

from utils import (
    generate_dob,
    generate_gender,
    generate_height,
    generate_place_of_birth,
    generate_address_1,
    generate_address_2,
    generate_id_number,
    generate_khmer_name,
    generate_english_name,
    generate_mrz_1,
    generate_mrz_2,
    generate_mrz_3,
    get_random_image_path,
)

# Define the font path and size
font_paths = {
    "bokor": "fonts/ocr_b.ttf",
    "content_bold": "fonts/content_bold.ttf",
    "dejavu": "fonts/DejaVuSansMono.ttf",
    "khmeros": "fonts/Khmer OS Content.ttf",
    "khmer_moul": "fonts/khmer_moul.ttf",
    "ocrb": "fonts/ocr_b.ttf"
}

font_size = 12
fonts = {
    name: ImageFont.truetype(path, font_size) for name, path in font_paths.items()
}
fonts["content_bold"] = ImageFont.truetype(font_paths["content_bold"], 55)
fonts["ocrb_large"] = ImageFont.truetype(font_paths["ocrb"], 50)
fonts["mrz"] = ImageFont.truetype(font_paths["ocrb"], 75)
fonts["khmeros"] = ImageFont.truetype(font_paths["khmeros"], 32)
fonts["khmer_moul"] = ImageFont.truetype(font_paths["khmer_moul"], 34)

# Directories for saving images and annotations
output_image_dir = "./data/synth-khmerID/images"
output_annotation_dir = "./data/synth-khmerID/annotations"

# Create directories if they do not exist
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_annotation_dir, exist_ok=True)

# Function to generate a single ID card image and its annotation
def generate_id_card_image(index):
    # Create a blank white image
    width, height = 1575, 1024
    image = Image.new('RGB', (width, height), 'white')

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Get a random photo path and paste it on the image
    photo_folder = "photos"
    photo_path = get_random_image_path(photo_folder)
    photo = Image.open(photo_path).resize((320, 500))
    image.paste(photo, (55, 80))

    bbox_data = {"id_card": []}

    def draw_bbox(draw, x1, y1, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        padding_x, padding_y = 10, 10

        x2 = x1 + text_width + 2 * padding_x
        y2 = y1 + text_height + 2 * padding_y

        draw.rectangle([x1, y1, x2, y2], outline='red')
        text_x = x1 + padding_x
        text_y = y1 + (y2 - y1 - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill='black')

        return x2, y2

    def draw_bbox_mrz(draw, x1, y1, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        padding_x, padding_y = 10, 10

        x2 = x1 + text_width + 2 * padding_x
        y2 = y1 + text_height + 2 * padding_y

        draw.rectangle([x1, y1, x2, y2 + 15], outline='red')
        text_x = x1 + padding_x
        text_y = y1 + (y2 - y1 - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill='black')

        return x2, y2

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

    # Functions to draw and add bounding boxes for each line
    def draw_all_bboxes():
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

    def id_num_bbox():
        text_id_num = generate_id_number()
        x1, y1 = 1100, 20
        x2, y2 = draw_bbox_mrz(draw, x1, y1, text_id_num, fonts["ocrb_large"])
        add_bbox_data("id_num", x1, y1, x2, y2-10, text_id_num)

    def khm_name_bbox():
        text_khmer_name = f"គោត្តនាមនិងនាម: {khmercut(generate_khmer_name())[0]} {khmercut(generate_khmer_name())[0]}"
        x1, y1 = 400, 90
        x2, y2 = draw_bbox(draw, x1, y1, text_khmer_name, fonts["khmer_moul"])
        add_bbox_data("khm_name", x1, y1, x2, y2, text_khmer_name)

    def eng_name_bbox():
        text_eng_name = generate_english_name()
        x1, y1 = 600, 165
        x2, y2 = draw_bbox_mrz(draw, x1, y1, text_eng_name, fonts["ocrb_large"])
        add_bbox_data("eng_name", x1, y1, x2, y2, text_eng_name)

    def dob_bbox():
        text_dob = f"ថ្ងៃខែឆ្នាំកំណើត: {generate_dob()}  ភេទ: {generate_gender()}  កំពស់: {generate_height()} ស.ម"
        x1, y1 = 400, 240
        x2, y2 = draw_bbox(draw, x1, y1, text_dob, fonts["khmeros"])
        add_bbox_data("dob", x1, y1, x2, y2, text_dob)

    def pob_bbox():
        text_pob = f"ទីកន្លែងកំណើត: {generate_place_of_birth()}"
        x1, y1 = 400, 314
        x2, y2 = draw_bbox(draw, x1, y1, text_pob, fonts["khmeros"])
        add_bbox_data("pob", x1, y1, x2, y2, text_pob)

    def address_1_bbox():
        text_address_1 = f"អាសយដ្ឋាន: {generate_address_1()}"
        x1, y1 = 400, 390
        x2, y2 = draw_bbox(draw, x1, y1, text_address_1, fonts["khmeros"])
        add_bbox_data("address_1", x1, y1, x2, y2, text_address_1)

    def address_2_bbox():
        text_address_2 = f"{generate_address_2()}"
        x1, y1 = 400, 470
        x2, y2 = draw_bbox(draw, x1, y1, text_address_2, fonts["khmeros"])
        add_bbox_data("address_2", x1, y1, x2, y2, text_address_2)

    def issue_expire_date_bbox():
        text_expire = f"សុពលភាព: {to_khmer_num(str(generate_dob()))} ដល់ថ្ងៃ {to_khmer_num(str(generate_dob()))}"
        x1, y1 = 400, 550
        x2, y2 = draw_bbox(draw, x1, y1, text_expire, fonts["khmeros"])
        add_bbox_data("issue_expire_date", x1, y1, x2, y2, text_expire)

    def identify_bbox():
        text_identity = "ភិនភាគ: ប្រច្រុយចុងភ្នែកស្តាំ"
        x1, y1 = 400, 630
        x2, y2 = draw_bbox(draw, x1, y1, text_identity, fonts["khmeros"])
        add_bbox_data("identify", x1, y1, x2, y2, text_identity)

    def mrz_1_bbox():
        text_mrz_1 = generate_mrz_1()
        x1, y1 = 60, 710
        x2, y2 = draw_bbox_mrz(draw, x1, y1, text_mrz_1, fonts["mrz"])
        add_bbox_data("mrz_1", x1, y1, x2, y2, text_mrz_1)

    def mrz_2_bbox():
        text_mrz_2 = generate_mrz_2()
        x1, y1 = 60, 810
        x2, y2 = draw_bbox_mrz(draw, x1, y1, text_mrz_2, fonts["mrz"])
        add_bbox_data("mrz_2", x1, y1, x2, y2, text_mrz_2)

    def mrz_3_bbox():
        text_mrz_3 = generate_mrz_3()
        x1, y1 = 60, 910
        x2, y2 = draw_bbox_mrz(draw, x1, y1, text_mrz_3, fonts["mrz"])
        add_bbox_data("mrz_3", x1, y1, x2, y2, text_mrz_3)

    # Draw the bounding boxes and add data to JSON
    draw_all_bboxes()

    # Define file paths
    image_filename = f"{index:06d}.png"
    annotation_filename = f"{index:06d}.json"
    image_path = os.path.join(output_image_dir, image_filename)
    annotation_path = os.path.join(output_annotation_dir, annotation_filename)

    # Save the image
    image.save(image_path)

    # Save the bounding box data to JSON file
    with open(annotation_path, 'w', encoding='utf-8') as json_file:
        json.dump(bbox_data, json_file, ensure_ascii=False, indent=4)

    print(f"Generated {image_filename} and {annotation_filename}")
    
    
    
if __name__ == "__main__":
    # Generate 100 images and their corresponding annotations
    for i in range(1, 1001):
        generate_id_card_image(i)
