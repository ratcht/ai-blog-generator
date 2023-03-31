from files.gptapi import GenerateText

topic = input("What would you like the blog topic to be about?: ")
keywords = input("What do you want the keywords to be? (seperate words by a comma): ")

blog_response = GenerateText(topic, keywords)
print(blog_response['choices'][0]['message']['content'])