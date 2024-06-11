import os
from setuptools import setup, find_packages


def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

requirements = [
    "Pillow",
    "jellyfish",
    "opencv-python",
    "numpy"
]

setup(
    name="ocr-toolkits",
    version="0.0.3",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={
        'ocr-tools': [
            'font/AKbalthom KhmerLer Regular.ttf',
            'font/Khmer MEF1 Regular.ttf',
            'font/Khmer OS Battambang Regular.ttf',
            'font/Khmer OS Muol Light Regular.ttf',
            'font/Khmer OS Siemreap Regular.ttf'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/MetythornPenn/ocr-toolkits.git',
    license='Apache Software License 2.0',
    author = 'Metythorn Penn',
    author_email = 'metythorn@gmail.com',
    keywords='ocr-toolkits',
    description='Ocr_tools is a Python library that generates synthetic images containing Khmer text and other important toolbox',
    install_requires=requirements,
    long_description=(read('README.md')),
    long_description_content_type='text/markdown',
	classifiers= [
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
	],
)
