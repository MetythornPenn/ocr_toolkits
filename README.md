# OCR toolkits

## Introduction

Collection of functions to work with ocr and synthetic data generater

## Features

- Generate synthetic images containing Khmer text
- Customize text content from a file
- Choose from multiple font styles
- Option to apply random blur effect to images
- Generate corresponding labels for each image

## Installation

You can install the Khmer Text Image Generator using pip:

```bash
pip install ocr_toolkits
```


## Usage

- create text file to words list eg. dict.txt and put all khmer words you want to gnerate or download [sample data here](https://github.com/MetythornPenn/khmerocr_tools/blob/main/dict.txt)

- create a folder call font and download all font from this link : [font](https://github.com/MetythornPenn/khmerocr_tools/tree/main/font)

- create python script to generate data eg. test.py
```python
from khmerocr_tools import synthetic_data

# Set parameters
image_height = 128
output_folder = 'output'
output_labels_file = 'output/labels.txt'
text_file_path = "dict.txt"
font_option = [1, 2]  

# Generate images and labels
synthetic_data(
    text_file_path, 
    image_height, 
    output_folder, 
    output_labels_file, 
    font_option=font_option, 
    random_blur=True
)

```

## Parameters

- `image_height`: Height of the generated images in pixels.
- `output_folder`: Path to the folder where generated images will be saved.
- `output_labels_file`: Path to the file where labels will be saved.
- `text_file_path`: Path to the text file containing Khmer text for generation.
- `font_option`: List of integers representing font options. 
  - 1 for AKbalthom KhmerLer Regular.
  - 2 for Khmer MEF1 Regular.
  - 3 for Khmer OS Battambang Regular.
  - 4 for Khmer OS Muol Light Regular.
  - 5 for Khmer OS Siemreap Regular.
  - Use an empty list [] to select all available fonts.
- `random_blur`: Boolean flag indicating whether to apply random blur effect to images.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
