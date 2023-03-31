import json
import os
from flask import Flask, redirect, url_for, render_template, request
from files.gptapi import generate_text
from files.scripts import Website, Project, load_websites, save_websites, StatusType, ProjectType, Language, ComplexEncoder


app = Flask(__name__)


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "files/text/saves.json"
abs_file_path = os.path.join(script_dir, rel_path)
#
websites = load_websites(abs_file_path)
print(websites)

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

    if website_url=="" or wp_login=="" or wp_password=="": 
      is_failed = 1
      return render_template("create-website.html", failed=is_failed)
    
    is_failed = 0
    websites.append(Website(website_url,wp_login,wp_password))
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
  global websites
  website_index=int(request.args.get('web_index'))
  project_index=int(request.args.get('proj_index'))

  url = websites[website_index].website_url
  login = websites[website_index].login
  password = websites[website_index].password

  websites[website_index].projects[project_index].generate_periodic()

  print(websites[website_index].projects)
  return render_template("website.html", website = websites[int(website_index)], projects=websites[int(website_index)].projects, index=int(website_index))


# add project
@app.route("/add/project/keywords", methods=["GET", "POST"])
def add_project_keywords():
  global websites
  is_failed = 0
  website_index=int(request.args.get('index'))

  if request.method == "POST":
    name = request.form['name']
    topic = request.form['topic']
    keywords_list = request.form['keywords'].split('\n')
    language = Language(request.form['language'])
    print(language)
    # parse keywords into array
    new_project = Project(name, StatusType.WEBSITE, ProjectType.KEYWORDS, 0, language)
    new_project.topic = topic
    new_project.keywords_dynamic=keywords_list

    websites[website_index].projects.append(new_project)
    print(json.dumps(websites[website_index], cls=ComplexEncoder))
    return redirect(url_for('website', index=website_index))
  return render_template("create-project-keywords.html", failed=is_failed, index=website_index)

@app.route("/add/project/titles", methods=["GET", "POST"])
def add_project_title():
  global websites
  is_failed = 0
  website_index=int(request.args.get('index'))

  return render_template("create-project-title.html", failed=is_failed, index=website_index)

if __name__ == "__main__":
  app.run()