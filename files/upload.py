from enum import Enum
import os

class StatusType(str, Enum):
  WEBSITE=1
  OFFLINE=2
    

def upload_post(type: StatusType, blog_text, website_url ="", login="", password=""):
  if type == StatusType.WEBSITE:
    wp_upload(blog_text, website_url, login, password)
    
  elif type == StatusType.OFFLINE:
    txt_upload(blog_text)


def wp_upload(blog_text, website_url, login, password):
  # upload to wordpress
  pass


def txt_upload(blog_text):
  # upload to text document + download
  i = 0
  while os.path.exists("text/blog%s.txt" %i):
    i += 1

  with open('text/blog%s.txt' %i, 'w') as f:
    f.write(blog_text)

  