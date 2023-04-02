# ai-blog-generator
Blog Generator powered by OpenAI
Note: This blog generator is compatible with WordPress REST API

Before starting the webapp, you must create an api-key.txt file
  Under files, create a txt file named api-key.txt and paste in your ChatGPT API Key

To start the webapp, run "app.py", it should open a browser page
  If it doesn't automatically open, you can navigate to https://127.0.0.1:8000/

To use with WordPress:
  * In WordPress, you must generate an Application Password
    This will be the password you input into the 'WordPress Password' field under /add/website
  * The username must be the username of an admin account to your wordpress site
  * The website url must end with '/'
  
To use Offline:
  Simply check the 'offline' checkbox and proceed normally
  
Once you have created a 'website', you must now create a project
  Clicking on a website field will take you to another page
  Here, you can choose either to create a project 'By keywords' or 'By titles'
    * 'By Keywords' allows you to input a 'topic' and a list of keywords. Each new line in the 'keywords' textarea will generate new blog post

After clicking create project, you must now navigate back to the project, and click Run
  This will either generate a blog and upload it to WordPress, or will generate a new txt file named 'blog{#}.txt' containing the generated blog
  
