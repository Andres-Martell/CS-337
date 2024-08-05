import networkx as nx
import re
import dependency_parser as dp
import scraper as s
import scaling
import youtubeScraper as youtube
import bs4
from text2digits import text2digits
import transformation_functions as tf
import string
from difflib import SequenceMatcher

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
import webbrowser

print("Welcome to the Recipe Reader! I'm Chef Gordon Ramsay! After entering the url of the recipe you'd like (from allrecipes.com), you may ask it questions, or give it commands like move forward, move backwards, or repeat the current step. You may also write 'exit' to leave the program.")

global ingredients
global content

url = input("Please enter the url of the recipe you'd like: ")
print("\n")
try:
    ingredients, content = s.new_scraping(url)
except:
    content = None
    print("Url not valid, please run again")

stepNum = 0
takeMePhrases = ['take me', 'go to', 'bring me to', "show me"]
navigationalPhrases = {"next": 1, "past":-1, "before": -1, "after": 1, "repeat": 0, "this step": 0, "prior": -1, "forward": 1, "forwards": 1, "back": -1, "previous": -1, "backwards": -1, "backward":-1}
quantityPhrases = ['many', 'much']
howToPhrases = ["how to", "how do i", "how could", "how would", "explain"]
durationPhrases = ['long', 'much time', 'minutes', 'hours', 'seconds']
time_keywords = ["minutes", "hours", "seconds"]
whatIsPhrases = ['what is', 'explain', 'what are', 'why', 'look up', 'substitute', 'change', 'replace']
ingredientsPhrases = ["ingredient", "ingredients"]
kindOfPhrases = ["kind of", "type"]
scalePhrases = ["scale", "less", "more"]


def breakDirections(recipeTxt):
    directions_index = recipeTxt.find("Directions")
    if directions_index == -1:
        return ""
    else:
        return recipeTxt[directions_index + len("Directions"):].strip()


def breakSentences(recipeTxt):
    # Split the string by any sequence of characters that ends with a period, question mark, or exclamation mark.
    # The split() method removes any leading or trailing whitespace.
    longText = ' '.join(recipeTxt)
    return re.split(r'(?<=[.?!])\s+', longText.strip())

def buildGraph(stepArray):
    g = nx.Graph()
    i = 0
    for step in stepArray:
        g.add_node(i, txt = step)
        i += 1
    j = 0
    while(j <= i):
        #after node:
        if j < i - 1:
            g.add_edge(j, j + 1)
        j+=1
    return g

def replacePronouns(query):
    keys = [str(dp.find_verb(query))]
    obj = dp.dObjs(query)['dobj']
    if obj:
        keys.append(obj[0])
    if any(map(query.lower().__contains__,['it', 'them', 'that', 'they'])):
        objects = dp.dObjs(g.nodes[stepNum]['txt'])
        dObjs = objects['dobj']
        keys = keys + dObjs
    if 'None' in keys:
        keys.remove('None')
    return keys

def moveThruSteps(g, currStep, dist):
    if currStep + dist >= 0 and currStep + dist < len(g.nodes):
        return currStep + dist
    else:
        if currStep + dist < 0:
            print("No steps previously")
        elif currStep + dist >= len(g.nodes):
            print("No further steps")
        return None

def wordInList(lst, word):
    for string in lst:
        if word in string:
            return string
    return None

def restOfSentence(string, word):
    index = string.find(word)
    if index == -1:
        return None
    return string[index + len(word):]

def durationQuestion(query):
    keys = [str(dp.find_verb(query))]
    obj = dp.dObjs(query)['dobj']
    if obj:
        keys.append(obj[0])
    if any(map(query.lower().__contains__,['it', 'them', 'that'])):
        objects = dp.dObjs(g.nodes[stepNum]['txt'])
        dObjs = objects['dobj']
        keys = keys + dObjs
    time_relevant_steps = []
    for step in content: 
        if any(map(step.lower().__contains__,time_keywords)):
            time_relevant_steps.append(step)
    returned_steps = []
    for t_step in time_relevant_steps:
        if any(map(t_step.lower().__contains__,keys)):
            returned_steps.append(t_step)
    if returned_steps:
        return ''.join(returned_steps)
    if len(returned_steps) == 0 and len(time_relevant_steps) > 0:
        return time_relevant_steps[0]
    else:
        return "Answer not found" 
    return ''.join(returned_steps)


