from fractions import Fraction

# Accepts a string, returns list broken up by line
def listify_content(content):
    content = content.split("\n")
    content = [word.lower() for word in content]
    return content

# Accepts a list of strings, and returns the list with each string
# shortened based off the first instance of a parentheses
def parentheses_remover(list_content):
    new_lists = []
    for lst in list_content:
        if "(" in lst:
            index = lst.find("(")
            new_list = lst[:index]
            new_list = new_list.strip()
            new_lists.append(new_list)
        else:
            new_lists.append(lst.strip())
    return new_lists

#sort list by length, for more exact ingredient pickups
def length_and_duplicate_fixer(list_content):
    list_content = list(set(list_content))
    list_content.sort(key = len, reverse = True)
    return list_content

#fixes strings with two names, for the US and UK version
def us_and_uk_fixer(list_content):
    final_list = []
    for string in list_content:
        new_string = string.lower()
        if "/" in new_string:
            strings = new_string.split("/")
            strings = parentheses_remover(strings)
            for string_1 in strings:
                final_list.append(string_1)
            list_content.remove(string)
        else: final_list.append(new_string)
    return final_list


def parentheses_returner(string):
    parentheses = None
    if "(" in string:
        index = string.find("(") + 1
        index_close = string.find(")")
        if (not index == -1) and (not index_close == -1):
            parentheses = string[index:index_close]
    return parentheses

def protein_chart_cleaner(protein_file):
    chart_list = listify_content(protein_file)
    #amount, protein content per that amount, (vegetarian, pescetarian, or meat), modifier
    protein_dict = dict()
    for line in chart_list:
        name = substring_before_number(line)
        line = line.replace(name, "")
        #print("now line: ", line)
        amount = get_substring_with_numbers(line)
        amount_measure = just_numbers(amount) #just numbers
        line = line.replace((amount + " "), "")
        amount = amount.replace((amount_measure + " "), "") #cup, grams, ounces, etc

        if "/" in amount_measure or "." in amount_measure:
            amount_measure = float(Fraction(amount_measure))

        protein_content = substring_till_stop_word(line, cuisine_types)
        protein_numbers = just_numbers(protein_content)
        line = line.replace(protein_content, "")
        protein_content = protein_content.replace((protein_numbers + " "), "")


        typeOfCuisine = line.strip()
        modifier = parentheses_returner(name)
        if modifier:
            name = name.replace(("(" + modifier + ")"),"")

        internal_dict = {"ingredient_amount": float(amount_measure), "ingredient_measurement": amount, "protein_amount": float(protein_numbers), "protein_measurement": protein_content, "type": typeOfCuisine, "modifier": modifier}

        protein_dict[name.lower().strip()] = internal_dict

    return protein_dict


    #now clean each line

def substring_before_number(string):
    for i, char in enumerate(string):
        if char.isdigit():
            return string[:i]
    return string

#takes in string and set of stop words
def substring_till_stop_word(string, stop_words):
    final_str = ""
    string_words = string.split(" ")
    for word in string_words:
        if word not in stop_words:
            final_str += word + " "
        else:
            final_str = final_str.strip()
            break
    return final_str

def just_numbers(string):
    string_words = string.split()
    substring = []
    for word in string_words:
        word = word.strip()
        no_slash = word
        if "/" in word:
            no_slash = word.replace("/", "")
        if "." in word:
            no_slash = no_slash.replace(".", "")
        if (word.isdigit() or no_slash.isdigit()):
            substring.append(word)
            break
    return "".join(substring)



def get_substring_with_numbers(string):
    end = -1 
    string_words = string.split()
    substring = []
   #t2d = text2digits.Text2Digits()
    for word in string_words:
        word = word.strip()
        no_slash = word
        if "/" in word:
            no_slash = word.replace("/", "")
        if "-" in word:
            no_slash = no_slash.replace("-", "")
        if "." in word:
            no_slash = no_slash.replace(".", "")
        if (word.isdigit() or no_slash.isdigit()) and (not end == 1):
            substring.append(word)
            end = 1
        elif word.isdigit() or no_slash.isdigit():
            break 
        else:
            substring.append(word)
    return " ".join(substring)

    '''

    for i in range(len(string)):

        if string[i].isdigit() and not string[i] == "/"):
            end = i
            break
    if start != -1 and end == -1:
        end = len(string)
    print("string start: ", string[start:])
    '''
    return string

#given a list of strings, returns a matching key to the dictionary for each string if available
def key_matcher(dictionary, lst):
    pass

spices_file = open('spice_list.txt', 'r') #https://www.britannica.com/topic/list-of-herbs-and-spices-2024392 <- where we got info from spice list
veggies_file = open('fruits_and_veggies_list.txt', 'r') #https://7esl.com/fruits-and-vegetables-vocabulary/ https://plantprosperous.com/list-of-fruits-and-vegetables/ <- where we got fruits and veggies
proteins_file = open('proteins.txt', 'r')
veggie_proteins_file = open('vegetarian_protein.txt', 'r')
protein_chart_file = open('protein_chart.txt', 'r')


measures = {'grams', 'gram', 'ounces', 'ounce', 'cup', 'cups', 'tbsp', 'can'}
cuisine_types = {'v', 'p', 'm'}
spice_list = spices_file.read() 
spices = set(parentheses_remover(listify_content(spice_list)))

veggies_list = veggies_file.read()
veggies = length_and_duplicate_fixer(us_and_uk_fixer(listify_content(veggies_list)))

proteins_list = proteins_file.read()
proteins = length_and_duplicate_fixer(listify_content(proteins_list))

veggie_proteins_list = veggie_proteins_file.read()
veggie_proteins = set(length_and_duplicate_fixer(listify_content(veggie_proteins_list)))

non_veggie_proteins = set(proteins) - set(veggie_proteins)

protein_conversions = protein_chart_file.read()
protein_chart = protein_chart_cleaner(protein_conversions)

    
    


    