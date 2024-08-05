#hosts collection

import tweet_handler as tw
from collections import Counter
import re

host_keywords = ['hosts', 'host', 'hosted by', 'hosting']
presenter_keywords = ['present', 'presents', 'presenters are','Presenters are', 'presenter is','Presenter is', 'presented by', 'Presented by']
#tweet_search
#presenter_keywords = [('presenters are', 'after'),('Presenters are', 'after'), ('presenter is', 'after'),('Presenter is', 'after'), ('presented', , 'Presented', 'presenting', 'Presenting']
presenters_keywords = [["present", ""], ["presents", ""],["presenters", "are"],["Presenters", "are"], ["presenter", "is"], ["Presenter", "is"], ["presented", "by"], ["Presented", "by"]]

regexPresent = re.compile('[pP]resen(t|ts|ter is|ters are|ted by)')
#given a counter, returns list of only the values with capital letters as the start
def Capitals(counter):
    capitals = dict()
    for string in counter:
        count = counter[string]
        if not string == '':
            if string[0].isupper():
                capitals[string] = count
    return capitals

def choose_host_tie(counter):
    possibleHosts = Capitals(counter)
    longest_name = ''
    start_value = 0
    for string in possibleHosts:
        if longest_name == '':
            longest_name = string
            start_value = possibleHosts[longest_name]
        else:
            lowers_present = False
            if not string.find(longest_name) == -1:
                parsed_string = string.split(' ')
                for word in parsed_string:
                    if word.islower() and not word == 'and':
                        lowers_present = True
                        break
                if not lowers_present:
                    longest_name = string
    return longest_name

def get_hosts(tweets):
    all_grams = []
    for tweet in tweets:
        tweet = tweet.split(' ')
        if 'hosted' in tweet:
            i = tweet.index('hosted')
            if tweet[i + 1] == 'by':
                del tweet[i+1]
                tweet[i] = 'hosted by'
        for keyword in host_keywords:
            grams = tw.nGrams(tweet, keyword, 'after')
            grams2 = tw.nGrams(tweet, keyword, 'before')
            all_grams.append(grams)
            all_grams.append(grams2)
    counter = tw.all_intersections(all_grams)
    counter = Counter(el for el in counter.elements() if counter[el] >= 15)
    return choose_host_tie(counter)

def get_presenters(tweets):
    #print("tweets: ", tweets)
    all_grams = []
    potentials = tw.regex_search(regexPresent, tweets)
    
    #print("tweets: ", potentials)
    for tweet in potentials:
        tweet = tweet.split(' ')
        for pair in presenters_keywords:
            if pair[0] in tweet:
                i = tweet.index(pair[0])
                if tweet[i + 1] == pair[1]:
                    del tweet[i+1]
                    tweet[i] = pair[0] + pair[1]
        for keyword in presenter_keywords:
            if keyword == "present" or "presents":
                grams = tw.nGrams(tweet, keyword, 'before')
                #print("do i make it in here")
            else: grams = tw.nGrams(tweet, keyword, 'after')
            all_grams.append(grams)    
        '''
        if 'presented' in tweet:
            i = tweet.index('presented')
            if tweet[i + 1] == 'by':
                del tweet[i+1]
                tweet[i] = 'presented by'
        for keyword in presenter_keywords:
            grams = tw.nGrams(tweet, keyword, 'after')
            #grams2 = tw.nGrams(tweet, keyword, 'before')
            all_grams.append(grams)
           # all_grams.append(grams2)
        '''
    #print("all grams", all_grams)
    counter = tw.all_intersections(all_grams)
    #print("counter: ", counter)
    counter = Counter(el for el in counter.elements() if counter[el] >= 1)
    return choose_host_tie(counter)