import json
import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont
import random
import string

from datetime import datetime, timedelta
import os
from pykhmernlp.corpus import km_words, en_words
from pykhmernlp.address import km_villages, km_commune, km_districts
from pykhmernlp.number import to_khmer_num

from pykhmernlp.number import to_khmer_num

# Fetch Khmer and English words
km_words = km_words()
en_words = en_words()


def generate_height():
    return to_khmer_num(str(random.randint(130, 220)))


# """------------ Line 1 : ID Card Number ------------- """

# Function to generate a random ID number
def generate_9_digit_number() -> str:
    return ''.join(random.choices('0123456789', k=9))

def generate_7_digit_number() -> str:
    return ''.join(random.choices('0123456789', k=7))


def random_01(null_prob=0.9) -> str:
    ls_text = ["", " (01)"]
    weights = [null_prob, 1 - null_prob]
    ran = random.choices(ls_text, weights=weights, k=1)[0]
    return ran


def generate_id_number() -> str :
    return generate_9_digit_number() + random_01()




# Function to generate random commune and district
def generate_commune_and_district(village):
    parts = village.split()
    return parts[-2], parts[-1]


# Function to generate a random date of birth
def generate_dob():
    start_date = datetime(1960, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_dob = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    date =  random_dob.strftime('%d.%m.%Y')
    return to_khmer_num(date)

# Function to generate a random gender
def generate_gender(female_prob= 0.55) -> str:
    genders_ls = ['ស្រី', 'ប្រុស']
    weights = [female_prob, 1 - female_prob]
    ran = random.choices(genders_ls, weights=weights, k=1)[0]
    return ran
    
def generate_gender_eng(female_prob= 0.55) -> str:
    genders_ls = ['F', 'M']
    weights = [female_prob, 1 - female_prob]
    ran = random.choices(genders_ls, weights=weights, k=1)[0]
    return ran


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
def generate_address_1():
    villages = km_villages()
    return f"{random.choice(villages)}"\


def generate_address_2():
    communes = km_commune()
    districts = km_districts()
    provinces = [
        "សៀមរាប", "ស្ទឹងត្រែង", "ស្វាយរៀង", "តាកែវ", "ត្បូងឃ្មុំ",
        "បាត់ដំបង", "បន្ទាយមានជ័យ", "កំពត", "កំពង់ឆ្នាំង", "កណ្ដាល",
        "កែប", "កោះកុង", "កំពង់ចាម", "កំពង់ធំ", "ក្រចេះ",
        "កំពង់ស្ពឺ", "មណ្ឌលគិរី", "ឧត្ដរមានជ័យ", "ប៉ៃលិន", "រាជធានីភ្នំពេញ",
        "ពោធិ៍សាត់", "ព្រៃវែង", "ព្រះវិហារ", "រតនគិរី", "ព្រះសីហនុ"
    ]
    return f"{random.choice(communes)} {random.choice(districts)} {random.choice(provinces)}"\


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
    # if len(first_name) > 5:
    #     first_name = first_name[:5]
    # if len(last_name) > 5:
    #     last_name = last_name[:5]
    return f"{first_name} {last_name}"


# Generate English names
def generate_english_name() -> str:
    first_name_length = random.randint(1, min(6, len(en_words)))
    last_name_length = random.randint(1, min(6, len(en_words)))
    first_name = ''.join(random.choices(en_words, k=first_name_length))
    last_name = ' '.join(random.sample(en_words, k=last_name_length))
    
    if len(first_name) > 5:
        first_name = first_name[:5]
    if len(last_name) > 5:
        last_name = last_name[:6]
    return f"{first_name.upper()} {last_name.upper()}"






def generate_mrz_1() -> str:
    prefix = "IDKHM"
    id_num = generate_9_digit_number()
    dynamic_max_len = random.randint(31, 31)
    min_symb_len = 0
    required_length = dynamic_max_len - len(prefix) - len(id_num)
    dynamic_symb = max(min_symb_len, int(required_length)) * "<"
    mrz_1 = prefix + id_num + dynamic_symb
    return mrz_1.upper()


def generate_mrz_2() -> str:
    num_first = generate_7_digit_number()
    gender = generate_gender_eng()
    num_last = generate_7_digit_number()
    suffix = "KHM"
    num_last = str(random.randint(0, 9))
    dynamic_max_len = random.randint(31, 31)
    min_symb_len = 0
    
    required_length = dynamic_max_len - len(num_first) - len(gender) - len(num_last) - len(suffix) - len(num_last)
    dynamic_symb = max(min_symb_len, int(required_length)) * "<"
    mrz_2 = num_first + gender + num_last + suffix + dynamic_symb + num_last
    return mrz_2.upper()


def dynamic_fname() -> str:
    char_set = string.ascii_letters
    random_len = random.randint(3, 10)
    random_string = ''.join(random.choices(char_set, k=random_len))
    return random_string
    
def dynamic_lname() -> str:
    char_set = string.ascii_letters
    random_len = random.randint(3, 8)
    random_string = ''.join(random.choices(char_set, k=random_len))
    return random_string


def generate_mrz_3() -> str:
    fname = dynamic_fname()
    mid_symb = "<<"
    lname = dynamic_lname()
    dynamic_max_len = random.randint(31, 31)
    min_symb_len = 0
    required_length = dynamic_max_len - len(fname) - len(mid_symb) - len(lname)
    dynamic_symb = max(min_symb_len, int(required_length)) * "<"
    mrz_1 = fname + mid_symb + lname + dynamic_symb
    return mrz_1.upper()




