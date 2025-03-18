import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime


def loadkeys(filename):
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    consumer_key, consumer_secret, access_token, access_token_secret = loadkeys(twitter_auth_filename)
    
    authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authentication.set_access_token(access_token, access_token_secret)
    return tweepy.API(authentication, wait_on_rate_limit=True)


def fetch_tweets(api, name):
    twts = api.user_timeline(screen_name = name, count = 100, tweet_mode = 'extended')
    tweets = list()
    analyzer = SentimentIntensityAnalyzer()
    
    for twt in twts:
        t_dict = dict()
        t_dict['id'] = twt.id
        t_dict['created'] = twt.created_at
        t_dict['retweeted'] = twt.retweet_count
        t_dict['text'] = twt.full_text
        t_dict['hashtags'] = twt.entities['hashtags']
        t_dict['urls'] = twt.entities['urls']
        t_dict['mentions'] = twt.entities['user_mentions']
        t_dict['score'] = analyzer.polarity_scores(twt.full_text)['compound']
        tweets.append(t_dict)
    
    d = {'user': name,
         'count': len(tweets),
         'tweets': tweets}
    
    return d


def fetch_following(api,name):
    identify = api.friends(name, count=100)
    follow = list()
    for fol in identify:
        d = dict()
        d['name'] = fol.name
        d['screen_name'] = fol.screen_name
        d['followers'] = fol.followers_count
        d['created'] = datetime.strftime(fol.created_at, '%Y-%m-%d')
        d['image'] = fol.profile_image_url
        follow.append(d)
    return follow