import json 
import re
from collections import Counter
import hosts as host
import gg_api


win_keywords = ["win", "won", "award", "nominee", "best", "nominated", "goes to", "Golden Globe", "host"]
award_keywords = ["award", "best", "motion picture", "actor", "actress", "supporting", "comedy", "drama", "musical", "director", "screenplay", "animated", "foreign", "television"]
host_keywords = ['hosts', 'host', 'hosted by', 'hosting']
nomination_keywords = ['nominees', 'nominated', 'nominations', 'nomination']
tweets = []

def load_tweets():
    with open('gg2013.json') as f:
        tweetsJSON = json.load(f)[0000:]
        for tweet in tweetsJSON:
            text = tweet['text']
            text = re.sub(r'#\b', '', text) #removing hashtags
            text = re.sub(r'\bRT\b', '', text) #removing retweet indicator "RT"
            text = re.sub(r'\bGoldenGlobes\b', '', text)

            text = re.sub('@[^\s]+','',text)
            text = re.sub('http[^\s]+','',text)
            tweets.append(text)

#Given tweets, most likely already sorted by awards, and a rule for what to search for, return matches
def regex_search(rule, tweets):
    matches = []
    for tweet in tweets:
        searching = re.search(rule, tweet)
        if searching:
            matches.append(tweet)
    return matches

def tweet_search(keywords):
    all_tweets = []
    for tweet in tweets:
        clean_tweet = check_and_clean_tweet(tweet, keywords)
        if clean_tweet:
            if not clean_tweet in all_tweets:
                all_tweets.append(clean_tweet)
    return all_tweets

#Checks if tweet has relevant information and is long enough to be helpful
#Cleans tweet of useless information
def check_and_clean_tweet(text, keywords):
    if len(text) < 5: return False
    #print("text: ", text)
    #print("ketwords: ", keywords)
    if not any(map(text.__contains__,keywords)):
        return False
    text = re.sub(r'#[a-zA-Z]+\b', '', text) #removing hashtags
    text = re.sub(r'\bRT\b', '', text) #removing retweet indicator "RT"

    #reagan added this in: 2/3 12:16. Takes away usernames and links
    text = re.sub('@[^\s]+','',text)
    text = re.sub('http[^\s]+','',text)
    
    return text


def analyze_tweets(search_word, keywords):
    test_tweets = tweets[:]
    ngrams = []
    awards = []
    for i, tweet in enumerate(test_tweets):
        updated = check_and_clean_tweet(tweet, keywords)
        if updated:
            award = get_award_name(updated)
            if award: awards.append(award)
            #b = nGrams(updated.split(" "), search_word, "before")
            #if b: ngrams.append(b[len(b)-1])
            #a = nGrams(updated.split(" "), search_word, "after")
            #if a: ngrams.append(a[len(a)-1])
    #print(ngrams)
    awards = award_cleaner(awards,2)
    return awards
   # print(all_intersections(ngrams))


#finds the name of an award by finding the index of "goes to" and "best" and returns the substring between these indexes 
def get_award_name(text):
    if "goes to" in text:
        try:
            end = text.index('goes to')
        except: 
            return
        try:
            begin = text.index("best")
        except:
            try:
                begin = text.index("Best")
            except:
                return
        return text[begin:end]


#takes out repeats of awards, and only includes awards that have been mentioned over a certain threshold
def award_cleaner(awards, threshold):
    c = Counter(awards)
    cleaned_awards = []
    for item in c:
        if c[item] > threshold:
            cleaned_awards.append(item)
    return cleaned_awards
        

