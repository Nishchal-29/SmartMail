# # import os
# # from dotenv import load_dotenv # type: ignore

# # from llama_index.core import Settings # type: ignore
# # from llama_index.llms.google_genai import GoogleGenAI # type: ignore
# # load_dotenv()

# # llm = GoogleGenAI(
# #     model="gemini-2.0-flash",
# #     api_key=os.environ["GOOGLE_API_KEY"]
# # )
# # def get_summary(email):
# #     prompt = f"""
# #     You are an AI assistant that helps users quickly understand emails.

# #     Summarize the following email in a clear, concise, and easy-to-skim format.
# #     If the email contains tasks, requests, or meeting details, include them clearly.
# #     Avoid repeating greetings or signatures.
# #     Use bullet points only if multiple points are present.

# #     Email:
# #     \"\"\"
# #     {email}
# #     \"\"\"

# #     Summary:
# #     """ 
# #     response = llm.complete(prompt)
# #     summary = response.text.strip()
# #     return summary


# # email_text1 = """
# # Subject: Project Chimera - Slight Pivot

# # Team,

# # Quick update on Project Chimera. We've had a bit of a rethink based on some new intel that's come to light. Basically, market analysis suggests focusing on Feature A is going to give us a bigger bang for our buck than Feature B in the initial launch.

# # So, we're shifting gears slightly. I know, I know, change is annoying. But trust me on this one. It's about maximizing impact and getting the best possible ROI.

# # We'll be re-prioritizing tasks accordingly. Sarah, can you please start re-allocating resources to Feature A? John, I need you to put Feature B on the back burner for now.

# # I've scheduled a quick meeting tomorrow at 10 AM to discuss the specifics and answer any questions. Come prepared to brainstorm how we can make this pivot as smooth as possible.

# # Let's make this work.

# # Best,

# # [Manager's Name]
# # Response:  None
# # """
# # email_text2 = """
# # Subject: Project Chimera - Slight Course Correction

# # Team,

# # Hope you're all having a productive week.

# # Right, so, about Project Chimera. As you know, we've been pushing hard towards the initial objectives, and frankly, the progress has been commendable. However, after a rather lengthy (and, dare I say, somewhat draining) meeting with the higher-ups this morning, we've had to make a few… adjustments.

# # Essentially, the market analysis we were working from has been updated with some, shall we say, *interesting* new data. This necessitates a slight pivot in our strategy. Specifically, we're going to be shifting our focus slightly away from Feature A and allocating more resources to Feature B. I know, I know, we've all put a lot of effort into Feature A, but trust me on this one, Feature B is where the real potential lies, at least according to the latest projections.

# # I'll be scheduling a brief meeting tomorrow afternoon to discuss these changes in more detail and answer any questions you might have. In the meantime, please hold off on any further work on Feature A. Let's make this transition as smooth as possible.

# # Thanks for your understanding and continued dedication.

# # Best,

# # [Manager's Name]
# # """

# # print(get_summary(email_text2))

# # import os
# # from dotenv import load_dotenv

# # from llama_index.llms.google_genai import GoogleGenAI

# # # Load environment variables from .env file
# # load_dotenv()

# # # Initialize Google Gemini via LlamaIndex
# # llm = GoogleGenAI(
# #     model="gemini-1.5-flash",  # or "gemini-1.0-pro"
# #     api_key=os.getenv("GOOGLE_API_KEY")
# # )

# # def get_summary(email):
# #     """
# #     Summarizes a given email using Gemini AI.
# #     """
# #     prompt = f"""
# # You are an AI assistant that helps users quickly understand emails.

# # Summarize the following email in a clear, concise, and easy-to-skim format.
# # If the email contains tasks, requests, or meeting details, include them clearly.
# # Avoid repeating greetings or signatures.
# # Use bullet points only if multiple points are present.

# # Email:
# # \"\"\"
# # {email}
# # \"\"\"

# # Summary:
# # """
# #     response = llm.complete(prompt)
# #     return response.text.strip()


# # def generate_email_from_prompt(user_prompt):
# #     """
# #     Generates an email subject and body based on a natural language prompt.
# #     Returns a dictionary with 'subject' and 'body'.
# #     """
# #     instruction = f"""
# # You are a smart email assistant.

# # Based on the following instruction, generate:
# # - A professional subject line
# # - A clear and appropriate email body (no HTML)

# # User Prompt:
# # \"\"\"
# # {user_prompt}
# # \"\"\"

# # Respond only in this exact JSON format:
# # {{
# #   "subject": "...",
# #   "body": "..."
# # }}
# # """
# #     response = llm.complete(instruction)

# #     # Extract JSON safely
# #     import re, json
# #     match = re.search(r"\{.*\}", response.text, re.DOTALL)
# #     try:
# #         return json.loads(match.group()) if match else {"subject": "", "body": ""}
# #     except Exception as e:
# #         print("AI response parsing failed:", e)
# #         return {"subject": "", "body": ""}

# # # def generate_email_from_prompt(email_to_reply_to):
# # #     instruction = f"""
# # # You are an AI assistant that writes professional email replies.

# # # Below is an incoming email. Your task is to write a polite, thoughtful, and contextually relevant REPLY to this email.

# # # Be concise but complete. Respond as a human professional would. DO NOT repeat the original email or restate obvious details.

# # # Respond in JSON format only like this:
# # # {{
# # #   "subject": "RE: [copied subject, or relevant short reply subject]",
# # #   "body": "..."
# # # }}

