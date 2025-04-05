import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from llama_index.core import Settings
from llama_index.llms.google_genai import GoogleGenAI
load_dotenv()

llm = GoogleGenAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)


#dont use, this is just for testing
def generate_conversation(email_parameters, response_parameters=None, email_formality=0.6, response_formality=0.4):
    prompt1 = f"""
    Just Generate me a email using the following parameters, without any other text. The formality of the email should be {email_formality}, where formality scale is of 0.0 to 1.0, where 0.0 is very informal and 1.0 is very formal. The email should be in the same tone as the parameters.:
    {email_parameters}
    """ 
    response1 = llm.complete(prompt1)
    email =  response1.text.strip()
    if response_parameters is not None:
        prompt2 = f"""
        For the given email, plese generate a response to the email. The response should also contain a suitable Subject. Do not include any other text in the response, except the response. The formality of the response should be {response_formality}, where formality scale is of 0.0 to 1.0, where 0.0 is very informal and 1.0 is very formal.
        The email is as follows:
        {email}
        Generate the response to the email using the following parameters:
        {response_parameters}
        """
        response2 = llm.complete(prompt2)
        response = response2.text.strip()
        return email, response
    else:
        return email, None

def get_formality(email, response):
    prompt = f"""
    For the given conversation, please rate the formality on a scale of 0.0 to 1.0, where 0.0 is very informal and 1.0 is very formal. Just return a single float value.
    The conversation is as follows:
    {email}

    The response is:
    {response}
    """
    response = llm.complete(prompt)
    this_num = float(response.text.split()[0])
    return this_num


#Dont use:
def get_conciseness(email, response):
    prompt = f"""
    For the given conversation, please rate the conciseness of the response on a scale of 0.0 to 1.0, where 0.0 is very verbose and 1.0 is very concise. Just return a single float value.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm.complete(prompt)
    this_num = float(response.text.split()[0])
    return this_num


def get_top_phrases(email_responses, ngram_range=(2, 3), top_k=10):
    vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words='english')
    X = vectorizer.fit_transform(email_responses)
    sum_words = X.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    sorted_phrases = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return sorted_phrases[:top_k]

def get_tone(email, response):
    prompt = f"""
    Categorize the tone of the response of the email into one or more of the following categories: Formal, Informal, Polite, Friendly, Assertive, Apologetic, Urgent, Grateful, Neutral or Encouraging. Return a list of categories separated by commas. The tone should be only from the list of categories. Do not include any other text in the response.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm.complete(prompt)
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
    response = llm.complete(prompt)
    return response.text.strip()


#Improve this:
def get_category(email, response):
    prompt = f"""
    Categorize the email and response into one or more of the following categories: Personal, Professional, Promotional, Informational, Transactional, Complaint, Inquiry, Feedback or Apology. Return a list of categories separated by commas. The category should be only from the list of categories. Do not include any other text in the response.
    The conversation is as follows:
    Email:
    {email}

    The response is:
    {response}
    """
    response = llm.complete(prompt)
    return response.text.strip()



#This function is to calculate EMA. It will be helpful in getting the formality scores of the user across different categories and email-response pairs.
def update_ema(old_score, new_score, alpha):
    return old_score * (1 - alpha) + new_score * alpha

# email, response = generate_conversation("A friendly email to a friend asking about their weekend plans with a formality score of 0.23 where formality scale is of 0.0 to 1.0, where 0.0 is very informal and 1.0 is very formal")
# print("Email: ", email)
# print("Response: ", response)
# print("Formality Score: ", get_formality(email, response))

# email2, response2 = generate_conversation("The email is about a promotional deal about a product", "However, in response the user is not interested in the product and is angry about the spam email")

# print("Email: ", email2)
# print("Response: ", response2)
# print("Formality Score: ", get_formality(email2, response2))
# print(get_top_phrases([email2, response2], ngram_range=(2, 3), top_k=10))
# print(get_tone(email2, response2))
# print(get_negotiation(email2, response2))


# email3, response3 = generate_conversation("A friendly email to a friend asking about their weekend plans. The response should be around 75 to 100 words long")
# print("Email: ", email3)
# print("Response: ", response3)

# print(get_top_phrases([email3, response3], ngram_range=(2, 3), top_k=10))
# print(get_tone(email3, response3))




# email4, response4 = generate_conversation("An email from the manager about changes in plans for the project. The response should be around 150-200 words long. The body should not be very concise and could be a little bit verbose.")
# print("Email: ", email4)
# print("Response: ", response4)
