from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="khmerocr-tools",
    version="0.13",
    description="Khmerocr_tools is a Python library that generates synthetic images containing Khmer text",
    package_dir={"": "app"},
    package_data={'khmerocr_tools': ['font/*.ttf']},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MetythornPenn/khmerocr_tools",
    author="Metythorn Penn",
    author_email="Metythorn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["Pillow>=10.2.0"],
    # extras_require={
    #     "dev": ["twine>=4.0.2"],
    # },
    python_requires=">=3.8",
)
