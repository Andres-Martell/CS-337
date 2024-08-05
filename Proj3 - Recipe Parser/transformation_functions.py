import dependency_parser as dp
import scraper as s
from text2digits import text2digits
import lexicon_files as lexicons
import transformation_dicts as td
import re
from scaling import fraction_finder as ff



def remove_parentheses(string):
    return re.sub(r'\([^()]*\)', '', string)


def remove_measurements(string):
    # Define a list of common cooking measurements and their abbreviations
    measurements = [
        "teaspoon", "tsp", "tablespoon", "tbsp", "cup", "pint", "quart", "gallon",
        "ounce", "oz", "pound", "lb", "gram", "g", "kilogram", "kg", "cups", "pints", "gallons", "quarts", 
        "pounds", "grams", "kilograms", "tablespoons", "teaspoons", "ounces", "lbs", "pounds"
    ]

    # Replace each measurement with an empty string
    for measurement in measurements:
        string = re.sub(r'\b{}\b'.format(measurement), '', string, flags=re.IGNORECASE)

    #finding fractions and replacing it with a number to be able to remove it
    split_string = string.split()
    for i in range(len(split_string)):
        upd = ff(split_string[i], 1)
        if upd != None:
            split_string[i] = str(upd)
    string = " ".join(split_string)

    # Replace numbers with an empty string
    string = re.sub(r'\d+', '', string)
    #repalce decimal points with emptry string
    string = re.sub(r'\.', '', string)

    return string.strip()



def pick_transform(num, ingredients, recipe):
    num = int(num)
    #print(num)
    if num == 0:
        print("you have chosen vegan")
        return vegan_transform(ingredients, recipe)
    if num == 1:
        print("you have chosen vegetarian")
        return non_veggie_to_veggie(ingredients, recipe)
    if num == 2:
        print("you have chosen non-vegetarian")
        return veggie_to_non_veggie(ingredients, recipe)
    if num == 3:
        print("you have chosen healthy")
        return transform_healthy(ingredients, recipe)
    if num == 4:
        print("you have chosen unhealthy")
        return transform_unhealthy(ingredients, recipe)
    if num == 5:
        print("you have chosen Italian")
        return transform_italian(ingredients, recipe)
    if num == 6:
        print("you have chosen Mexican")
        return transform_mexican(ingredients, recipe)
    