# # # Incoming Email:
# # # \"\"\"
# # # {email_to_reply_to}
# # # \"\"\"
# # # """
# # #     response = llm.complete(instruction)

# # #     print("LLM Raw Response:", response.text)

# # #     import re, json
# # #     match = re.search(r"\{.*\}", response.text, re.DOTALL)
# # #     try:
# # #         return json.loads(match.group()) if match else {"subject": "", "body": ""}
# # #     except Exception as e:
# # #         print("AI response parsing failed:", e)
# # #         return {"subject": "", "body": ""}

# import os
# import json
# import re
# from dotenv import load_dotenv
# from llama_index.llms.google_genai import GoogleGenAI

# # Load environment variables
# load_dotenv()

# # Initialize Gemini LLM (default/basic usage)
# llm = GoogleGenAI(
#     model="gemini-1.5-flash",
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# # ========== 1. Simplify Email ==========
# def get_summary(email):
#     prompt = f"""
# You are an AI assistant that helps users quickly understand emails.

# Summarize the following email in a clear, concise, and easy-to-skim format.
# If the email contains tasks, requests, or meeting details, include them clearly.
# Avoid repeating greetings or signatures.
# Use bullet points only if multiple points are present.

# Email:
# \"\"\"
# {email}
# \"\"\"

# Summary:
# """
#     response = llm.complete(prompt)
#     return response.text.strip()


# # ========== 2. Generate Email From Prompt ==========
# def generate_email_from_prompt(user_prompt):
#     instruction = f"""
# You are a smart email assistant.

# Based on the following instruction, generate:
# - A professional subject line
# - A clear and appropriate email body (no HTML)

# User Prompt:
# \"\"\"
# {user_prompt}
# \"\"\"

# Respond only in this exact JSON format:
# {{
#   "subject": "...",
#   "body": "..."
# }}
# """
#     response = llm.complete(instruction)
#     print("LLM Response:", response.text)

#     match = re.search(r"\{.*\}", response.text, re.DOTALL)
#     try:
#         return json.loads(match.group()) if match else {"subject": "", "body": ""}
#     except Exception as e:
#         print("AI response parsing failed:", e)
#         return {"subject": "", "body": ""}


# # ========== 3. Generate Email with Company Context ==========
# def generate_crafted_response(user_prompt: str) -> str:
#     from pinecone import Pinecone
#     from llama_index.core import Settings, VectorStoreIndex
#     from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
#     from llama_index.llms.google_genai import GoogleGenAI
#     from llama_index.vector_stores.pinecone import PineconeVectorStore

#     # Load envs again if running standalone
#     load_dotenv()

#     pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
#     pinecone_index = pinecone_client.Index("first")
#     embed_model = GoogleGenAIEmbedding(model_name='models/embedding-001')
#     enhanced_llm = GoogleGenAI(
#         model="gemini-2.0-flash",
#         api_key=os.environ["GOOGLE_API_KEY"]
#     )

#     # Set up LlamaIndex
#     Settings.embed_model = embed_model
#     Settings.llm = enhanced_llm

#     # Step 1: Treat user prompt as the scenario
#     email_scenario = user_prompt

#     # Step 2: Fetch relevant company rules from Pinecone
#     vector_store1 = PineconeVectorStore(pinecone_index=pinecone_index, namespace='companyrules2')
#     index1 = VectorStoreIndex.from_vector_store(
#         vector_store=vector_store1,
#         embed_model=embed_model
#     )
#     query_engine1 = index1.as_query_engine(similarity_top_k=3)
#     rule_context = query_engine1.query(email_scenario)

#     # Step 3: Load user profile
#     with open("hackfest/new/userProfile.json", "r") as f:
#         user_data = json.load(f)
#     user_profile = user_data["user1"]

#     # Extract user style
#     top_tone = max(user_profile["tone_profile"], key=user_profile["tone_profile"].get)
#     top_category = max(user_profile["category_profile"], key=user_profile["category_profile"].get)
#     conciseness_score = user_profile["avg_conciseness"]

#     if conciseness_score > 0.75:
#         concise_note = "The response should be concise and to the point."
#     elif conciseness_score > 0.5:
#         concise_note = "The response should maintain moderate detail and clarity."
#     else:
#         concise_note = "The response can be more descriptive and elaborate if necessary."

#     user_style_instruction = f"""
# Please write the email in a **{top_tone.lower()}** tone, suitable for a **{top_category.lower()}** communication scenario.
# {concise_note}
# """.strip()

#     # Step 4: Final prompt
#     final_prompt = f"""
# Generate a suitable email based on the following condition:

# {email_scenario}

# And based on the following company rules or guidelines:

# {rule_context}

# User style preferences:
# {user_style_instruction}
# Write a professional email response following all applicable company policies. Only give me email text and nothing else.
# Email:
# """.strip()

#     response = enhanced_llm.complete(final_prompt)
#     return response.text.strip()
# _________________________________________________________________________

import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()

llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

def get_summary(email):
    prompt = f"""
    You are an AI assistant that helps users quickly understand emails.

    Summarize the following email in a clear, concise, and easy-to-skim format.
    If the email contains tasks, requests, or meeting details, include them clearly.
    Avoid repeating greetings or signatures.
    Use bullet points only if multiple points are present. Keep the formatting into account.
    

    Email:
    \"\"\"
    {email}
    \"\"\"

    Summary:
    """ 
    response = llm.complete(prompt)
    summary = response.text.strip()
    return summary