from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from random import random


import sys
import time
from twitter.api import TwitterHTTPError
from urllib.error import URLError
from http.client import BadStatusLine
import pandas as pd
import json 
from params import Parameters as params
import pickle
import sklearn
# To make it more readable, lets store
# the OAuth credentials in strings first.

from twitter import *


loaded_model = pickle.load(open('model.sav','rb'))
CONSUMER_KEY = params.keys['API_keys']
CONSUMER_SECRET = params.keys['API_secret_key']
OAUTH_TOKEN = params.keys['Access_token']
OAUTH_TOKEN_SECRET = params.keys['Access_token_secret']
auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
t = Twitter(auth=auth)

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
        if e.e.code == 401:
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered %i Error. Retrying in %i seconds' % (e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0
    while True:
        try:
            return twitter_api_func(*args, **kw)
        except TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

# This will let us create new partial
# functions with arguments set to 
# certain values.
from functools import partial

# This was maxint.
# There is no longer a maxint (in Python 3)
from sys import maxsize


def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                                friends_limit=maxsize, followers_limit=maxsize):
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    # You can also do this with a function closure.
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids,
                                count=15000)
   # get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids,
    #                            count=15000)
    friends_ids= []
    for twitter_api_func, limit, ids, label in [
            [get_friends_ids, friends_limit, friends_ids, "friends"]
            ]:
        #LOOK HERE! This little line is important.
        if limit == 0: continue
        cursor = -1
        while cursor != 0:
            # Use make_twitter_request via the partially bound callable...
            if screen_name:
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)
            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),
                    label, (user_id or screen_name), file=sys.stderr))
            if len(ids) >= limit or response is None:
                break
    # Do something useful with the IDs, like store them to disk...
    return friends_ids[:friends_limit]
following_oliver = following_meyers = following_colbert=following_sambee = following_hannity = following_tucker=following_maddow = following_tapper = following_cooper=following_lindsay= following_cruz = following_mitch=following_ryan=following_bernie=following_warren= following_kamala = following_beto=following_dogs=following_rowling=following_james=following_musk=0
import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

#john oliver,seth meyers, colbert,sam bee
user = api.get_user(screen_name = 'iamjohnoliver')
user_oliver=user.id #oliver
user = api.get_user(screen_name = 'LastWeekTonight')
user_oliver_show=user.id #oliver_show

user = api.get_user(screen_name = 'StephenAtHome')
user_colbert=user.id #cobert
user = api.get_user(screen_name = 'colbertlateshow')
user_colbert_show=user.id #cobert_show

user = api.get_user(screen_name = 'sethmeyers')
user_meyers=user.id #meyers
user = api.get_user(screen_name = 'LateNightSeth')
user_meyers_show =user.id #meyers_show

user = api.get_user(screen_name = 'iamsambee')
user_sambee=user.id #sambee
user = api.get_user(screen_name = 'FullFrontalSamB')
user_sambee_show=user.id #sambee_show
#news-hannity, tucker carlson, rachel maddow, tapper, cooper
user = api.get_user(screen_name = 'jaketapper')
user_tapper=user.id 
user = api.get_user(screen_name = 'TheLeadCNN')
user_tapper_show=user.id 

user = api.get_user(screen_name = 'seanhannity')
user_hannity=user.id 
user = api.get_user(screen_name = 'TuckerCarlson')
user_carlson=user.id 
user = api.get_user(screen_name = 'maddow')
user_maddow=user.id

user = api.get_user(screen_name = 'andersoncooper')
user_cooper=user.id 
user = api.get_user(screen_name = 'AC360')
user_cooper_show=user.id 
#lindsay graham,ted cruz, leader mitch mcconel, paul ryan
user = api.get_user(screen_name = 'LindseyGrahamSC')
user_graham=user.id 
user = api.get_user(screen_name = 'tedcruz')
user_cruz=user.id 
user = api.get_user(screen_name = 'senatemajldr')
user_mitch=user.id 
user = api.get_user(screen_name = 'SpeakerRyan')
user_ryan=user.id 
#bernie, elizabeth warren,kamala harris, beto rourke
user = api.get_user(screen_name = 'BernieSanders')
user_bernie=user.id 
user = api.get_user(screen_name = 'SenWarren')
user_warren=user.id 
user = api.get_user(screen_name = 'KamalaHarris')
user_kamala=user.id 
user = api.get_user(screen_name = 'BetoORourke')
user_beto=user.id 
# weratedogs, j k rowling, lebron james, elon musk
user = api.get_user(screen_name = 'dog_rates')
user_doggo=user.id 
user = api.get_user(screen_name = 'jk_rowling')
user_rowling=user.id 
user = api.get_user(screen_name = 'KingJames')
user_james=user.id 
user = api.get_user(screen_name = 'elonmusk')
user_elon=user.id 