def howManyQuestion(inquiry, manyWord):
    objects = dp.dObjs(inquiry)
    dObjs = objects['dobj']
    objStr = ' '.join(dObjs)
    if not dObjs:
        dObjs.append(restOfSentence(inquiry, manyWord))
    lemmaObjs = dp.lemmaWords(objStr)
    dObjs = dObjs + lemmaObjs

    for dObj in dObjs:
        possible_instruction = wordInList(ingredients, dObj)
        if possible_instruction:
            return possible_instruction
    pObjs = objects['pobj']
    pObjStr = " ".join(pObjs)
    if not pObjs:
        pObjs.append(restOfSentence(inquiry, manyWord))
    lemmaPObjs = dp.lemmaWords(pObjStr)
    pObjs = pObjs + lemmaPObjs
    for pObj in pObjs:
        possible_instruction = wordInList(ingredients, pObj)
        if possible_instruction:
            return possible_instruction


    return "Try rewording your question, please :0"

def howToQuestion(inquiry, howToWord):
    print("Video answer loading...\n")
    youtube.open_youtube_video(inquiry)


def whatIsQuestion(inquiry):
    print("google search loading...\n")
    url = ''
    #j = search(query)
    for j in search(inquiry, num_results = 2):
        if not url:
            url = j
        #print(j)
    webbrowser.open(url, new = 2)

def ingredientsQuestion():
    for ingredient in ingredients:
        print(ingredient)
    print("\n")


def phrase_in_string(string, phrases):
    for phrase in phrases:
        if string.find(phrase) != -1:
            return phrase #might need to change back to return True
    return False

def whatKindOfQuestion(inquiry, phrase_found):
    #inquiry = re.sub(phrase_found, '', inquiry)
    inquiry_words = inquiry.split(" ")
    possible_ingredients = []
    #print(dp.dependency_tester(inquiry))
    objects = dp.dObjs(inquiry)
    dObjs = objects['dobj']
    dObjs = dObjs + objects['pobj']
    #print("objs: ", dObjs)
    objStr = ' '.join(dObjs)
    if not dObjs:
        dObjs.append(restOfSentence(inquiry, phrase_found))
    lemmaObjs = dp.lemmaWords(objStr)
    dObjs = dObjs + lemmaObjs
    dObjs = list(set(dObjs))
    if dObjs:
        if len(dObjs) > 1:
            for obj in dObjs:
                possible_ingredient = wordInList(ingredients, obj)
                if possible_ingredient:
                    ingredient = possible_ingredient
        else: ingredient = dObjs[0]
    else:
        print("Try rewording your question please")
    #wanna find the phrase in ingredients list that has it
    #look at ingredients list, find the relevant one, return the modifier of the ingredient
    ingredientsPhrase = wordInList(ingredients, ingredient)
    if ingredientsPhrase:
        print(dp.find_modifier(ingredientsPhrase, ingredient), "\n")



