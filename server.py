import sys
from flask import Flask, render_template
from tweetie import *
from colour import Color

from numpy import median

app = Flask(__name__)

def add_color(tweets):
    """
    Given a list of tweets, one dictionary per tweet, add
    a "color" key to each tweets dictionary with a value
    containing a color graded from red to green. Pure red
    would be for -1.0 sentiment score and pure green would be for
    sentiment score 1.0.

    Use colour.Color to get 100 color values in the range
    from red to green. Then convert the sentiment score from -1..1
    to an index from 0..100. That index gives you the color increment
    from the 100 gradients.

    This function modifies the dictionary of each tweet. It lives in
    the server script because it has to do with display not collecting
    tweets.
    """
    colors = list(Color("red").range_to(Color("green"), 100))
    
    for t in tweets:
        score = t['score']
        rounded = round(50*(score+1))
        t['color'] = colors[rounded]
    return tweets


@app.route("/favicon.ico")
def favicon():
    """
    Open and return a 16x16 or 32x32 .png or other image file in binary mode.
    This is the icon shown in the browser tab next to the title.
    """
    with open('favicon.png', 'rb') as file:
        favicon = file.read()
    return favicon


@app.route("/<name>")
def tweets(name):
    "Display the tweets for a screen name color-coded by sentiment score"
    tweets = fetch_tweets(api, name)
    twitter = tweets['tweets']
    color = add_color(twitter)
    
    scores = []
    for c in color:
        scores.append(c['score'])
    
    med = median(scores)
    username = name
    return render_template('tweets.html', username = username, med = med, color = color)
    


@app.route("/following/<name>")
def following(name):
    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """
    k = lambda x: x['followers']
    user = sorted(fetch_following(api, name), key = k, reverse=True)
    return render_template('following.html', name = name, user = user)


i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i+1]
api = authenticate(twitter_auth_filename)

#app.run(host='0.0.0.0', port=80)
#app.run()