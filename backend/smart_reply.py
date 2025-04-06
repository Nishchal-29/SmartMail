# # smart_reply.py

# from compose import llm

# def generate_smart_reply(original_email: str) -> str:
#     prompt = f"""
# You're an assistant that helps users draft smart, polite and efficient replies to emails.

# Reply appropriately to the email below:
# \"\"\"
# {original_email}
# \"\"\"

# Response:
# """
#     response = llm.complete(prompt)
#     return response.text.strip()