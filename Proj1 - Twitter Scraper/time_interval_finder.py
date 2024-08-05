import json
import re
from collections import Counter
import tweet_handler
import statistics

INTERVAL = 120000

def load_tweets():
    with open('gg2013.json') as f:
        global tweets
        tweets = json.load(f)[0000:]

def time_finder(awardName):
    awardKeywords = reg_help(awardName)
    load_tweets()
    all_tweets = []
    time_period = []
    for tweet in tweets:
        text = tweet['text']
        text = re.sub(r'#[a-zA-Z]+\b', '', text) #removing hashtags
        text = re.sub(r'\bRT\b', '', text) #removing retweet indicator "RT"

        text = re.sub('@[^\s]+','',text)
        text = re.sub('http[^\s]+','',text)
        key = keyword_match(text, awardKeywords, 0)
        if key:
            all_tweets.append(text)
            time_period.append(tweet["timestamp_ms"])
    return time_period

def reg_help(award):
    remove_list = ['for', 'or', 'in', 'a', 'an']
    std_award = award.lower()
    list_string = std_award.split(" ")
    for word in remove_list:
        if word in list_string:
            list_string.remove(word)
    return list_string



def keyword_match(tweet, keywords, index):
    if index >= len(keywords):
        return True
    curr = keywords[index]
    if tweet.find(curr.lower()) == -1 and tweet.find(curr.capitalize()) == -1:
        return False
    else:
        return keyword_match(tweet, keywords, (index+1))

def get_peak_time(time):
    return statistics.median(time)
    

def get_time_interval_tweets(award, interval):
    time = time_finder(award)
    if time == []:
        return None
    peak = get_peak_time(time)
    relevant_tweets = []
    for t in tweets:
        timestamp = t['timestamp_ms']
        if timestamp > (peak-interval) and timestamp < (peak+interval):
            relevant_tweets.append(t['text'])
    return relevant_tweets


        
if __name__ == "__main__":
    load_tweets()
    tweet_handler.load_tweets()