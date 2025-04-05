import os
from dotenv import load_dotenv

from llama_index.core import Settings
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
    Use bullet points only if multiple points are present.

    Email:
    \"\"\"
    {email}
    \"\"\"

    Summary:
    """ 
    response = llm.complete(prompt)
    summary = response.text.strip()
    return summary


email_text1 = """
Subject: Project Chimera - Slight Pivot

Team,

Quick update on Project Chimera. We've had a bit of a rethink based on some new intel that's come to light. Basically, market analysis suggests focusing on Feature A is going to give us a bigger bang for our buck than Feature B in the initial launch.

So, we're shifting gears slightly. I know, I know, change is annoying. But trust me on this one. It's about maximizing impact and getting the best possible ROI.

We'll be re-prioritizing tasks accordingly. Sarah, can you please start re-allocating resources to Feature A? John, I need you to put Feature B on the back burner for now.

I've scheduled a quick meeting tomorrow at 10 AM to discuss the specifics and answer any questions. Come prepared to brainstorm how we can make this pivot as smooth as possible.

Let's make this work.

Best,

[Manager's Name]
Response:  None
"""
email_text2 = """
Subject: Project Chimera - Slight Course Correction

Team,

Hope you're all having a productive week.

Right, so, about Project Chimera. As you know, we've been pushing hard towards the initial objectives, and frankly, the progress has been commendable. However, after a rather lengthy (and, dare I say, somewhat draining) meeting with the higher-ups this morning, we've had to make a few… adjustments.

Essentially, the market analysis we were working from has been updated with some, shall we say, *interesting* new data. This necessitates a slight pivot in our strategy. Specifically, we're going to be shifting our focus slightly away from Feature A and allocating more resources to Feature B. I know, I know, we've all put a lot of effort into Feature A, but trust me on this one, Feature B is where the real potential lies, at least according to the latest projections.

I'll be scheduling a brief meeting tomorrow afternoon to discuss these changes in more detail and answer any questions you might have. In the meantime, please hold off on any further work on Feature A. Let's make this transition as smooth as possible.

Thanks for your understanding and continued dedication.

Best,

[Manager's Name]
"""

print(get_summary(email_text2))
