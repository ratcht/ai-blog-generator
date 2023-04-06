import json
import os
from flask import Flask, redirect, url_for, render_template, request
from files.gptapi import generate_text
from files.scripts import Website, Project, load_websites, save_websites, StatusType, ProjectType, Language, ComplexEncoder
# import webbrowser
import sys

app = Flask(__name__)

def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "files/text/saves.json"
# abs_file_path = os.path.join(script_dir, rel_path)
abs_file_path = resource_path(rel_path)

# testpath = resource_path(rel_path)

websites = load_websites(abs_file_path)
# websites=[]


@app.route("/home")
@app.route("/", methods=["GET"])
def index():
  global websites
  return render_template("index.html", websites = websites)

@app.route("/save", methods=["GET"])
def save_all():
  global websites
  save_websites(websites, abs_file_path)
  return redirect(url_for('index')) 

@app.route("/delete", methods=["GET"])
def delete_website():
  global websites
  website_index=request.args.get('index')
  websites.pop(int(website_index))
  return redirect(url_for('index')) 


# submit to gptapi
@app.route("/submit",methods=["POST"])
def submit():
  blog_text = ""
  if request.method == "POST":
    topic = request.get_json()['topic']
    keywords = request.get_json()['keywords']
    api_response = generate_text(topic, keywords)
    blog_text = api_response["choices"][0]["message"]["content"]
    print(blog_text)
  return json.dumps(blog_text)



# add website page and POST request
@app.route("/add/website", methods=["GET", "POST"])
def add_website():
  global websites
  is_failed = 0
  if request.method == "POST":
    website_url = request.form['website_url']

    wp_login = request.form['wp_login']
    wp_password = request.form['wp_password']
    is_offline = request.form['is_offline']
    status_type =StatusType.WEBSITE

    if (website_url=="" or wp_login=="" or wp_password=="") and is_offline=="off": 
      is_failed = 1
      return render_template("create-website.html", failed=is_failed)
    
    if is_offline == 'on':
      # offline website
      status_type=StatusType.OFFLINE
      websites.append(Website(status_type, 'Offline Task', 'N/A', 'N/A'))
      print("Successfully added website!")
      return redirect(url_for('index'))

    # add the slash onto the end of the url
    if website_url[len(website_url)-1] != '/':
      website_url+='/'
      
    is_failed = 0

    print("Successfully added website!")
    websites.append(Website(status_type, website_url,wp_login,wp_password))
    return redirect(url_for('index'))
  return render_template("create-website.html", failed=is_failed)


# clicked on website item
@app.route("/website")
def website():
  global websites
  website_index=request.args.get('index')
  print(websites[int(website_index)].projects)
  return render_template("website.html", website = websites[int(website_index)], projects=websites[int(website_index)].projects, index=int(website_index))


# clicked on website item
@app.route("/website/run")
def run_project():
  print("Loading...")
  global websites
  website_index=int(request.args.get('web_index'))
  project_index=int(request.args.get('proj_index'))

  websites[website_index].projects[project_index].generate_periodic(websites[website_index].status_type, websites[website_index].website_url, websites[website_index].login, websites[website_index].password)

  print(websites[website_index].projects)
  return render_template("website.html", website = websites[int(website_index)], projects=websites[int(website_index)].projects, index=int(website_index))

# clicked on website item
@app.route("/website/delete")
def del_project():
  print("Loading...")
  global websites
  website_index=int(request.args.get('web_index'))
  project_index=int(request.args.get('proj_index'))

  try:
    websites[website_index].projects.pop(project_index)
  except:
    print("Something went wrong...")
  else:
    print("Succesfully deleted!")
  return render_template("website.html", website = websites[int(website_index)], projects=websites[int(website_index)].projects, index=int(website_index))


# add project
@app.route("/add/project/keywords", methods=["GET", "POST"])
def add_project_keywords():
  global websites
  is_failed = 0
  website_index=int(request.args.get('index'))

  if request.method == "POST":
    name = request.form['name']
    general_statement = request.form['general-statement']
    fill_blanks = request.form['fill-blank'].split('\r\n')
    print(fill_blanks)

    keywords_list = request.form['keywords'].split('\r\n')
    language = Language(request.form['language'])
    min_word_count = int(request.form['wordcount'])
    # parse keywords into array
    new_project = Project(name, ProjectType.KEYWORDS, 0, language)
    new_project.general_statement = general_statement
    new_project.fill_blanks = fill_blanks
    new_project.keywords_dynamic=keywords_list
    new_project.min_word_count=min_word_count
    new_project.slug = request.form['slug']



    websites[website_index].add_project(new_project)
    print("Project added!")
    return redirect(url_for('website', index=website_index))
  return render_template("create-project-keywords.html", failed=is_failed, index=website_index)

@app.route("/add/project/titles", methods=["GET", "POST"])
def add_project_title():
  global websites
  is_failed = 0
  website_index=int(request.args.get('index'))
  if request.method == "POST":
    name = request.form['name']
    title = request.form['titles'].split('\n')
    language = Language(request.form['language'])
    min_word_count = int(request.form['wordcount'])
    print(language)
    # parse keywords into array
    new_project = Project(name, ProjectType.TITLES, 0, language)
    new_project.titles = title
    new_project.min_word_count=min_word_count
    new_project.slug = request.form['slug']

    websites[website_index].projects.append(new_project)
    print(json.dumps(websites[website_index], cls=ComplexEncoder))
    return redirect(url_for('website', index=website_index))
  return render_template("create-project-title.html", failed=is_failed, index=website_index)

if __name__ == "__main__":
  # webbrowser.open('http://127.0.0.1:8000')  # Go to example.com
  app.run(port=8000)
