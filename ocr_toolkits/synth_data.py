from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import shutil

def calculate_font_size(text, font_path, max_height, initial_size=20):
    current_size = initial_size
    font = ImageFont.truetype(font_path, current_size)
    
    while ImageDraw.Draw(Image.new('RGB', (1, 1))).multiline_textbbox((0, 0), text, font=font)[3] < 0.9 * max_height:
        current_size += 1
        font = ImageFont.truetype(font_path, current_size)
    
    return current_size

def synthetic_data(file_path, image_height, output_folder, output_labels_file, font_option=[], random_blur=False):
    font_options = [
        {'name': 'AKbalthom KhmerLer Regular', 'file': './font/AKbalthom KhmerLer Regular.ttf'},
        {'name': 'Khmer MEF1 Regular', 'file': './font/Khmer MEF1 Regular.ttf'},
        {'name': 'Khmer OS Battambang Regular', 'file': './font/Khmer OS Battambang Regular.ttf'},
        {'name': 'Khmer OS Muol Light Regular', 'file': './font/Khmer OS Muol Light Regular.ttf'},
        {'name': 'Khmer OS Siemreap Regular', 'file': './font/Khmer OS Siemreap Regular.ttf'},
    ]
    
    if not font_option:
        selected_fonts = font_options
    else:
        selected_fonts = [font_options[i - 1] for i in font_option]

    # Remove existing output folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create output folder
    os.makedirs(output_folder, exist_ok=True)

    # Clear the content of the labels file
    open(output_labels_file, 'w', encoding='utf-8').close()

    with open(output_labels_file, 'a', encoding='utf-8') as labels_file:
        counter = 1
        text_list = open(file_path, 'r', encoding='utf-8').readlines()

        for text in text_list:
            text = text.strip()
            for font_option in selected_fonts:
                font_size = calculate_font_size(text, font_option['file'], image_height)
                font = ImageFont.truetype(font_option['file'], font_size)

                img = Image.new("RGB", (100, image_height), "white")  # Width doesn't matter initially
                d1 = ImageDraw.Draw(img)

                text_bbox = d1.textbbox((0, 0), text, font=font)
                image_width = text_bbox[2] - text_bbox[0] + 20  # Add some padding
                img = img.resize((image_width, image_height))

                d1 = ImageDraw.Draw(img)
                text_position = ((image_width - text_bbox[2]) // 2, (image_height - text_bbox[3]) // 2)
                
                text_color = "black"

                # Use the specified font when drawing text
                d1.text(text_position, text, fill=text_color, font=font)

                # Random blur
                if random_blur:
                    blur_radius = random.randint(0, 5)
                    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                # Use a simple image name with a counter
                image_name = f"{counter}.jpg"
                output_path = os.path.join(output_folder, image_name)
                img.save(output_path)

                # Write label to the labels file in real-time
                # Remove the 'output/' prefix from the output path
                output_path = output_path.replace('output/', '')
                labels_file.write(f"{output_path} {text}\n")

                print('Generate image:', output_path + ' | ' + text)
                counter += 1

# Example usage:
# image_height = 128
# output_folder = 'output'
# output_labels_file = 'labels.txt'
# text_file_path = "dict.txt"  # Change this to your text file path
# font_option = []  # Select font options here, e.g., [1] for Khmer OS Muol Light Regular, [2] for Khmer OS Battambang Regular, or [] for all fonts

# synthetic_data(text_file_path, image_height, output_folder, output_labels_file, font_option=font_option, random_blur=True)

