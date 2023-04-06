from enum import Enum
import os
import base64
import requests

class StatusType(str, Enum):
  WEBSITE=1
  OFFLINE=2
    

def upload_post(type: StatusType, name, blog_text, website_url ="", login="", password="", slug="posts"):
  if type == StatusType.WEBSITE:
    wp_upload(name, blog_text, website_url, login, password,slug)
    
  elif type == StatusType.OFFLINE:
    txt_upload(blog_text)


def wp_upload(name, blog_text, website_url, login, password, slug):
  print("Waiting for WP")
  # username="chatgpt2023"
  # password="syr7 2saN DGs8 2ktF NwFP frnJ"

  url = str(website_url)+"wp-json/wp/v2/"+slug
  print(url)
  credentials = login + ':' + password
  token = base64.b64encode(credentials.encode())
  header = {'Authorization': 'Basic ' + token.decode('utf-8')}
  # GET Request: 
  # response = requests.get(url , headers=header)

  post = {
  'title'    : name,
  'status'   : 'draft', 
  'content'  : blog_text,
  'categories': 5 # category ID
  }
  response = requests.post(url , headers=header, json=post)
  print("WP Upload!")


  


def txt_upload(blog_text):  
  print("TXT Upload!")
  script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
  #rel_path = "files/text/saves.json"
  #abs_file_path = os.path.join(script_dir, rel_path)
  # upload to text document + download
 # print(os.getcwd())
  i = 0
  while os.path.exists(os.path.join(os.getcwd(), "text/blog%s.txt") %i):
    i += 1

  with open(os.path.join(os.getcwd(), "text/blog%s.txt") %i, 'w') as f:
    f.write(blog_text)

  