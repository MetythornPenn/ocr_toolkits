from khmerocr_tools import synthetic_data


image_height = 128
output_folder = 'output'
output_labels_file = 'labels.txt'
text_file_path = "dict.txt"  # Change this to your text file path
font_option = []  # Select font options here, e.g., [1] for Khmer OS Muol Light Regular, [2] for Khmer OS Battambang Regular, or [] for all fonts

synthetic_data(
    text_file_path, 
    image_height, 
    output_folder, 
    output_labels_file, 
    font_option=font_option, 
    random_blur=True
    )


