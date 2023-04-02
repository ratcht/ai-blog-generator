from dotenv import load_dotenv
import openai
import os

#Load env vars
load_dotenv()

api_key = os.environ.get('GPT_API_KEY')

#authenticate openai
openai.api_key = api_key


def generate_text_by_keywords(topic: str, keywords: str, language: str, min_word_count: int):
  intro_word_count = 0.2*min_word_count
  body_word_count=0.6*min_word_count
  conclusion_word_count=0.2*min_word_count
  blog_intro = generate_text("Write the opening to a personal blog page about " + topic+ " that includes the keyword(s) (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must be around the word count: "+str(intro_word_count)+". You do not need to introduce the blog itself, just open the post. Do not say 'welcome to my blog'.")
  blog_body = generate_text("Write the body section of a personal blog for the introduction: '" +blog_intro +"'. The blog body must be about " + topic+ " that includes the keyword (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must meet the minimum word count: "+str(body_word_count))
  blog_conclusion = generate_text("Write the conclusion section of a personal blog, without saying 'in conclusion' or anything similar, for the introduction: '" +blog_intro +"'. The blog body must be about " + topic+ " that includes the keyword (but is not soley focused on): " + keywords+ ". The blog must be in the language: " + language+". The blog must meet the minimum word count: "+str(conclusion_word_count))

  return blog_intro+'\n'+blog_body+'\n'+blog_conclusion

def generate_text_by_title(title: str, language: str):
  return generate_text("Write a personal blog with 1 or 2 headers (but not titled header) on the title " + title+ " in the language: " + language).content


def generate_text(content):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a blog writer. You have a nice personal touch on your writings and share your own opinions fluidly"},
        {"role": "user", "content": content}
      ]
  )
  return response['choices'][0]['message']['content']

