from bs4 import BeautifulSoup
import urllib.request as browser
import re
import requests 


def new_scraping(url):
    page = requests.get(url)
    if not page: 
        print("Please enter a valid url from https://allrecipes.com with https:// at the begining of your url")
        return None, None
    #print(page.content)
    soup = BeautifulSoup(page.content,"lxml")
    captions = soup.find_all(class_ = "figure-article-caption-owner")
    for c in captions:
        c.replace_with('')
    ingredients = soup.find_all(class_ = "mntl-structured-ingredients__list-item")
    text_ingredients = []
    for i in ingredients:
        text = re.sub(r'\n','',i.text)
        text_ingredients.append(text)
    
    
    steps = soup.find_all(class_ = "comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup")
    text_steps = []
    for step in steps:
        text = re.sub(r'\n','',step.text)
        text_steps.append(text)
    return text_ingredients, text_steps