def vegan_transform(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        
        starting_key = remove_parentheses(remove_measurements(ingredient))
        while(not starting_key == ""):
            if starting_key in td.vegan_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.vegan_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.vegan_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.vegan_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.vegan_transformations[word]
    return substitution_dict

def non_veggie_to_veggie(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        
        starting_key = remove_parentheses(remove_measurements(ingredient))
        while(not starting_key == ""):
            if starting_key in td.vegetarian_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.vegetarian_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.vegetarian_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.vegetarian_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.vegetarian_transformations[word]
    return substitution_dict

def veggie_to_non_veggie(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        
        starting_key = remove_parentheses(remove_measurements(ingredient))
        while(not starting_key == ""):
            if starting_key in td.non_vegetarian_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.non_vegetarian_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.non_vegetarian_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.non_vegetarian_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.non_vegetarian_transformations[word]
    return substitution_dict

def transform_italian(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        #print(ingredient)
        #print("here")
        starting_key = remove_parentheses(remove_measurements(ingredient))
        #print(starting_key)
        while(not starting_key == ""):
            if starting_key in td.italian_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                #print(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.italian_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.italian_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.italian_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.italian_transformations[word]
    return substitution_dict

def transform_mexican(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        #print(ingredient)
        #print("here")
        starting_key = remove_parentheses(remove_measurements(ingredient))
        #print(starting_key)
        while(not starting_key == ""):
            if starting_key in td.mexican_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                #print(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.mexican_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.mexican_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.mexican_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.mexican_transformations[word]
    return substitution_dict

def transform_healthy(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        #print(ingredient)
        #print("here")
        starting_key = remove_parentheses(remove_measurements(ingredient))
        #print(starting_key)
        while(not starting_key == ""):
            if starting_key in td.healthy_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                #print(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.healthy_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.healthy_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.healthy_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.healthy_transformations[word]
    return substitution_dict



def transform_unhealthy(ingredients, recipe):
    #check if any of the ingredients are in the non_veggie_proteins list
    #remove existing veggies from the list options (proteins)

    #NOTE: CHECK IF THERE IS A FRACTION SOMEHOW, AND CHANGE ALL STRINGS IN INGREDIENT LISTS TO BE NORMAL FRACTIONS NOT THE WEIRD ONES CAUSE IT STORES ODDLY
    substitution_dict = dict()
    for ingredient in ingredients:
        #check to see if string past measurements is in there and then look at modifiers to do it
        #print(ingredient)
        #print("here")
        starting_key = remove_parentheses(remove_measurements(ingredient))
        #print(starting_key)
        while(not starting_key == ""):
            if starting_key in td.unhealthy_transformations:
                break
            else:
                old_key = starting_key
                starting_key = dp.remove_first_modifier(starting_key)
                #print(starting_key)
                if old_key == starting_key:
                    break

        if starting_key in td.unhealthy_transformations:
            substitution_dict[remove_measurements(ingredient)] = td.unhealthy_transformations[starting_key]

        else: 
            words = ingredient.split(" ")
            for word in words:
                if word in td.unhealthy_transformations:
                    substitution_dict[remove_measurements(ingredient)] = td.unhealthy_transformations[word]
    return substitution_dict




x,y = s.new_scraping("https://www.allrecipes.com/recipe/8526807/ground-beef-stroganoff-noodles/")
#print(x)
#print(y)
#print(transform_italian(x,y))




#if goal_multiplier = 1, it auto calculates goal based off original amount of protein, if not we convert to that goal 
# (ie if we wanna increase/decrease protein)
def protein_converter(ingredient, ingredient2, amount, goal_multiplier): #https://www.etiwoundhealingcenter.com/documents/Protein-Chart.pdf 
    #use protein content chart to convert a protein ingredient to a different one
    #currently assuming that we're using the same unit, might need to have a unit converter function
    protein_info1 = lexicons.protein_chart[ingredient]
    amount1 = protein_info1['ingredient_amount']
    protein1 = protein_info1['protein_amount']
    protein_goal = ((amount * protein1) / amount1) * goal_multiplier

    protein_info2 = lexicons.protein_chart[ingredient2]
    amount2 = protein_info2["ingredient_amount"]
    protein2 = protein_info2["protein_amount"]

    howMuchProteinNeeded = protein_goal - protein2
    thresholdAllowed = 3 #3 grams within each other

    totalAmount = ((protein_goal * amount2) / protein2)
    return round(totalAmount,1)

#print(protein_converter('ham', 'snapper', 4, 1))


# takes in a value, and two unit types, converts from the first unit type to the 2nd.
# returns a float
def convert_units(value, from_unit, to_unit):
    
    conversions = {
    "tsp": {"tbsp": 0.333333, "cup": 0.0208333, "oz": 0.166667, "ml": 4.92892, "l": 0.00492892},
    "tbsp": {"tsp": 3.0, "cup": 0.0625, "oz": 0.5, "ml": 14.7868, "l": 0.0147868},
    "cup": {"tsp": 48.0, "tbsp": 16.0, "oz": 8.0, "ml": 236.588, "l": 0.236588},
    "oz": {"tsp": 6.0, "tbsp": 2.0, "cup": 0.125, "ml": 29.5735, "l": 0.0295735},
    "ounce": {"tsp": 6.0, "tbsp": 2.0, "cup": 0.125, "ml": 29.5735, "l": 0.0295735},
    "ounces": {"tsp": 6.0, "tbsp": 2.0, "cup": 0.125, "ml": 29.5735, "l": 0.0295735},
    "lb": {"oz": 16.0, "grams": 453.592, "kg": 0.453592},
    "grams": {"lb": 0.00220462, "oz": 0.035274, "kg": 0.001},
    "kg": {"lb": 2.20462, "oz": 35.274, "grams": 1000},
    "floz": {"cup": 0.125, "pt": 0.0625, "qt": 0.03125, "gal": 0.0078125, "ml": 29.5735, "l": 0.0295735},
    "cup (dry)": {"oz": 8.0, "grams": 236.588, "kg": 0.236588},
    "oz (dry)": {"cup (dry)": 0.125, "grams": 28.3495, "kg": 0.0283495},
    "g (dry)": {"cup (dry)": 0.00422675, "oz (dry)": 0.035274, "kg": 0.001},
    "kg (dry)": {"cup (dry)": 4.22675, "oz (dry)": 35.274, "grams": 1000},
    }


    if from_unit == to_unit:
        return value

    try:
        conversion_factor = conversions[from_unit][to_unit]
    except KeyError:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported.")

    return value * conversion_factor
