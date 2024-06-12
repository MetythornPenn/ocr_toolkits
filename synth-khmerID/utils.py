import json
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont
import random
from datetime import datetime, timedelta
import os
from pykhmernlp.corpus import km_words, en_words
from pykhmernlp.address import km_villages, km_commune, km_districts
from pykhmernlp.number import to_khmer_num



# Fetch Khmer and English words
km_words = km_words()
en_words = en_words()


# Function to generate random commune and district
def generate_commune_and_district(village):
    parts = village.split()
    return parts[-2], parts[-1]


# Function to convert numeric strings to Khmer numerals
def to_khmer_numeral(number):
    khmer_digits = '០១២៣៤៥៦៧៨៩'
    return ''.join(khmer_digits[int(digit)] for digit in str(number) if digit.isdigit())


# Function to generate a random date of birth
def generate_dob():
    start_date = datetime(1960, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_dob = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_dob.strftime('%d.%m.%Y')

# Function to generate a random gender
def generate_gender():
    genders = ['ប្រុស', 'ស្រី']
    return random.choice(genders)


# Function to generate a random place of birth
def generate_place_of_birth():
    communes = km_commune()
    districts = km_districts()
    provinces = [
        "សៀមរាប", "ស្ទឹងត្រែង", "ស្វាយរៀង", "តាកែវ", "ត្បូងឃ្មុំ",
        "បាត់ដំបង", "បន្ទាយមានជ័យ", "កំពត", "កំពង់ឆ្នាំង", "កណ្ដាល",
        "កែប", "កោះកុង", "កំពង់ចាម", "កំពង់ធំ", "ក្រចេះ",
        "កំពង់ស្ពឺ", "មណ្ឌលគិរី", "ឧត្ដរមានជ័យ", "ប៉ៃលិន", "រាជធានីភ្នំពេញ",
        "ពោធិ៍សាត់", "ព្រៃវែង", "ព្រះវិហារ", "រតនគិរី", "ព្រះសីហនុ"
    ]
    return f"{random.choice(communes)} {random.choice(districts)} {random.choice(provinces)}"

# Function to generate a random address
def generate_address():
    villages = km_villages()
    communes = km_commune()
    districts = km_districts()
    provinces = [
        "សៀមរាប", "ស្ទឹងត្រែង", "ស្វាយរៀង", "តាកែវ", "ត្បូងឃ្មុំ",
        "បាត់ដំបង", "បន្ទាយមានជ័យ", "កំពត", "កំពង់ឆ្នាំង", "កណ្ដាល",
        "កែប", "កោះកុង", "កំពង់ចាម", "កំពង់ធំ", "ក្រចេះ",
        "កំពង់ស្ពឺ", "មណ្ឌលគិរី", "ឧត្ដរមានជ័យ", "ប៉ៃលិន", "រាជធានីភ្នំពេញ",
        "ពោធិ៍សាត់", "ព្រៃវែង", "ព្រះវិហារ", "រតនគិរី", "ព្រះសីហនុ"
    ]
    return f"{random.choice(villages)}\n{random.choice(communes)} {random.choice(districts)} {random.choice(provinces)}"\

# Function to generate a random ID number
def generate_id_number():
    return ''.join(random.choices('0123456789', k=9))

# Function to generate random issue and expiry dates
def generate_issue_and_expiry_dates():
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 12, 31)
    issue_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    expiry_date = issue_date + timedelta(days=random.randint(365 * 5, 365 * 10))
    return issue_date.strftime('%d.%m.%Y'), expiry_date.strftime('%d.%m.%Y')

# Function to download an image from a URL
def download_image(url, filename):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Error downloading image: {e}")
        return False


# Generate Khmer names
def generate_khmer_name():
    first_name_length = random.randint(1, min(5, len(km_words)))
    last_name_length = random.randint(1, min(5, len(km_words)))
    first_name = ''.join(random.choices(km_words, k=first_name_length))
    last_name = ''.join(random.choices(km_words, k=last_name_length))
    if len(first_name) > 5:
        first_name = first_name[:5]
    if len(last_name) > 5:
        last_name = last_name[:5]
    return f"{first_name} {last_name}"


# Generate English names
def generate_english_name():
    first_name_length = random.randint(1, min(6, len(en_words)))
    last_name_length = random.randint(1, min(6, len(en_words)))
    first_name = ''.join(random.choices(en_words, k=first_name_length))
    last_name = ' '.join(random.sample(en_words, k=last_name_length))
    if len(first_name) > 5:
        first_name = first_name[:5]
    if len(last_name) > 5:
        last_name = last_name[:6]
    return f"{first_name} {last_name}"