def ingredient_matcher(step_string, ingredients_list):
    #parse the words in step_string, and see if any of them match that of ingredients_list 
    #ingredients_without_punctuation = remove_punctuation(ingredients_list)
    step_ingredients = []
    common_words = ["and", "to", "with", "medium", "low", "high", "or", "ground", " ", ",", ""]
    ingredient_counts = dict()
    word_counts = dict()
    step_string = set(remove_punctuation(step_string.split(" ")))
    
    #if there's a word in an ingreident that matches the word in step_string, add it to it's dictionary
    for ingredient in ingredients_list:
        ingredient_counts[tf.remove_measurements(ingredient)] = 0
        ingredient_without_measure = tf.remove_measurements(ingredient)
        ingredient_words = ingredient_without_measure.split(" ")
        ingredient_words = remove_punctuation(ingredient_words)
        for word in ingredient_words:
            if (word in step_string) and (not word in common_words):
                step_ingredients.append(tf.remove_measurements(ingredient))
                ingredient_counts[tf.remove_measurements(ingredient)] += 1
                if word in word_counts:
                    if tf.remove_measurements(ingredient) not in word_counts[word]:
                        old_list = word_counts[word]
                        old_list.append(tf.remove_measurements(ingredient))
                        word_counts[word] = old_list
                else:
                    word_counts[word] = [tf.remove_measurements(ingredient)]
                #print(ingredient)
                #print("word match: ", word)

    #check the ingredients for any repeats:
    #if any word_counts are above 1, that means a word has matched twice. not ideal, so get rid of whichever one has less words
    for word in word_counts:
        possible_ingredients = word_counts[word]
        if len(possible_ingredients) == 2:
            possible_ingredients_1 = possible_ingredients[0]
            possible_ingredients_2 = possible_ingredients[1]
            if ingredient_counts[possible_ingredients_1] > ingredient_counts[possible_ingredients_2]:
                step_ingredients.remove(possible_ingredients_2)
            elif ingredient_counts[possible_ingredients_1] < ingredient_counts[possible_ingredients_2]:
                step_ingredients.remove(possible_ingredients_1)
            
            #NOTE: COME BACK HERE AND CHECK IF THE WORD IS INGREDIENT, THEN COMPARE THE WORD_COUNTS IN THE DICTIONARY INGREDIENT_COUNTS


    return (list(set(step_ingredients)))

def remove_punctuation(strings):
    table = str.maketrans("", "", string.punctuation) # create a translation table to remove punctuation
    new_strings = []
    for s in strings:
        new_s = s.translate(table) # remove punctuation using the translation table
        new_strings.append(new_s)
    return new_strings


def takeMeResponse(inquiry, step_length):
    #check if step is in the word
        #check for number 
        #check for written number
        #check for first or last
    step_match = re.search(r'\bstep\b', inquiry)
    if step_match:
        number_matches = re.findall(r'\d+', inquiry)
        possible_written_number = extract_written_number(inquiry)
        if number_matches:
            if len(number_matches) == 1:
                if int(number_matches[0]) - 1 >= 0 and int(number_matches[0]) - 1 < step_length:
                    return int(number_matches[0]) - 1
                else:
                    return
            else:
                index = inquiry.find("step")
                num_1_index = inquiry.find(number_matches[0])
                num_2_index = inquiry.find(number_matches[1])
                if abs(index - num_1_index) < abs(index - num_2_index):
                    if int(number_matches[0]) - 1 >= 0 and int(number_matches[0]) - 1 < step_length:
                        return int(number_matches[0]) - 1
                else:
                    if int(number_matches[1]) - 1 >= 0 and int(number_matches[1]) - 1 < step_length:
                        return int(number_matches[1]) - 1
        elif not possible_written_number == -1:
            if possible_written_number -1 >= 0 and possible_written_number - 1 < step_length:
                return possible_written_number - 1
        else: #check for first or last
            first_check = inquiry.find("first")
            last_check = inquiry.find("last")
            if not first_check == -1:
                return 0
            elif not last_check == -1:
                return step_length
        return -1
    else: return -2


def extract_written_number(text):
    t2d = text2digits.Text2Digits()
    words = text.split()
    for word in words:
        try:
            number = t2d.convert(word)
            try: 
                num = int(number)
                return num
            except:
                pass
        except ValueError:
            pass
    return -1

def scaleQuestion(inquiry):
    global ingredients
    try: 
        scaleby = float(inquiry)
        ingredients = scaling.scale(ingredients, scaleby)
        return
    except Exception as e:
        inp2 = input("Please enter a valid number to scale by: ")
        scaleQuestion(inp2)



