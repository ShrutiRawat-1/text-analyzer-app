from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ask(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(e)
        return None

def ner(text):
    return ask(f'''Do named entity recognition on the text below.
Group the entities by type. Choose the types yourself.
Use exactly this format with a blank line between groups:

TYPE: entity 1, entity 2, entity 3

Text: {text}''')

def sentiment(text):
    return ask(f'''What is the sentiment of the text below?
Reply with one word: Positive, Negative or Neutral.

Text: {text}''')

def detect_language(text):
    return ask(f'''What language is the text below written in?
Reply with only the language name.

Text: {text}''')
