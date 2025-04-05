import json

INPUT_FILE = "modified.json"
OUTPUT_FILE = "id_email.json"

def main():
    # Read input JSON array
    with open(INPUT_FILE, "r") as infile:
        data = json.load(infile)

    # Extract only id and email
    result = [{"id": item["id"], "email": item["email"]} for item in data]

    # Write to output file as JSON array
    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(result, outfile, indent=2)

    print(f"✅ Extracted {len(result)} items and saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
