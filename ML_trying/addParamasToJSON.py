import generate_conv
import json
import time
with open("./hackfest/new.json", "r") as f:
    data = json.load(f)
count = 0
# try:
for item in data:
    count += 1
    print(f"Count is {count}")
    time.sleep(10)
    email = item['email']
    response = item['response']
    item['metadata'] = {
        "formality": generate_conv.get_formality(email, response),
        "tone": generate_conv.get_tone(email, response),
        "category":generate_conv.get_category(email, response),
        "negotiation_style":generate_conv.get_negotiation(email, response),
        "top_phrases":generate_conv.get_top_phrases([response])
    }
# # except Exception as e:
with open("./hackfest/modified.json", "w") as f:
    json.dump(data, f, indent=2)
# # else:



# import generate_conv
# import json
# import time
# import os

# # Paths
# input_path = "./hackfest/new.json"
# output_path = "./hackfest/modified.json"

# # Load input
# with open(input_path, "r") as f:
#     data = json.load(f)

# # Load existing output if any
# if os.path.exists(output_path):
#     with open(output_path, "r") as f:
#         modified_data = json.load(f)
#     processed_ids = {item['id'] for item in modified_data if 'id' in item}
# else:
#     modified_data = []
#     processed_ids = set()

# count = 0
# for item in data:
#     # Optional: skip if already processed (based on ID or hash of email-response)
#     item_id = item.get('id') or hash(item['email'] + item['response'])
#     if str(item_id) in processed_ids:
#         continue

#     try:
#         count += 1
#         print(f"Processing item {count}...")

#         # Slow down to avoid rate limits
#         time.sleep(10)

#         email = item['email']
#         response = item['response']

#         # Add metadata
#         item['metadata'] = {
#             "formality": generate_conv.get_formality(email, response),
#             "tone": generate_conv.get_tone(email, response),
#             "category": generate_conv.get_category(email, response),
#             "negotiation_style": generate_conv.get_negotiation(email, response),
#             "top_phrases": generate_conv.get_top_phrases([response])
#         }

#         # Add ID if not present
#         item['id'] = str(item_id)

#         # Save to output list
#         modified_data.append(item)
#         processed_ids.add(str(item_id))

#         # Save immediately after every successful entry
#         with open(output_path, "w") as f:
#             json.dump(modified_data, f, indent=2)

#     except Exception as e:
#         print(f" Error at count {count}: {e}")
#         continue
