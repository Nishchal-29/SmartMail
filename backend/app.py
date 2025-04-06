# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

# from craftResponse import generate_crafted_response
# from compose import generate_email_from_prompt
# from summary import get_summary  # ✅ Make sure this exists

# app = FastAPI()

# # Enable CORS so frontend can talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # or ["*"] for testing
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ========================
# # 📩 EMAIL GENERATION
# # ========================
# class PromptRequest(BaseModel):
#     prompt: str

# @app.post("/craft-response")
# def craft_response_handler(data: PromptRequest):
#     result = generate_crafted_response(data.prompt)
#     return {"response": result}

# @app.post("/smart-reply")
# def smart_reply_handler(data: PromptRequest):
#     return {"response": generate_email_from_prompt(data.prompt)}


# # ========================
# # ✂️ EMAIL SUMMARY
# # ========================
# class EmailBody(BaseModel):
#     body: str

# @app.post("/simplify")
# def simplify_email(data: EmailBody):
#     summary = get_summary(data.body)
#     return {"summary": summary}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from summary import get_summary
from compose import generate_email_from_prompt  # For composing new emails
from craftResponse import generate_crafted_response  # For smart replies

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== Schemas ========
class PromptRequest(BaseModel):
    prompt: str

class EmailBody(BaseModel):
    body: str


# ======== Endpoints ========

# ✨ Compose from prompt (NEW EMAIL)
@app.post("/compose-email")
def compose_email_handler(data: PromptRequest):
    return {"response": generate_email_from_prompt(data.prompt)}

# 💬 Smart reply to an email
@app.post("/smart-reply")
def smart_reply_handler(data: PromptRequest):
    return {"response": generate_crafted_response(data.prompt)}

# ✂️ Summarize Email
@app.post("/simplify")
def simplify_email(data: EmailBody):
    summary = get_summary(data.body)
    return {"summary": summary}