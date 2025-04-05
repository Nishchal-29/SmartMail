import generate_conv
import json
import time

INPUT_FILE = "dataForTest.json"
OUTPUT_FILE = "./modified.json"
SLEEP_DURATION = 10
RETRY_WAIT = 15

def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(i) for i in obj]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, "item"):  # Handles numpy.int64, float64, etc.
        return obj.item()
    else:
        return str(obj)

def process_item(item, count):
    email = item.get('email')
    response = item.get('response')

    while True:
        try:
            formality = generate_conv.get_formality(email, response)
            if isinstance(formality, list):
                formality = {str(i): val for i, val in enumerate(formality)}

            item['metadata'] = {
                "formality": formality,
                "tone": generate_conv.get_tone(email, response),
                "category": generate_conv.get_category(email, response),
                "negotiation_style": generate_conv.get_negotiation(email, response),
                "top_phrases": generate_conv.get_top_phrases([response])
            }
            return item
        except Exception as e:
            print(f"Error on item {count}: {e}\n⏳ Retrying in {RETRY_WAIT} seconds...\n")
            time.sleep(RETRY_WAIT)

def main():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    result = []

    for count, item in enumerate(data, start=1):
        print(f"Processing item {count}/{len(data)}...")
        processed = process_item(item, count)
        result.append(sanitize_for_json(processed))
        print(f"Processed item {count}. Sleeping for {SLEEP_DURATION} seconds...\n")
        time.sleep(SLEEP_DURATION)

    # Write full array as valid JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nAll items processed and saved to '{OUTPUT_FILE}' as a proper JSON array.")

if __name__ == "__main__":
    main()