def substitute(transformation_dict):
    global ingredients
    global content
    possible_subs = list(transformation_dict.keys())
    steps = breakSentences(content) #will be editing steps to be correct, then add it all back together to one big string
    common_words = ["and", "to", "with", "medium", "low", "high", "or", "ground", " ", ",", ""]
    new_steps = []
    used_subs = set()

    for step in steps:
        #step = remove_punctuation(step.split(" ")))
        relevant_ingredients = ingredient_matcher(step, ingredients)
        #print("relevant_ingredients: ", relevant_ingredients)
        #print("possible_subs: ", possible_subs)
        in_common = set(relevant_ingredients) & set(possible_subs)
        if in_common: #will have to make sure that all dicts return EXACTLY string that ingredient matcher appears:
            #print("Are any in common: ", in_common)
            for common_ingredient in in_common:
                #print(common_ingredient)
                #ingredient_without_measure = tf.remove_measurements(common_ingredient)
                similarity = SequenceMatcher(None, common_ingredient, step).ratio()
                if common_ingredient in step:
                    #print("made it in: ", common_ingredient)
                    step = step.replace(common_ingredient, transformation_dict[common_ingredient])
                    used_subs.add(common_ingredient)
        new_steps.append(step)
    final_steps = []
    for step in new_steps:
        step_words = step.split(" ")
        relevant_ingredients = ingredient_matcher(step, ingredients)
        in_common = set(relevant_ingredients) & set(possible_subs)
        in_common.difference_update(used_subs)
        if in_common:
            for common_ingredient in in_common:
                common_ingredient_words = common_ingredient.split(" ")
                for word in step_words:
                    table = str.maketrans("", "", string.punctuation)
                    new_word = word.translate(table)
                    if new_word in common_ingredient_words:
                        change = step_words.index(word)
                        step_words[change] = transformation_dict[common_ingredient]
                step = " ".join(step_words)
        final_steps.append(step)

    for ingredient in ingredients:
        for sub in possible_subs:
            similarity = SequenceMatcher(None, ingredient, sub).ratio()
            if similarity > .5:
                #print("check do i get here")
               # print(sub)
               # print(ingredient)
               # print(tf.remove_parentheses(sub))
                try:
                    ingredient_index = ingredients.index(ingredient)
                    ingredients[ingredient_index] = ingredient.replace(tf.remove_parentheses(sub).strip(), transformation_dict[sub])
                except:
                    continue
    #print(ingredients)



    






    #print("step rn: ", step)
    '''
    else:
        ingredient_words = common_ingredient.split(" ")
        ingredient_words = remove_punctuation(ingredient_words)
        #print("step: ", step)

        for word in ingredient_words:
            #print("word: ", word)
            if (word in step) and (not word in common_words):
                step = step.replace(word, transformation_dict[common_ingredient])
    '''
    content = final_steps 




                #in step, find what common word for that ingredient is in there that caused  it to match
        #entire string other than measurements will be in transformattion dict as keys



#start at 0, move thru based on navigational commands. keep track of step in main
def newPhrase(g, inquiry):
    #navigational phrases
    inquiry_words = inquiry.split()
    keys = navigationalPhrases.keys()
    global stepNum
    inquiry_words = inquiry_words + replacePronouns(inquiry)
    for word in inquiry_words:
        if word in keys:
            distance = navigationalPhrases[word]
            if not moveThruSteps(g, stepNum, distance) == None:
                stepNum = moveThruSteps(g, stepNum, distance)
                print(g.nodes[stepNum]['txt'], "\n")
            return

    if phrase_in_string(inquiry, takeMePhrases):
        possible_step = takeMeResponse(inquiry, len(g.nodes) -1)
        if not possible_step == -1 and not possible_step == -2 and not possible_step == None:
            stepNum = possible_step
            print(g.nodes[stepNum]['txt'], "\n")
            return
        else: 
            if not possible_step == -2:
                print("Not a valid step, sorry D:")
                return


    
    #if past this, no navigational phrases. Now check for question types
    
    #how many questions
    n_inquiry = " ".join(inquiry_words)
    for word in inquiry_words:
        if word in ingredientsPhrases: #what are the ingredients questions?
            ingredientsQuestion()
            return

        if word in durationPhrases:
            print(durationQuestion(n_inquiry))
            print("\n")
            return

        if word in quantityPhrases: #so it is a how many question
            print(howManyQuestion(n_inquiry, word))
            print("\n")
            return


    if phrase_in_string(inquiry, kindOfPhrases):
        phrase_found = phrase_in_string(n_inquiry, kindOfPhrases)
         #so it is what kind of question
        whatKindOfQuestion(n_inquiry, phrase_found)
        return

    if phrase_in_string(n_inquiry, howToPhrases): #so it is a how to question
        howToQuestion(n_inquiry, word)
        return

  
    if phrase_in_string(n_inquiry, whatIsPhrases): #so it is a what is question
        whatIsQuestion(n_inquiry)
        return

    inp = input("We could not find a response for your inquiry. Would you like us to google your inquiry? Y/N: ")
    if inp.lower() == 'y':
        whatIsQuestion(n_inquiry)
    else: 
        print("Ok sounds good.")
    #questions



