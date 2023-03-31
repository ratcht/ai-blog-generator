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
  script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
  #rel_path = "files/text/saves.json"
  #abs_file_path = os.path.join(script_dir, rel_path)
  # upload to text document + download
  i = 0
  while os.path.exists(os.path.join(script_dir, "text/blog%s.txt") %i):
    i += 1

  with open(os.path.join(script_dir, "text/blog%s.txt") %i, 'w') as f:
    f.write(blog_text)

  