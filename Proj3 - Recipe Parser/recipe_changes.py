import dependency_parser as dp
import scraper
import transformation_dicts as dicts
test_dict = {
    'chicken': 'tofu',
    'orange juice': 'apple juice',
    'sugar': 'splenda',
    'tortillas': 'bread'
}


def change_ingredients(tranformation_dict, ingredients):
    for ing in range(len(ingredients)):
        ingwords = ingredients[ing].split()
        #print(ingwords)
        for i in range(len(ingwords)):
            #print(ingwords[i])
            for key in tranformation_dict.keys():
                if ingwords[i] == key:
                    ingwords[i] = tranformation_dict[key]
        ingredients[ing] = " ".join(ingwords)
    return ingredients

def change_content(tranformation_dict, content):
    for c in range(len(content)):
        cwords = content[c].split()
        #print(ingwords)
        for i in range(len(cwords)):
            #print(ingwords[i])
            for key in tranformation_dict.keys():
                if cwords[i] == key:
                    cwords[i] = tranformation_dict[key]
        content[c] = " ".join(cwords)
    return content

if __name__ == "__main__":
    ing, cont = scraper.new_scraping("https://www.allrecipes.com/recipe/8509102/chicken-al-pastor/")
    #print(ing)
    print(change_ingredients(dicts.vegetarian_transformations, ing))