from text2digits import text2digits
import scraper
import spacy
import unicodedata

def scale(ingredients, scaleby):
    t2d = text2digits.Text2Digits()
    updated_ingredients = []
    for ing in ingredients: 
        words = ing.split()
        updated_words = []
        for word in words:
            try:
                number = t2d.convert(word)
                scaled = int(number) * scaleby
                updated_words.append(str(scaled))
            except:
                scaled = fraction_finder(word, scaleby)
                if scaled == None:
                    updated_words.append(word)
                else: 
                    updated_words.append(str(scaled))
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(" ".join(updated_words))
        for i in range(len(doc)):
            if doc[i].pos_ == 'NUM' and doc[i+1].pos_ == 'NUM':
                updated_words[i] = str(float(updated_words[i]) + float(updated_words[i+1]))
                updated_words.pop(i+1)     
        updated_ingredients.append(" ".join(updated_words))

    return updated_ingredients

# referenced the code to identify fractions using unicode from https://stackoverflow.com/questions/49440525/detect-single-string-fraction-ex-%C2%BD-and-change-it-to-longer-string
def fraction_finder(s, scaleby):
    for c in s:
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        if name.startswith('VULGAR FRACTION'):
            normalized = unicodedata.normalize('NFKC', c)
            numerator, _ , denominator = normalized.partition('⁄')
            return (int(numerator) * scaleby / int(denominator))
        