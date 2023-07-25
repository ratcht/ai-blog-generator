from files.gptapi import generate_text_by_keywords, generate_text_by_title, generate_text_by_placeholder
from files.upload import StatusType, upload_post
import time
import random
from enum import Enum
import logging
import json
import re

class Language(str, Enum):
  ENGLISH="English"
  GERMAN="German"
  FRENCH="French"
  SPANISH="Spanish"


class ProjectType(str, Enum):
  TITLES="By Title"
  KEYWORDS="By Keywords"
  PLACEHOLDER="By Placeholder"

def find_longest_list_len(list_a, list_b, list_c, list_d):
  base_list=[list_a, list_b, list_c, list_d]
  return len(max(base_list, key=len))


class Project:
  def __init__(self, name, project_type:ProjectType,post_delay, language:Language, min_word_count=250, blog_text="", slug="post"):
    self.name = name
    self.project_type=project_type
    self.post_delay=post_delay
    self.language = language
    self.blog_text=blog_text
    self.on = False
    self.general_statement=""
    self.fill_blanks=[]
    self.keywords_dynamic=[]
    self.titles=[]
    self.general_prompt=""
    self.general_title = ""
    self.keywords_a=[]
    self.keywords_b=[]
    self.keywords_c=[]
    self.keywords_d=[]

    self.min_word_count=min_word_count
    self.slug = slug
  

  def update_as_keywords(self, name,general_statement, fill_blanks, keywords_dynamic, slug):
    self.name=name
    self.slug=slug
    self.general_statement=general_statement
    self.fill_blanks=fill_blanks
    self.keywords_dynamic=keywords_dynamic


  def update_as_titles(self,name, titles, slug):
    self.name=name
    self.slug=slug
    self.titles = titles

  def update_as_placeholders(self, name, general_prompt, general_title, keywords_a, keywords_b, keywords_c, keywords_d, keywords_dynamic, slug):
    self.name=name
    self.slug=slug
    self.general_prompt=general_prompt
    self.general_title=general_title
    self.keywords_a=keywords_a
    self.keywords_b=keywords_b
    self.keywords_c=keywords_c
    self.keywords_d=keywords_d
    self.keywords_dynamic=keywords_dynamic

  def create_post_by_title(self, title):
    self.blog_text = generate_text_by_title(title, self.language.value, self.min_word_count)

  def create_post_by_keywords(self, general_statement, fill_blank, keywords):
    self.blog_text = generate_text_by_keywords(general_statement, fill_blank, keywords, self.language.value, self.min_word_count)

  def create_post_by_placeholder(self, general_prompt, placeholder_list, keywords):
    self.blog_text = generate_text_by_placeholder(general_prompt, placeholder_list, keywords, self.language.value, self.min_word_count)


  def generate_periodic(self, status_type ,website_url="", login="", password=""):
    if self.project_type==ProjectType.KEYWORDS:
      for fill_blank in self.fill_blanks:
        self.create_post_by_keywords(self.general_statement, fill_blank, (', ').join(self.keywords_dynamic))
        print("GPT Done!")
        upload_post(status_type, self.general_statement+" "+fill_blank, self.blog_text, website_url, login, password, self.slug)
        time.sleep(self.post_delay)

    elif self.project_type==ProjectType.TITLES:
      for title in self.titles:
        self.create_post_by_title(title)
        print("GPT Done!")
        upload_post(status_type, title, self.blog_text, website_url, login, password, self.slug)
        time.sleep(self.post_delay)

    elif self.project_type==ProjectType.PLACEHOLDER:
      upper = find_longest_list_len(self.keywords_a, self.keywords_b,self.keywords_c,self.keywords_d)
      for i in range(0,upper):
        keyword_a = self.keywords_a[i] if i < len(self.keywords_a) else self.keywords_a[len(self.keywords_a)-1]
        keyword_b = self.keywords_b[i] if i < len(self.keywords_b) else self.keywords_b[len(self.keywords_b)-1]
        keyword_c = self.keywords_c[i] if i < len(self.keywords_c) else self.keywords_c[len(self.keywords_c)-1]
        keyword_d = self.keywords_d[i] if i < len(self.keywords_d) else self.keywords_d[len(self.keywords_d)-1]
        placeholder_list = [keyword_a,keyword_b,keyword_c,keyword_d]
        self.create_post_by_placeholder(self.general_prompt, placeholder_list, (', ').join(self.keywords_dynamic))
        print("GPT Done!")

        # generate title
        title = re.sub("\[a\]", placeholder_list[0], self.general_title)
        title = re.sub("\[b\]", placeholder_list[1], title)
        title = re.sub("\[c\]", placeholder_list[2], title)
        title = re.sub("\[d\]", placeholder_list[3], title)

        upload_post(status_type, title, self.blog_text, website_url, login, password, self.slug)
        time.sleep(self.post_delay)
    logging.info("Completed!")

  def jsonify(self):
    return dict(name = self.name, project_type=self.project_type,post_delay=self.post_delay, language = self.language, min_word_count=self.min_word_count , blog_text=self.blog_text, on = self.on, general_statement=self.general_statement, 
                fill_blanks=self.fill_blanks, general_title=self.general_title,keywords_dynamic=self.keywords_dynamic,titles=self.titles, slug=self.slug, keywords_a=self.keywords_a, keywords_b=self.keywords_b, keywords_c=self.keywords_c, keywords_d=self.keywords_d, general_prompt=self.general_prompt)


class Website:
  def __init__(self, status_type: StatusType, website_url, login, password):
    self.status_type = status_type
    self.website_url=website_url
    self.login = login
    self.password = password
    self.projects = []

  def jsonify(self):
    return dict(status_type = self.status_type, website_url=self.website_url, login=self.login, password=self.password, projects=self.projects) 
 
  def get_projects(self):
    return self.projects

  def add_project(self, project):
    self.projects.append(project)

class ComplexEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj,'jsonify'):
      return obj.jsonify()
    else:
      return json.JSONEncoder.default(self, obj)


def parse_project(json_obj):
  project = Project(json_obj["name"], ProjectType(json_obj["project_type"]), json_obj["post_delay"], Language(json_obj["language"]), int(json_obj["min_word_count"]), json_obj["blog_text"], json_obj["slug"])
  project.keywords_dynamic=json_obj["keywords_dynamic"]
  project.general_statement=json_obj["general_statement"]
  project.general_prompt=json_obj["general_prompt"]

  project.keywords_a=json_obj["keywords_a"]
  project.keywords_b=json_obj["keywords_b"]
  project.keywords_c=json_obj["keywords_c"]
  project.keywords_d=json_obj["keywords_d"]

  project.general_title=json_obj["general_title"]
  project.fill_blanks=json_obj["fill_blanks"]
  project.titles=json_obj["titles"]
  return project

def save_websites(websites, file_path):
  with open(file_path, "w") as json_file:
    json_file.write(json.dumps(websites, cls=ComplexEncoder))




def load_websites(file_path):
  websites = []
  print(file_path)
  with open(file_path) as _file:
    json_data = json.load(_file)
    for site in json_data:
      website_to_add = Website(site["status_type"], site["website_url"], site["login"], site["password"])
      for project in site['projects']:
        website_to_add.add_project(parse_project(project))
      websites.append(website_to_add)
  return websites