#end twitter requests



#create one more plot
#source = ColumnDataSource(data=dict(x=x, y=y))




#put a text field
def my_text_input_handler(new):
    user = api.get_user(screen_name = new)
    user_id=user.id
    for i in [user_id]:
        friends_ids = get_friends_followers_ids(t,
                                    user_id=int(i))
        if user_graham in friends_ids :
            following_lindsay = 1
        else:
            following_lindsay=0
        if user_cruz in friends_ids :
            following_cruz = 1
        else:
            following_cruz=0
        if user_mitch in friends_ids :
            following_mitch = 1
        else:
            following_mitch=0
        if user_ryan in friends_ids :
            following_ryan = 1
        else:
            following_ryan=0
        if user_colbert in friends_ids or user_colbert_show in friends_ids :
            following_colbert = 1
        else:
            following_colbert=0

        if user_oliver in friends_ids or user_oliver_show in friends_ids :
            following_oliver = 1
        else:
            following_oliver=0

        if user_meyers in friends_ids or user_meyers_show in friends_ids:
            following_meyers = 1
        else:
            following_meyers=0
        if user_sambee in friends_ids or user_sambee_show in friends_ids:
            following_sambee = 1
        else:
            following_sambee=0

        if user_hannity in friends_ids:
            following_hannity=1
        else:
            following_hannity = 0
        if user_carlson in friends_ids :
            following_tucker = 1
        else:
            following_tucker =0
        if user_maddow in friends_ids :
            following_maddow = 1
        else:
            following_maddow=0
        if user_tapper in friends_ids or user_tapper_show in friends_ids :
            following_tapper = 1
        else:
            following_tapper=0
        if user_cooper in friends_ids or user_cooper_show in friends_ids:
            following_cooper=1
        else:
            following_cooper = 0

        if user_bernie in friends_ids:
            following_bernie=1
        else:
            following_bernie = 0
        if user_warren in friends_ids :
            following_warren = 1
        else:
            following_warren =0
        if user_kamala in friends_ids :
            following_kamala = 1
        else:
            following_kamala=0
        if user_beto in friends_ids :
            following_beto = 1
        else:
            following_beto=0

        if user_doggo in friends_ids:
            following_dogs=1
        else:
            following_dogs = 0
        if user_rowling in friends_ids :
            following_rowling = 1
        else:
            following_rowling =0
        if user_james in friends_ids :
            following_james = 1
        else:
            following_james=0
        if user_elon in friends_ids :
            following_musk = 1
        else:
            following_musk=0
    #df = pd.DataFrame(columns=['ID','oliver','meyers','colbert','sambee','hannity','carlson','maddow','tapper','cooper','lindsay','cruz','mitch','paulryan','berie','warren','kamala','beto'])    
        df = pd.DataFrame([[i, following_oliver,following_meyers,following_colbert,following_sambee,following_hannity,following_tucker,following_maddow,following_tapper,following_cooper,following_lindsay,following_cruz,following_mitch,following_ryan,following_bernie,following_warren,following_kamala,following_beto,following_dogs,following_rowling,following_james,following_musk]], columns=['ID','oliver','meyers','colbert','sambee','hannity','carlson','maddow','tapper','cooper','lindsay','cruz','mitch','paulryan','berie','warren','kamala','beto','ratedogs','rowling','james','elonmusk'])
    df=df.drop(columns=['ID'])
    res = loaded_model.predict(df)
    
    return res[0]

@app.route("/")
def home():
    return "hello"
    
@app.route("/t", methods=['POST'])
def get_data():
    data = request.json
    val  = 'harshdsdh'
    data1 = str(data['body'])
    print((data1))
    print((val))
    if val==data1:
        print("twter")
    else:
        print("thumbss")
        
    value = my_text_input_handler(data1)
    print(value)
    #response= make_response()
    response = jsonify({"statusCode": 200,"status": "Prediction made", "result": "Prediction: " + str(value) })
    #response.headers.add('Access-Control-Allow-Origin', '*')
    return str(value)
    
    


if __name__ == "__main__":
    app.run(debug=True)
 