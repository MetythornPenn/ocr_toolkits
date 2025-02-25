import regex
import jellyfish
from datetime import datetime, timedelta
from autocorrect import *

def autocorrect_gender(input_text: str, return_eng: bool = False) -> str:
    target_gender_male = "ប្រុស"
    target_gender_female = "ស្រី" 
    similarity_threshold = 0.6

    try:
        # Validate input type
        if not isinstance(input_text, str):
            raise TypeError("Input text must be a string.")

        jaro_distance_similarity_male = jellyfish.jaro_winkler_similarity(input_text, target_gender_male)
        jaro_distance_similarity_female = jellyfish.jaro_winkler_similarity(input_text, target_gender_female)

        if jaro_distance_similarity_male >= similarity_threshold:
            return "Male" if return_eng else target_gender_male
        elif jaro_distance_similarity_female >= similarity_threshold:
            return "Female" if return_eng else target_gender_female
        else:
            return input_text

    except TypeError as e:
        print(f"Error: {e}")
        return input_text

def autocorrect_address_1(part: str, dictionary: set = phum_dict) -> str:
    return " ".join(autocorrect_word_in_part(w, dictionary) for w in merge_tokens(part).split())

def autocorrect_address_2(address_2_text: str, khum_dictionary: set = khum_dict, district_dictionary: set = district_dict, province_dictionary: set = province_dict) -> str:
    parts = address_2_text.split()
    if len(parts) >= 2 and is_number(parts[1]):
        commune, district, province = parts[0] + parts[1], parts[2] if len(parts) > 2 else "", " ".join(parts[3:]) if len(parts) > 3 else ""
    else:
        commune, district, province = (parts[0], parts[1], " ".join(parts[2:])) if len(parts) >= 4 else (parts[0], parts[1] if len(parts) > 1 else "", " ".join(parts[2:]) if len(parts) > 2 else "")
    corrected_commune = autocorrect_word(commune, khum_dictionary, max_ratio=0.6)[0]
    corrected_district = autocorrect_word(district, district_dictionary, max_ratio=0.6)[0] if district else ""
    corrected_province = autocorrect_word(province, province_dictionary, max_ratio=0.6)[0] if province else ""
    return " ".join(filter(None, [corrected_commune, corrected_district, corrected_province]))

def autocorrect_province(province_text: str) -> str:
    return autocorrect_word(province_text, province_dict, max_ratio=0.6)[0]

def autocorrect_district(district_text: str) -> str:
    return autocorrect_word(district_text, district_dict, max_ratio=0.6)[0]

def autocorrect_khum(khum_text: str) -> str:
    return autocorrect_word(khum_text, khum_dict, max_ratio=0.6)[0]

def autocorrect_phum(phum_text: str) -> str:
    phum_text = normalize_text(phum_text)
    if phum_text.startswith("ភូមិ"):
        rem = phum_text[len("ភូមិ"):]
        return "ភូមិ" + autocorrect_word(rem, phum_dict, max_ratio=0.6)[0] if rem.strip() else "ភូមិ"
    return autocorrect_with_clusters(phum_text, phum_dict)

