import spacy
from spacy import displacy

#https://towardsdatascience.com/natural-language-processing-dependency-parsing-cf094bbbe3f7

# Load the language model
nlp = spacy.load('en_core_web_sm')

#print("hello world")
'''
sentence = 'spicy chicken thighs'

# nlp function returns an object with individual token information,
# linguistic features and relationships
doc = nlp(sentence)

print("{:<15} | {:<8} | {:<15} | {:<20}".format(
    'Token', 'lemma', '  dep_', 'Children'))
print("-" * 70)

for token in doc:
  # Print the token, dependency nature, head and all dependents of the token
  print("{:<15} | {:<8} | {:<15} | {:<20}"
         .format(str(token.text), str(token.lemma_), str(token.dep_), str([child for child in token.children])))

 # Use displayCy to visualize the dependency

#displacy.render(doc, style='dep', jupyter=True, options={'distance': 120})
'''

def sentence_arrays(sentence):
  doc = nlp(sentence)
  action_dictionary = dict()
  for token in doc:
      tokens_array = [child for child in token.children]
      if len(tokens_array) > 0:
        if not str(token.text) in action_dictionary.keys():
          action_dictionary[str(token.text)] = tokens_array
        else:
          curr_words = action_dictionary[str(token.text)]
          curr_words = curr_words + tokens_array
          action_dictionary[str(token.text)] = curr_words

  for key in action_dictionary:
    if action_dictionary[key] == []:
      del action_dictionary[key]
  return action_dictionary


def dObjs(sentence):
  doc = nlp(sentence)
  objs = {'dobj': [], 'pobj': []}
  for i in range(len(doc)):
    token = doc[i]
    if 'obj' in str(token.dep_):
      text = str(token.text)
      if i - 1 > 0:
        if str(doc[i - 1].dep_) == 'compound':
          text = str(doc[i - 1].text) + " " + text
      if not str(token.dep_) in objs.keys():
        objs[str(token.dep_)] = [text]
      else:
        curr_list = objs[str(token.dep_)]
        curr_list.append(text)
        objs[str(token.dep_)] = curr_list
  return objs

def lemmaWords(sentence):
  doc = nlp(sentence)
  lemmas = []
  for token in doc:
    lemmas.append(token.lemma_)
  return lemmas

#print(sentence_arrays('Beat maple syrup and margarine together in a large bowl until well mixed and creamy. Mix in egg until combined.'))
#print(dObjs('How many eggs do I need?'))


def find_verb(sentence):
  doc = nlp(sentence)
  for token in doc:
    if token.pos_ == 'VERB':
      return token


def find_modifier(sentence, word):
  doc = nlp(sentence)
  text = word
  for i in range(len(doc)):
    token = doc[i]
    if token.text == word:
      if i > 0:
        if str(doc[i - 1].dep_) == 'compound':
          #return str(doc[i - 1])
          text = str(doc[i - 1]) + " " + text
  return text

def get_root_word(compound_word):
    doc = nlp(compound_word)
    root = None
    for token in doc:
        if token.dep_ == 'ROOT':
            root = token
            break
    if root is None:
        return compound_word
    return root.lemma_
  
  
#print(get_root_word('chopped boneless chickens'))
#print(get_root_word(' boneless chickens'))
#print(get_root_word(' mozerella cheese'))
'''
def remove_modifier(compound_word):
    doc = nlp(compound_word)
    root = None
    for token in doc:
        if token.dep_ == 'ROOT':
            root = token
            break
    if root is None:
        return compound_word
    modifier = None
    for child in root.children:
        if child.dep_ == 'amod' or child.dep_ == 'compound':
            modifier = child
            break
    if modifier is None:
        return root.text
    return modifier.head.text + ' ' + root.text
'''
  
def remove_first_modifier(compound_word):
    doc = nlp(compound_word)
    root = None
    for token in doc:
        if token.dep_ == 'ROOT':
            root = token
            break
    if root is None:
        return compound_word
    for child in root.children:
        if child.dep_ == 'amod' or child.dep_ == 'compound':
            return compound_word.replace(child.text + ' ', '', 1)
    return root.text
  
#print(remove_first_modifier('chopped boneless chicken thighs'))
#print(remove_first_modifier('boneless chicken'))
#print(remove_first_modifier('mozerella cheese'))
#print(remove_first_modifier('boneless chicken thighs'))
  
  
  

def dependency_tester(sentence):

  # nlp function returns an object with individual token information,
  # linguistic features and relationships
  doc = nlp(sentence)

  print("{:<15} | {:<8} | {:<15} | {:<20}".format(
      'Token', 'lemma', '  pos', 'Children'))
  print("-" * 70)

  for token in doc:
    # Print the token, dependency nature, head and all dependents of the token
    print("{:<15} | {:<8} | {:<15} | {:<20}"
          .format(str(token.text), str(token.lemma_), str(token.dep_), str([child for child in token.children])))

  # Use displayCy to visualize the dependency

  #displacy.render(doc, style='dep', jupyter=True, options={'distance': 120})