#Creates list of nGrams
#Tweet: List of strings
#startWord: Key word to begin from, such as "won", "goes to", etc
#rule: can take 'before' or 'after', looking either before or after the startWord's index
def nGrams(tweet, startWord, rule):
    try:
        i = tweet.index(startWord)
    except:
        return []#startword not in the tweet so move on
    if i < 0:
        return []
    grams = []

    #nGrams of words before
    if rule == 'before':
        currBefore = ''
        if i - 1 > 0:
            for j in range(0, i):
                word = tweet[i - 1 - j]
                if not currBefore == '':
                    currBefore = word + ' ' + currBefore
                else:
                    currBefore = word
                grams.append(currBefore)
        
    #nGrams of words after
    elif rule == 'after':
        currAfter = ''
        if i + 1 < len(tweet):
            for k in range(i + 1, len(tweet)):
                word = tweet[k]
                if not currAfter == '':
                    currAfter = currAfter + ' ' + word
                else:
                    currAfter = word
                grams.append(currAfter)
    return grams



# Takes in list of lists of strings, and 
# returns counter
def all_intersections(grams):
    #print("is grams empty here? ", len(grams))
    #print("grams: ", grams)
    completeList = sum(grams, [])
    counter = Counter(completeList)
    #print("complete list: ", completeList)
    return counter

#startWord: the most common word in the nGram (aka: 'Cristoph')
#tweet: list of strings representing one tweet
#returns string beginning with startword and appending any words starting with a capital letter
def stop_at_capitals(startWord, tweet):
    final_name = startWord
    start_index = tweet.index(startWord)
    noLowers = True
    while(noLowers and start_index < len(tweet) - 1):
        start_index += 1
        if tweet[start_index][0].isupper():
            final_name = final_name + tweet[start_index]
        else:
            noLowers = False
    return final_name



def choose_winner_tie(counter):
    '''
    uncleaned_winner = host.choose_host_tie(counter)
    res = re.sub(r'[^\w\s]', '', uncleaned_winner)
    return res


    '''
    longest_word = ''
    highest_value = 0
    #print("counter: ", counter)
    for x in counter:
        key = x
        value = counter[x]
        if not key == '':
            if value > highest_value:
                highest_value = value
                longest_word = key
            elif value == highest_value:
                if len(longest_word) < len(key):
                    longest_word = key
    return longest_word
    
                

def get_winners(tweets, awardName):
    #for each tweet, get the n gram for goes to, append to list of n gram, and then return counter
    all_grams = []
    for tweet in tweets:
        tweet = tweet.split(' ')
        if 'goes' in tweet:
            i = tweet.index('goes')
            if tweet[i + 1] == 'to':
                del tweet[i+1]
                tweet[i] = 'goes to'
        if 'took' in tweet:
            i = tweet.index('took')
            if tweet[i + 1] == 'home':
                del tweet[i+1]
                tweet[i] = 'took home'
        
        grams = nGrams(tweet, 'goes to', 'after')
        grams2 = nGrams(tweet, 'won', 'before')
        grams3 = nGrams(tweet, 'wins', 'before')
        grams4 = nGrams(tweet, 'took home', 'before')
        all_grams.append(grams)
        all_grams.append(grams2)
        all_grams.append(grams3)
        all_grams.append(grams4)
    counter = all_intersections(all_grams)
    winners = choose_winner_tie(counter)
    if winners == '':
        #print("Counter: ", counter)
        return False
    else: return winners

#Given a list of tweets (strings) about a given awards, and the awardName, return list of likely nominees for that award
def get_nominees(awardTweets, awardName):
    #awardTweets = tweet_search(awardName)
    '''
    all_grams = []
    for tweet in awardTweets:
        tweet = tweet.split(' ')
            #print("tweet: ", tweet)
            #print("keyword: ", keyword)
            grams = nGrams(tweet, keyword, 'after')
            grams2 = nGrams(tweet, keyword, 'before')
            all_grams.append(grams)
            all_grams.append(grams2)
    #print("is all grmas empty: ", len(all_grams))
    counter = all_intersections(all_grams)
    return counter
    '''
    print("what is this holdup")
    regexNom = re.compile('[nN]omin(ated|ees|ee|ations|ation)')
    potentials = regex_search(regexNom, awardTweets)
    all_grams = []
    for tweet in potentials:
        tweet = tweet.split(' ')
        for keyword in nomination_keywords:
            grams = nGrams(tweet, keyword, 'after')
            grams2 = nGrams(tweet, keyword, 'before')
            all_grams.append(grams)
            all_grams.append(grams2)
    counter = all_intersections(all_grams)
    counter = Counter(el for el in counter.elements() if counter[el] >= 15)
    return counter

    #print(potentials)


