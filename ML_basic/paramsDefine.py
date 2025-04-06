import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
load_dotenv()

llm1 = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)
llm2 = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key="AIzaSyCCOqMyckUorwYE1ZB7swdayyplgTPlTdw"
)

def get_top_phrases(email_responses, ngram_range=(2, 3), top_k=10):
    vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words='english')
    X = vectorizer.fit_transform(email_responses)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    sorted_phrases = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return sorted_phrases[:top_k]

def get_tone(email, response):
    prompt = f"""
    Categorize the tone of the response of the email into one or more of the following categories: Formal, Polite, Friendly, Assertive, Apologetic, Urgent, Grateful, Neutral or Encouraging. Return a list of categories separated by commas. The tone should be only from the list of categories. Do not include any other text in the response.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm2.complete(prompt)
    return response.text.strip()

def get_negotiation(email, response):
    prompt = f"""
    Categorize the Negotiation Style of the response of the email into one or more of the following categories: Cooperative, Compromising, Assertive, Passive, Aggressive, Dismissive, Persuasive, Indirect, Empathetic or Resistant. Return a list of categories separated by commas. The negotiation style should be only from the list of categories. Do not include any other text in the response.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm1.complete(prompt)
    return response.text.strip()


#Improve this:
def get_category(email, response):
    prompt = f"""
    Categorize the email and response into one or more of the following categories: Professional, Promotional, Informational, Transactional, Complaint, Inquiry, Feedback, Apology or Request. Return a list of categories separated by commas. The category should be only from the list of categories. Do not include any other text in the response.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm2.complete(prompt)
    return response.text.strip()
