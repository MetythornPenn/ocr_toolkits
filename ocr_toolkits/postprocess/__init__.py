import regex
import jellyfish
from datetime import datetime, timedelta



def extract_mrz1(text):
    
    # Define the regular expression pattern with a capture group for digits
    # pattern = r"IDKHM(\d+)<+$"  # Capture any number of digits
    # pattern = r"(?i)IDK?HM(\d+)<+$"
    pattern = r"(?i)(?:I{0,2}D?K?H?M?)(\d+)<+$" 

    # Search for matches using the pattern after potential OCR correction
    transform_text = text.replace("O", "0").replace("o","0").replace("I", "1")
    match = regex.search(pattern, transform_text)

    # If a match is found, extract the ID number
    if match:
        id_number = match.group(1)
        if len(id_number) == 10:
            return id_number[:-1]
        else:
            return id_number
            
    else:
        # Return None if no match is found
        return None



def extract_mrz2(text):
    # Define the regular expression pattern to match the specified format
    pattern = r'(\d{7})([FM])(\d{7})'

    # Search for matches using the pattern
    transform_text = text.replace("o", "0").replace("O","0").replace("I", "1")
    match = regex.search(pattern, transform_text)

    # If a match is found, extract date of birth, gender, and expiry date
    if match:
        dob_part = match.group(1)
        gender = match.group(2)
        exp_part = match.group(3)
        
        # Extract date components for date of birth
        dob_day = dob_part[4:6]
        dob_month = dob_part[2:4]
        dob_year = dob_part[:2]
        
        # Extract date components for expiry date
        exp_day = exp_part[4:6]
        exp_month = exp_part[2:4]
        exp_year = exp_part[:2]
        
        # Calculate expiry date as datetime object
        expiry_date = datetime.strptime(f"20{exp_year}{exp_month}{exp_day}", "%Y%m%d")
        
        # Calculate issue date by subtracting 10 years from expiry date
        issue_date = expiry_date - timedelta(days=3652)  # 10 years minus 2 leap days
        
        # Format date strings
        dob_str = f"{dob_day}-{dob_month}-{dob_year}"
        issue_date_str = issue_date.strftime("%d-%m-%y")
        expiry_date_str = expiry_date.strftime("%d-%m-%y")
        
        # Determine gender
        gender_str = 'Female' if gender == 'F' else 'Male'

        return dob_str, issue_date_str, expiry_date_str, gender_str
    else:
        # Return None if no match is found
        return None
    
    
def extract_mrz3(text):
    # Define the regular expression pattern
    # This pattern captures `fname` and `lname` while allowing for noisy characters and spaces
    pattern = r'(?P<fname>[\w\s-]+?)\s*<{1,3}\s*(?P<lname>\w+)\s*<{5,}.*'
    
    # Search for matches using the pattern
    transform_text = text.replace("o", "O").replace("0", "O").replace("1", "I")
    match = regex.search(pattern, transform_text)
    
    # If a match is found, extract fname and lname
    if match:
        fname = match.group('fname').replace(' ', '')  # Remove any spaces from fname
        lname = match.group('lname').replace(' ', '')
        
        # Uppercase fname, lname
        fname = fname.upper()
        lname = lname.upper()
        
        return fname, lname
    else:
        # Return None if no match is found
        return None
    


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