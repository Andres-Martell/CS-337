# CS337 Project3 Recipe Transformer

Contributors: Reagan Dennison, Andres Martell, and Nik Yadav 

## Installation and things to download

- Run the requirements.txt file to download all of the necessary imports we use in the project. Run the command "pip install -r requirements.txt" on whatever machine you wish to run the project on. 



## Running the Program 

- To run the program, use "python recipeParsing.py" to call our function
- Once the program starts, it will ask you to enter a link from allrecipes.com. Please enter the url that you wish to use for your recipe. 
- After entering the url, the bot will ask if you want to make any transformation to the recipe. The possible transformations are vegetarian/non-vegetarian, healthy/not-healthy, cuisine alterations, and scaling the recipe. You are prompted to pick which option you would like to transform the recipe to. Once you pick the transformation, it will alter the ingredients and steps for you. 
- After any transformation, the program will take you through the recipe step by step. You can traverse through the recipe by saying next, forward, or forward moving phrases or backwards with similar phrases. You can also say take me to the nth step in written form (i.e. Take me to the fourth step)
- At any point, you can ask the bot questions about quantity, duration, and other questions. Based on your question we can provide the answer from the ingredients or recipe steps or if the answer is not present in the recipe a youtube video or google search will open to better help with your question.

### Example queries
- What kind of mushrooms do I need?
- How long do I cook the chicken for?
- What are the ingredients? 
- What is fish sauce? (google search will occur)
- How do I cook chicken? (youtube search will occur)
- Take me to step 4
- Show me the fourth step

## Works Cited 
- https://medium.com/geekculture/scrape-youtube-search-with-python-part-1-7521a0f40315 was used for reference on youtube scraping
- https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7 was used for reference on dependency parsing 
- https://realpython.com/beautiful-soup-web-scraper-python/ was used for reference for screen scraping the information for the recipes 
- We used the following links for creating our dictionaries: https://www.britannica.com/topic/list-of-herbs-and-spices-2024392, https://plantprosperous.com/list-of-fruits-and-vegetables/, and https://7esl.com/fruits-and-vegetables-vocabulary/. 
- We also used ChatGPT for the creation of some our dictionaries for the transformation of ingredients. We wanted to have a more extensive dictionary of possible changes to a recipe, so we queried chatgpt with our dictionary and had it add other possible key-value pairs to our existing dictionaries. 
- A number of stackoverflow forums were also used throughout the project. One in particular 


### Link to our github repository
https://github.com/red6696/cs337_project3
