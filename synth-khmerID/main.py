from utils import (
    generate_commune_and_district,
    to_khmer_numeral,
    generate_dob,
    generate_gender,
    generate_place_of_birth,
    generate_address,
    generate_id_number,
    generate_issue_and_expiry_dates,
    download_image,
    generate_khmer_name,
    generate_english_name,
)


# Function to generate ID card
def generate_id_card(row, index):
    id_card = Image.new('RGB', (400, 260), color='white')
    draw = ImageDraw.Draw(id_card)

    # Load fonts
    try:
        font = ImageFont.truetype("fonts/bokor.ttf", 10)
        font_id = ImageFont.truetype("fonts/content_bold.ttf", 14)
        font_moul = ImageFont.truetype("fonts/khmer_moulight.ttf", 11)
        font_small = ImageFont.truetype("fonts/Khmer OS Content.ttf", 10)
        mrz_font = ImageFont.truetype("fonts/ocr_b.ttf", 20)
    except OSError:
        print("Font file not found.")
        return

    # Add photos
    photo_url = f'https://randomuser.me/api/portraits/{"men" if row["gender"] == "ប្រុស" else "women"}/{random.randint(0, 99)}.jpg'
    photo_filename = f"photos/{index + 1:06d}.png"
    if download_image(photo_url, photo_filename):
        photo = Image.open(photo_filename).resize((90, 140))
        id_card.paste(photo, (15, 35))

    # Add personal information
    draw.text((300, 5), row['id_number'], font=font_id, fill='black')

    # Draw the name with different fonts
    draw.text((120, 30), f"គោត្តនាមនិងនាម: ", font=font, fill='black')
    draw.text((190, 30), f"{row['name']}", font=font_moul, fill='black')
    draw.text((190, 50), f"{row['english_name'].upper()}", font=font_small, fill='black')

    draw.text((120, 70), f"ថ្ងៃខែឆ្នាំកំណើត: ", font=font, fill='black')
    draw.text((180, 72), f"{to_khmer_numeral(row['dob'][:2])}.{to_khmer_numeral(row['dob'][3:5])}.{to_khmer_numeral(row['dob'][6:])} ", font=font_small, fill='black')

    draw.text((250, 70), f"ភេទ: ", font=font, fill='black')
    draw.text((275, 72), f"{row['gender']} ", font=font_small, fill='black')

    draw.text((300, 70), f"កំពស់:", font=font, fill='black')
    draw.text((330, 72), f"{to_khmer_numeral(str(random.randint(150, 190)))}", font=font_small, fill='black')
    draw.text((360, 70), f"ស.ម", font=font, fill='black')

    draw.text((120, 90), f"ទីកន្លែងកំណើត: ", font=font, fill='black')
    draw.text((180, 92), f"{row['place_of_birth']}", font=font_small, fill='black')

    address_lines = row['address'].splitlines()
    draw.text((120, 110), f"អាសយដ្ឋាន: ", font=font, fill='black')
    draw.text((170, 112), f"{address_lines[0] if len(address_lines) > 0 else ''}", font=font_small, fill='black')
    draw.text((120, 130), f"{address_lines[1] if len(address_lines) > 1 else ''}", font=font_small, fill='black')
    draw.text((160, 150), f"{address_lines[2] if len(address_lines) > 2 else ''}", font=font_small, fill='black')

    draw.text((120, 150), f"សុពលភាព: ", font=font, fill='black')
    draw.text((170, 152),f"{to_khmer_numeral(row['issue_date'][:2])}.{to_khmer_numeral(row['issue_date'][3:5])}.{to_khmer_numeral(row['issue_date'][6:])}  ដល់ថ្ងៃ  {to_khmer_numeral(row['expiry_date'][0:2])}.{to_khmer_numeral(row['expiry_date'][3:5])}.{to_khmer_numeral(row['expiry_date'][6:])}", font=font_small, fill='black')

    # Generate a random 6-digit number
    random_number = ''.join(random.choices('0123456789', k=1))

    # Add MRZ
    gender_code = f"{random.randint(0, 9)}{'M' if row['gender'] == 'ប្រុស' else 'F'}"
    mrz_info = (
        f"IDKHM{row['id_number']}<<<<<<<<<<<<<<<"
        f"\n{row['dob'][8:10]}{row['dob'][3:5]}{row['dob'][0:2]}{gender_code}{row['expiry_date'][8:10]}{row['expiry_date'][3:5]}{row['expiry_date'][0:2]}KHM<<<<<<<<<<<{random_number}"
        f"\n{row['english_name'].upper().replace(' ', '<<')}<<<<<<<<<<<<<<<<"
    )
    draw.text((20, 180), mrz_info, font=mrz_font, fill='black')

    # Save ID card
    id_card.save(f'id_cards/{index + 1:06d}.png')


# Sample DataFrame with 5 records
data = pd.DataFrame({
    'name': [generate_khmer_name() for _ in range(5)],
    'english_name': [generate_english_name() for _ in range(5)],
    'dob': [generate_dob() for _ in range(5)],
    'gender': [generate_gender() for _ in range(5)],
    'place_of_birth': [generate_place_of_birth() for _ in range(5)],
    'address': [generate_address() for _ in range(5)],
    'id_number': [generate_id_number() for _ in range(5)],
    'issue_date': [generate_issue_and_expiry_dates()[0] for _ in range(5)],
    'expiry_date': [generate_issue_and_expiry_dates()[1] for _ in range(5)]
})

# Create directory to save ID cards
os.makedirs('id_cards', exist_ok=True)

# Generate ID cards for each record in DataFrame
for index, row in data.iterrows():
    generate_id_card(row, index)

print("All ID cards created successfully!")
print(f"You can find the ID cards in the 'id_cards' directory: {os.path.abspath('id_cards')}")