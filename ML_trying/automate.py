import generate_conv
import json
import os

def get_pairs(email_params_list, response_params_list, email_formality_list, response_formality_list):
    all_pairs = []
    for i in range(len(email_params_list)):
        print(f"Entered the loop for {i+1}th time")
        email_parameters = email_params_list[i]
        response_parameters = response_params_list[i]
        email_formality = email_formality_list[i]
        response_formality = response_formality_list[i]
        email, response = generate_conv.generate_conversation(email_parameters, response_parameters=response_parameters,email_formality=email_formality,response_formality=response_formality)
        this = {
            "email": email,
            "response": response
        }
        all_pairs.append(this)
    return all_pairs

def save_pairs_to_json(pairs, filename="./hackfest/email_response_pairs.json"):
    # Check if file exists
    if os.path.exists(filename):
        with open(filename, "r") as alpha:
            existing = json.load(alpha)
    else:
        existing = []

    # Append new ones
    existing.extend(pairs)

    # Save back
    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)

# email_params_list = ["This email is about promotion from a company about a laptop","This email is from a friend asking about hangout dates","This email is about meeting reschedule dates from the manager"]
# response_params_list = ["In response, the user is angry for spam and does not like it","In response to this email, the user arranges some dates for hangouts","In response, the user confirms the dates and will be there at the meeting"]
# pairs = get_pairs(email_params_list,response_params_list)
# save_pairs_to_json(pairs, filename="./hackfest/this.json")

count = 0
this = 1
print("Write the parameters for email and response pair")
email_params_list= []
response_params_list=[]
email_formality_list = []
response_formality_list=[]
while(this):
    count +=1
    print("Enter the prompt for email\n")
    email_prompt = input()
    print("Enter the prompt for corresponding response:\n")
    response_prompt = input()
    print("Enter formality for email\n")
    email_formality = float(input())/10
    print("Enter formality for email\n")
    response_fomality = float(input())/10
    email_params_list.append(email_prompt)
    response_params_list.append(response_prompt)
    email_formality_list.append(email_formality)
    response_formality_list.append(response_fomality)
    this = input("\nMore?")
    this = True if this == 'y' else False
pairs =get_pairs(email_params_list, response_params_list=response_params_list, email_formality_list=email_formality_list, response_formality_list=email_formality_list)
save_pairs_to_json(pairs, filename="./hackfest/this.json")
print(f"Saved {count} pairs to json")
