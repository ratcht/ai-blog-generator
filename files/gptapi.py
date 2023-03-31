from dotenv import load_dotenv
import openai
import os

#Load env vars
load_dotenv()

api_key = os.environ.get('GPT_API_KEY')

#authenticate openai
openai.api_key = api_key


def generate_text_by_keywords(topic: str, keywords: str, language: str):
  return generate_text("Write a personal blog with a few short headers about " + topic+ " that includes the keyword (but is not soley focused on): " + keywords+ ". The post must be in the language: " + language)


def generate_text_by_title(title: str, language: str):
  return generate_text("Write a personal blog with a few short headers on the title " + title+ " in the language: " + language).content


def generate_text(content):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a blog writer. You have a nice personal touch on your writings and share your own opinions fluidly"},
        {"role": "user", "content": content}
      ]
  )
  return response['choices'][0]['message']['content']