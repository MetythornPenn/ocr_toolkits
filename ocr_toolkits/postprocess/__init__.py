import jellyfish


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