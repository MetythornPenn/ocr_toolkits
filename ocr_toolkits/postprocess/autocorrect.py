# autocorrect.py
import os
import re
import unicodedata
import regex
import jellyfish
import pkg_resources

# Words to exclude from correction and target words.
WORDS_EXCLUDE = {"ផ្ទះ", "ផ្លូវ"}
TARGETS = {"ផ្ទះ", "ផ្លូវ", "ភូមិ"}

def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text)

def load_resource_text(resource_path: str) -> str:
    """Load a text resource from the package."""
    return pkg_resources.resource_string(__name__, resource_path).decode("utf-8")

def load_autocorrect_dict_from_resource(resource_path: str) -> set:
    """Load words from a single file resource."""
    text = load_resource_text(resource_path)
    return {normalize_text(line.strip()) for line in text.splitlines() if line.strip()}

def load_autocorrect_dicts_from_resource(folder_resource: str) -> set:
    """Load words from all .txt files in a folder inside the package."""
    words = set()
    for filename in pkg_resources.resource_listdir(__name__, folder_resource):
        if filename.endswith(".txt"):
            resource_path = os.path.join(folder_resource, filename)
            text = load_resource_text(resource_path)
            words |= {normalize_text(line.strip()) for line in text.splitlines() if line.strip()}
    return words

# Automatically load dictionaries when the package is imported.
phum_dict = load_autocorrect_dicts_from_resource("../data/phum")
khum_dict = load_autocorrect_dicts_from_resource("../data/khum")
district_dict = load_autocorrect_dict_from_resource("../data/district.txt")
province_dict = load_autocorrect_dict_from_resource("../data/province.txt")

def autocorrect_word(word: str, word_set: set, max_ratio: float = 0.4, max_typo_distance: int = None) -> list:
    """Correct a word using Damerau-Levenshtein distance."""
    word = normalize_text(word)
    if word in word_set:
        return [word]
    max_typo_distance = max(3, int(len(word) * 0.4)) if max_typo_distance is None else max_typo_distance
    best_candidate, best_ratio = None, float("inf")
    for correct in word_set:
        d = jellyfish.damerau_levenshtein_distance(word, correct)
        ratio = d / max(len(word), len(correct))
        if d <= max_typo_distance or ratio <= max_ratio:
            if ratio < best_ratio:
                best_ratio, best_candidate = ratio, correct
    if any("០" <= ch <= "៩" for ch in word) and not (best_candidate and any("០" <= ch <= "៩" for ch in best_candidate)):
        return [word]
    return [word] if best_candidate is None or best_ratio > 0.20 else [best_candidate]

def is_number(word: str) -> bool:
    return re.sub(r"[\u200B-\u200D\uFEFF]", "", word).strip().isdigit()

def merge_tokens(part: str) -> str:
    tokens = part.split()
    merged, i = [], 0
    while i < len(tokens):
        if tokens[i] in TARGETS and i + 1 < len(tokens) and re.search(r"[A-Za-z0-9]", tokens[i + 1]):
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return " ".join(merged)

def autocorrect_word_in_part(word: str, dictionary: set) -> str:
    word = normalize_text(word)
    if is_number(word) or word in WORDS_EXCLUDE:
        return word
    if any(word.startswith(t) for t in TARGETS):
        return word
    return autocorrect_with_prefixes(word, dictionary)

def autocorrect_with_prefixes(word: str, dictionary: set) -> str:
    prefixes = {"ផ្លុវ", "ផ្លុរ", "ផ្លូរ", "ផ្លូ", "ផ្ល"}
    for prefix in prefixes:
        if word.startswith(prefix):
            return handle_prefix(word, prefix)
    return autocorrect_with_clusters(word, dictionary)

def handle_prefix(word: str, prefix: str) -> str:
    if prefix == "ផ្ល":
        m = re.search(r"[0-9\u17E0-\u17E9/]", word)
        return "ផ្លូវ" + word[m.start():] if m else "ផ្លូវ"
    return "ផ្លូវ" + word[len(prefix):]

def autocorrect_with_clusters(word: str, dictionary: set) -> str:
    clusters = regex.findall(r"\X", word)
    best_target, best_n, best_distance = None, 0, float("inf")
    for t in TARGETS:
        t_clusters = regex.findall(r"\X", t)
        if len(clusters) < len(t_clusters):
            continue
        d = jellyfish.damerau_levenshtein_distance("".join(clusters[:len(t_clusters)]), t)
        if d < best_distance:
            best_distance, best_target, best_n = d, t, len(t_clusters)
    if best_target and best_distance <= 2:
        rem = "".join(clusters[best_n:])
        return best_target + (autocorrect_word(rem, dictionary)[0] if rem.strip() else "")
    return word if word in dictionary else (autocorrect_word(word, dictionary)[0] or word)

