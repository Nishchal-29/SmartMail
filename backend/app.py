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

from compose import generate_email_from_prompt
from craftResponse import generate_crafted_response
from summary import get_summary

app = FastAPI()

# Enable CORS for frontend (adjust domain as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======== Models ========
class PromptRequest(BaseModel):
    prompt: str

class SmartReplyRequest(BaseModel):
    prompt: str            # The original email body
    user_prompt: str = ""  # Optional user guidance

class EmailBody(BaseModel):
    body: str

# ======== Endpoints ========

# ✨ Compose new email from prompt
@app.post("/compose-email")
def compose_email_handler(data: PromptRequest):
    return {
        "response": generate_email_from_prompt(data.prompt)
    }

# 💬 Smart reply to received email
@app.post("/smart-reply")
def smart_reply_handler(data: SmartReplyRequest):
    return {
        "response": generate_crafted_response(
            email_scenario=data.prompt,
            user_prompt=data.user_prompt if data.user_prompt else None
        )
    }

# 📝 Summarize email content
@app.post("/simplify")
def simplify_email(data: EmailBody):
    return {
        "summary": get_summary(data.body)
    }