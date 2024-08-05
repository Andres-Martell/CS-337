import tweet_handler as th
import hosts as host_handler
import time_interval_finder as interval
from collections import Counter
import re

'''Version 0.35'''

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

award_keywords = ["award", "best", "motion picture", "actor", "actress", "supporting", "comedy", "drama", "musical", "director", "screenplay", "animated", "foreign", "television"]

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    th.load_tweets()
    host_tweets = th.tweet_search(th.host_keywords)
    hosts = host_handler.get_hosts(host_tweets)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    award_names = th.analyze_tweets("award", award_keywords)
    pruned_list = th.prune_awards(award_names)
    awards = pruned_list
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = dict()
    if year == 2013 or year == 2015:
        awards = OFFICIAL_AWARDS_1315
    elif year == 2018 or 2019:
        awards = OFFICIAL_AWARDS_1819
    hosts = get_hosts(year)
    for award in awards: 
        interval_tweets = interval.get_time_interval_tweets(award, th.INTERVAL)
        if interval_tweets:
            award_nominees = nominee_helper(award, interval_tweets, hosts)
            nominees[award] = award_nominees
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = dict()
    if year == 2013 or year == 2015:
        awards = OFFICIAL_AWARDS_1315
    elif year == 2018 or 2019:
        awards = OFFICIAL_AWARDS_1819
    for award in awards: 
        award_tweets = th.universal_tweet_finder(award)
        award_winner = th.get_winners(award_tweets,award)
        winners[award] = award_winner
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

#takes in the relevant time interval tweets and tries to find the most tweeted about people/movies in the given time period
def nominee_helper(award, tweets, hosts):
    PERSON_KEYWORDS = ["actor", "actress", "director", "screenplay"]
    award_nominees = []
    consecutive_capitalized_words = []
    for tweet in tweets: 
        consecutive_capitalized_words.append(list(re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',tweet)))
    if consecutive_capitalized_words:
        complete = sum(consecutive_capitalized_words, [])
    c = Counter(complete)
    if th.check_and_clean_tweet(award,PERSON_KEYWORDS):
        person_award = True
    else:
        person_award = False
    for noun in c.most_common(15):
        if person_award: 
            location = th.NAMESLIST.loc[(th.NAMESLIST['primaryName'] == noun[0])]
            if not location.empty and noun[0] not in hosts:
                award_nominees.append(noun[0])
        else:
            location = th.MOVIESLIST.loc[(th.MOVIESLIST['primaryTitle'] == noun[0])]
            if not location.empty and noun[0] not in hosts:
                award_nominees.append(noun[0])
            else:
                df = th.TVLIST.loc[(th.TVLIST['primaryTitle'] == noun[0])]
                if not df.empty and noun[0] not in hosts:
                    award_nominees.append(noun[0])
    return award_nominees

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    th.load_tweets()

    awards = get_awards(2013)
    nominees = get_nominees(2013)
    print(nominees.values())
    return


if __name__ == '__main__':
    main()

