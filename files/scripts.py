from files.gptapi import generate_text_by_keywords, generate_text_by_title
from files.upload import StatusType, upload_post
import time
import random
from enum import Enum
import json


class Language(str, Enum):
  ENGLISH="English"
  GERMAN="German"
  FRENCH="French"
  SPANISH="Spanish"


class ProjectType(str, Enum):
  TITLES="By Title"
  KEYWORDS="By Keywords"

class Project:
  def __init__(self, name, status_type: StatusType, project_type:ProjectType,post_delay, language:Language, min_word_count=250, blog_text=""):
    self.name = name
    self.status_type = status_type
    self.project_type=project_type
    self.post_delay=post_delay
    self.language = language
    self.blog_text=blog_text
    self.on = False
    self.topic=""
    self.keywords_dynamic=[]
    self.titles=[]
    self.min_word_count=min_word_count
  
  def create_post_by_title(self, title):
    print("Waiting for GPT")
    self.blog_text = generate_text_by_title(title, self.language.value, self.min_word_count)

  def create_post_by_keywords(self, topic, keywords):
    print("Waiting for GPT")
    self.blog_text = generate_text_by_keywords(topic, keywords, self.language.value, self.min_word_count)

  def generate_periodic(self, website_url="", login="", password=""):
    if self.project_type==ProjectType.KEYWORDS:
      for keyword in self.keywords_dynamic:
        self.create_post_by_keywords(self.topic, keyword)
        upload_post(StatusType.OFFLINE, self.blog_text, website_url, login, password)

        time.sleep(self.post_delay)

    elif self.project_type==ProjectType.TITLES:
      for title in self.titles:
        self.create_post_by_title(title)
        upload_post(self.status_type, self.blog_text, website_url, login, password)

        time.sleep(self.post_delay)

  def jsonify(self):
    return dict(name = self.name, status_type = self.status_type, project_type=self.project_type,post_delay=self.post_delay, language = self.language, blog_text=self.blog_text, on = self.on, topic=self.topic, 
                keywords_dynamic=self.keywords_dynamic,titles=self.titles)


class Website:
  def __init__(self, website_url, login, password, projects=[]):
    self.website_url=website_url
    self.login = login
    self.password = password
    self.projects = projects

  def add_project(self, name, status_type: StatusType, project_type: ProjectType, post_delay, language:Language):
    self.projects.append(Project(name, status_type, project_type, post_delay, language))

  def jsonify(self):
    return dict(website_url=self.website_url, login=self.login, password=self.password, projects=self.projects) 

class ComplexEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj,'jsonify'):
      return obj.jsonify()
    else:
      return json.JSONEncoder.default(self, obj)


def parse_project(json_obj):
  return Project(json_obj["name"], StatusType(json_obj["status_type"]), ProjectType(json_obj["project_type"]), json_obj["post_delay"], Language(json_obj["language"]), json_obj["min_word_count"], json_obj["blog_text"])

def save_websites(websites, file_path):
  with open(file_path, "w") as json_file:
    json_file.write(json.dumps(websites, cls=ComplexEncoder))

def load_websites(file_path):
  websites = []
  _file = open(file_path)
  json_data = json.load(_file)
  for site in json_data:
    projects =[]
    for proj in site["projects"]:
      projects.append(parse_project(proj))
    websites.append(Website(site["website_url"], site["login"], site["password"], projects))
  return websites

