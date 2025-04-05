import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

llm1 = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)
# email_parameters = input("Enter the parameters for the input of the email.")
email_parameters = "I am User123 asking my boss to reschedule the meeting to thursday 2pm. My boss is boss123. He was organizing meeting earlier on 3pm wednesday. The tone should be formal and polite. the email should be 75 to 100 words long. My email address is testuser123@gmail.com and my boss email id is testboss123@gmail.com"
prompt1 = f"""
Just Generate me a email using the following parameters, without any other text. The email should be in the same tone as the parameters or it should satisfy the conditions of the parameters:
{email_parameters}
""" 
response1 = llm1.complete(prompt1)
# print(response1)

def extract_email_components(raw_email: str) -> tuple:
    lines = raw_email.strip().splitlines()

    # Find the subject line
    subject = ""
    body_lines = []
    subject_found = False
    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line[len("Subject:"):].strip()
            subject_found = True
        elif subject_found:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    return (subject, body)

pair = extract_email_components(response1.text.strip())
print(pair)