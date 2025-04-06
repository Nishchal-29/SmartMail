# import spacy
from collections import Counter
import json
import re
import json
# nlp = spacy.load("en_core_web_sm")

with open("DataWithParam.json","r") as f:
    data = json.load(f)

def build_user_profile(data):
    total_conciseness = 0.0
    count = 0
    tone_counter = Counter()
    total_tones = 0
    category_counter = Counter()
    total_categories = 0
    for item in data:
        tone_str = item["metadata"].get("tone", "")
        tones = [tone.strip() for tone in tone_str.split(",") if tone.strip()]
        tone_counter.update(tones)
        total_tones += len(tones)
        cat_str = item["metadata"].get("category", "")
        categories = [cat.strip() for cat in cat_str.split(",") if cat.strip()]
        category_counter.update(categories)
        total_categories += len(categories)
        conciseness = item["metadata"].get("conciseness")
        if conciseness is not None:
            total_conciseness += conciseness
            count += 1

    avg_conciseness = round(total_conciseness / count, 3) if count > 0 else 0.0
    tone_profile = {
        tone: round(count / total_tones, 3)
        for tone, count in tone_counter.items()
    }
    category_profile = {
        category: round(count / total_categories, 3)
        for category, count in category_counter.items()
    }
    return (tone_profile,category_profile,avg_conciseness)

def build_tone_profile(data):
    tone_counter = Counter()
    total_tones = 0

    for item in data:
        tone_str = item["metadata"].get("tone", "")
        tones = [tone.strip() for tone in tone_str.split(",") if tone.strip()]
        tone_counter.update(tones)
        total_tones += len(tones)
        

    # Normalize to get frequencies
    tone_profile = {
        tone: round(count / total_tones, 3)
        for tone, count in tone_counter.items()
    }

    return tone_profile
def get_top_n_tones(tone_profile, n=2):
    return sorted(tone_profile.items(), key=lambda x: x[1], reverse=True)[:n]

def build_category_profile(data):
    category_counter = Counter()
    total_categories = 0

    for item in data:
        cat_str = item["metadata"].get("category", "")
        categories = [cat.strip() for cat in cat_str.split(",") if cat.strip()]
        category_counter.update(categories)
        total_categories += len(categories)

    # Normalize
    category_profile = {
        category: round(count / total_categories, 3)
        for category, count in category_counter.items()
    }

    return category_profile

def build_conciseness_profile(data):
    total_conciseness = 0.0
    count = 0

    for item in data:
        conciseness = item["metadata"].get("conciseness")
        if conciseness is not None:
            total_conciseness += conciseness
            count += 1

    avg_conciseness = round(total_conciseness / count, 3) if count > 0 else 0.0
    return avg_conciseness


# def build_top_phrases_profile(data, top_n=10):
#     phrase_counter = Counter()
#     pattern = r"\('(.+?)',\s*np\.int64\((\d+)\)\)"

#     for item in data:
#         top_phrases_list = item["metadata"].get("top_phrases", [])
#         for phrase_str in top_phrases_list:
#             match = re.match(pattern, phrase_str)
#             if match:
#                 phrase, count = match.groups()
#                 phrase_counter[phrase] += int(count)
#             else:
#                 print(f"Skipped unparsable phrase: {phrase_str}")
    
#     return phrase_counter.most_common(top_n)


# def extract_phrases(text, max_phrase_len=4):
#     doc = nlp(text)
#     phrases = []

#     for chunk in doc.noun_chunks:
#         phrase = chunk.text.lower().strip()
#         if 1 <= len(phrase.split()) <= max_phrase_len:
#             phrases.append(phrase)
    
#     return phrases

# def build_top_phrases_profile_spacy(data, top_n=10):
#     phrase_counter = Counter()

#     for item in data:
#         email_text = item.get("email", "")
#         phrases = extract_phrases(email_text)
#         phrase_counter.update(phrases)
    
#     return phrase_counter.most_common(top_n)

# tone_profile = build_tone_profile(data)
# print(tone_profile)
# print(get_top_n_tones(tone_profile))
# print(get_top_n_tones(tone_profile))
# category_profile = build_category_profile(data)
# print(category_profile)
# top_phrase_profile = build_top_phrases_profile_spacy(data)
# print(top_phrase_profile)
# conciseness_profile = build_conciseness_profile(data)
# print(conciseness_profile)

user_profile = build_user_profile(data)
# print(user_profile)

user_profile = {
    "user1": {
        "tone_profile": user_profile[0],
        "category_profile": user_profile[1],
        "avg_conciseness": user_profile[2]
    }
}
with open("hackfest/new/userProfile.json", "w") as f:
    json.dump(user_profile, f, indent=2)