def prune_awards(awards_list):
    remove_list = ['for', 'or', 'in', 'a', 'an', 'of']
    final_list = []
    standards = []
    for award in awards_list:
        std_award = award.lower()
        list_string = std_award.split(" ")
        for word in remove_list:
            if word in list_string:
                list_string.remove(word)
        std_award = ''.join(list_string)

        pattern = re.compile('\W')
        std_award = re.sub(pattern, '', std_award)

        if not std_award in standards:
            final_list.append(award)
            standards.append(std_award)
    return final_list

# Takes in one award name, and returns a list of lists of strings
# Ideally should, given an awards name such as "Best actor in a motion picture drama", returned list
# such as [best", "actor", "motion", "picture", "drama"].
# All strings returned will be lower case
def reg_help(award):
    remove_list = ['for', 'or', 'in', 'a', 'an', '-']
    std_award = award.lower()
    list_string = std_award.split(" ")
    for word in remove_list:
        if word in list_string:
            list_string.remove(word)
    return list_string

# given a tweet, a list of keywords, and a starting index, returns boolean of whether all 
# keywords are present in a tweet
def keyword_match(tweet, keywords, index):
    if index >= len(keywords):
        return True
    curr = keywords[index]
    if tweet.find(curr.lower()) == -1 and tweet.find(curr.capitalize()) == -1:
        return False
    else:
        return keyword_match(tweet, keywords, (index+1))

# Using the recursive helper function keyword_match, and reg_help, 
# the function takes in one awardName, and returns a list of tweets related to it
def universal_tweet_finder(awardName):
    awardKeywords = reg_help(awardName)
    all_tweets = []
    for text in tweets:
        if keyword_match(text, awardKeywords, 0):
            all_tweets.append(text)
            tweets.remove(text)
    return all_tweets




if __name__ == "__main__":
    load_tweets()
    print("where am i slowing down?")
    award_names = analyze_tweets("award", award_keywords)
    #award_names = gg_api.OFFICIAL_AWARDS_1315
    print("here 1?")
    awardDict = dict()
    #print("how many awards do we have: ", len(award_names))
    '''
    pruned_list = prune_awards(award_names)
    award_names = pruned_list
    '''
    award_names.sort(key=len, reverse=True)
    winners_found = 0
    
    for award in award_names:
        relevant_tweets = universal_tweet_finder(award)
        awardDict[award] = relevant_tweets
        
        winners = get_winners(awardDict[award], award)
        if winners:
            winners_found +=1
            print("Winner of ", award, ": ", get_winners(awardDict[award], award))
        else:
            '''
            del awardDict[award]
            index = award_names.index(award)
            del award_names[index]
            '''
            pass
            #print('NO WINNER FOUND FOR ', award)
    print(winners_found, " out of ", len(award_names))
    '''
    testAward = 'cecil b. demille award'
    testAwardTweets = universal_tweet_finder(testAward)
    winners = get_winners(testAwardTweets, testAward)
    print(winners)
    '''

    '''
    print("before or after tweet_search")
    testAward = award_names[1]
    testAwardTweets = universal_tweet_finder(testAward)
    print(len(testAwardTweets))
    print("after tweet search?")
    print("testAward: ", testAward)

    print("nominees: ", get_nominees(testAwardTweets, testAward))
    '''
    #host_tweets = tweet_search(host_keywords)
    #hosts = host.get_hosts(host_tweets)
