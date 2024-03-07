# Khmerocr_tools | Synthetic Data Generator

## Introduction

The Khmer Text Image Generator is a Python library that generates synthetic images containing Khmer text for use in training optical character recognition (OCR) models. It allows users to customize various aspects of the generated images, such as the text content, font style, background color, and blur effect.

## Features

- Generate synthetic images containing Khmer text
- Customize text content from a file
- Choose from multiple font styles
- Option to apply random blur effect to images
- Generate corresponding labels for each image


## Installation

You can install the Khmer Text Image Generator using pip:

```bash
pip install khmerocr_tools
```


## Usage

```python
from khmerocr_tools import synthetics_data

# Set parameters
image_height = 128
output_folder = 'output'
output_labels_file = 'labels.txt'
text_file_path = "text.txt"
font_option = [1, 2]  

# Generate images and labels
synthetics_data(
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
