import generate_conv

def classify(email):
    prompt = f"""
    You have to classify the following email into one of the four categoies: Spam, Work, Personal and Promotions.
    The email is as follows:
    {email}
    Just return a single word as a classification from the above options
    """
    response = generate_conv.llm1.complete(prompt)
    return response.text.strip()

example = "Dear [Hiring Manager Name],\n\nI am writing to formally accept the internship offer for the [Internship Title] position at [Company Name]. I am very pleased and grateful for the opportunity.\n\nThank you for extending this offer and for your time during the interview process. I am enthusiastic about the prospect of contributing to [Company Name] and gaining valuable experience in [Industry/Specific Area].\n\nI am eager to begin on [Start Date] and am available to discuss any onboarding requirements or necessary paperwork at your earliest convenience.\n\nThank you again for this wonderful opportunity.\n\nSincerely,\n\n[Student Name]"
print(classify(example))