if __name__ == '__main__':
    
    while(content == None):
        url = input("Please enter the url of the recipe you'd like: ")
        print("\n")
        try:
            ingredients, content = s.new_scraping(url)
        except:
            print("Url not valid, please run again.")
    picker = input("Would you like to perform a transformation? Y/N: ")
    if picker.lower() == "y":
        print("0 - vegan\n")
        print("1 - vegetarian\n")
        print("2 - non-vegetarian\n")
        print("3 - healthy\n")
        print("4 - unhealthy\n")
        print("5 - Italian\n")
        print("6 - Mexican\n")
        print("7 - Change the scale of the recipe\n")
        picker2 = input("type the # of the transformation you would like to perform: ")
        if int(picker2) == 7:
            inq = input("How much would you scale by?: ")
            scaleQuestion(inq)
        else:
            transform_dict = tf.pick_transform(picker2, ingredients, content)
           # print(transform_dict)
            substitute(transform_dict)
        print("Transformed. Ready to step through the recipe!")
    
    steps = breakSentences(content)
    g = buildGraph(steps)
    exiting = False
    yOrN = input("Would you like to display the whole ingredients list before getting started? Y/N: ")
    if yOrN.lower() == "y":
        ingredientsQuestion()
    else:
        print("Okay! Let's get started!\n")
    print("First step:", g.nodes[stepNum]['txt'])
    while(not exiting):
        inq = input("What would action would you like to take next?: ")
        inq = inq.lower()
        inq = re.sub(r'[^\w\s\']', '', inq)
        if inq == 'exit':
            exiting = True
            break
        newPhrase(g, inq)
    #print(tf.non_veggie_to_veggie(ingredients, content))
    #example_step = "Add chicken broth to a medium saucepan and bring to a boil over medium-high."

    '''
    for step in g.nodes:
        txt = g.nodes[step]['txt']
        print("step: ", txt)
        print(ingredient_matcher(txt, ingredients))
        print("\n")
    '''
    #print(ingredient_matcher(example_step, ingredients))
    #example_transform = tf.non_veggie_to_veggie(ingredients, content)
    #substitute(example_transform)

# Meanwhile, heat 2 tablespoons of the oil in a large pot or Dutch oven over medium-high. -> why doesnt this return oil
#Add 3 of the onion quarters, reserving the last quarter for later use, and garlic to pan. -> ['12  lime wedges, for serving', '4 cloves garlic']
# Can fix above if i make it check in a list of words for the step string rather than just in the string

#step:  Add chicken; cook, flipping once, until golden brown, about 3 minutes per side. <- why is chicken broth matching
#['1 ½ pounds skinless, boneless chicken breasts', '4 cups chicken broth', '1  dried de árbol chile, stemmed and seeded (Optional)']
#matching bc chicken breasts and chicken broth both have the same number of matching words, just chicken. dont know what i can look at to get it to just match w chicken

#step:  Repeat process with remaining sauce, meat chicken and tortillas.
#['4 cups chicken broth', '1 ½ pounds skinless, boneless chicken breasts'] -> why doesn't this get tortillas