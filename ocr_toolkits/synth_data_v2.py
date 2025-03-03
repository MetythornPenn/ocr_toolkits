import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import time
from tqdm import tqdm 


def calculate_font_size(text, font_path, max_height, initial_size=20):
    current_size = initial_size
    font = ImageFont.truetype(font_path, current_size)

    while (
        ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textbbox(
            (0, 0), text, font=font
        )[3]
        < 0.9 * max_height
    ):
        current_size += 1
        font = ImageFont.truetype(font_path, current_size)

    return current_size


def synthetic_data_v2(
    file_path,
    image_height,
    output_folder,
    output_labels_file,
    font_option=[],
    random_blur=False,
    repeat=1,
):

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
        
        
    # Define a list of background colors (black, white, gray)
    background_colors = [
        (0, 0, 0),  # Black
        (255, 255, 255),  # White
        (128, 128, 128),  # Gray
    ]

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Start the timer
    start_time = time.time()  # Define start_time here

    # Open the labels file in append mode
    with open(output_labels_file, "a", encoding="utf-8") as labels_file:
        text_list = open(file_path, "r", encoding="utf-8").readlines()

        # Initialize tqdm progress bar with a fixed position
        total_images = len(text_list) * repeat
        with tqdm(
            total=total_images,
            desc="Generating Images",
            unit="image",
            position=0,
            leave=True,
        ) as pbar:
            counter = 1  # Initialize counter for image naming

            for text in text_list:
                text = text.strip()
                for _ in range(repeat):
                    try:
                        # Randomly select a font if font_option is 'random'
                        if font_option == "random":
                            font = random.choice(selected_fonts)
                        else:
                            # Use the first font if not random
                            font = selected_fonts[0]

                        font_size = calculate_font_size(
                            text, font["file"], image_height
                        )
                        font_obj = ImageFont.truetype(font["file"], font_size)

                        # Randomly select a background color
                        background_color = random.choice(background_colors)

                        # Set text color based on background color
                        if background_color == (0, 0, 0):  # Black background
                            text_color = (255, 255, 255)  # White text
                        else:
                            # Black text for white/gray backgrounds
                            text_color = (0, 0, 0)

                        # Width doesn't matter initially
                        img = Image.new("RGB", (100, image_height), background_color)
                        d1 = ImageDraw.Draw(img)

                        text_bbox = d1.textbbox((0, 0), text, font=font_obj)
                        image_width = (
                            text_bbox[2] - text_bbox[0] + 20
                        )  # Add some padding
                        img = img.resize((image_width, image_height))

                        d1 = ImageDraw.Draw(img)
                        text_position = (
                            (image_width - text_bbox[2]) // 2,
                            (image_height - text_bbox[3]) // 2,
                        )

                        # Use the specified font when drawing text
                        d1.text(text_position, text, fill=text_color, font=font_obj)

                        # Random blur
                        if random_blur:
                            blur_radius = random.randint(0, 5)
                            img = img.filter(
                                ImageFilter.GaussianBlur(radius=blur_radius)
                            )

                        # Use a simple image name with a counter
                        image_name = f"{counter}.jpg"
                        output_path = os.path.join(output_folder, image_name)
                        img.save(output_path)

                        # Write label to the labels file in real-time
                        relative_output_path = os.path.relpath(
                            output_path, start="dataset/final"
                        )
                        labels_file.write(f"{relative_output_path} {text}\n")

                        # Print the image details below the progress bar
                        tqdm.write(f"Generate image: {output_path} | Text: {text}")
                        counter += 1
                        pbar.update(1)  # Update the progress bar

                    except Exception as e:
                        tqdm.write(
                            f"Error generating image for text '{text}' with font '{font['name']}': {e}"
                        )
                        continue

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)
    print(f"Total time taken: {elapsed_minutes} minutes {elapsed_seconds} seconds")

#Set parameters
image_height = 128
output_folder = "output"
output_labels_file = "labels.txt"
text_file_path = "dict.txt"
repeat = 20  # Generate 4 images for each text
font_option = [1,2]

#Generate images and lebels
synthetic_data_v2(
    file_path=text_file_path,
    font_option=font_option,
    image_height=image_height,
    output_folder=output_folder,
    output_labels_file=output_labels_file,
    random_blur=True,
    repeat=repeat,
)
