import tweepy as tp
import datetime
import time
import emoji

consumer_key = "0Mily48PNIlHZ6XpD7xTbIvn3"
consumer_secret = "gIhQdvo2FoI0VgpmtTLxjFWXA0BFmMopIRKmB8HcxcIYh4EuZQ"
access_token = "1173765313323773952-Ngg7n5Hmr2kETxR7NqADJp6nLLIX9M"
access_secret = "aUDKSF9gwDaowjQHxcUyzXp8JPIwLvJArwuguYCDG8haS"

auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

from googletrans import Translator
translator = Translator()
from langdetect import detect

bts_timeline = api.user_timeline("BTS_twt")
me_timeline = api.user_timeline(1173765313323773952)

n = 0
last_tweet_time = me_timeline[n].created_at

def translate_BTS():
    for tweets in reversed(bts_timeline):
        twt_id = tweets.id
        if last_tweet_time < tweets.created_at:
            #if tweet is in English
            if detect(tweets.text) == 'en':
                print("tweet is in English - no translation needed")
                if tweets.entities["urls"] != "":
                    txt_b4_img = tweets.text.find("https://")
                    twt = tweets.text[:txt_b4_img]
                    print(twt)
                else:
                    txt_b4_img = len(tweets.text)
                    twt = tweets.text[:txt_b4_img]
                    print(twt)
            #if tweet is not in English
            else:
                print("creating BTS translation...")
                try:
                    if tweets.entities["urls"] != "":
                        txt_b4_img = tweets.text.find("https://")
                    else:
                        txt_b4_img = len(tweets.text)
                    twt = tweets.text[:txt_b4_img]
                    print(twt)
                    twt = twt.replace("#", "-")
                    translation = translator.translate(twt, dest='en')
                    twt = translation.text
                    twt = twt.replace("-", "#")
                    twt = twt.replace("# ", "#")
                    url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                    #api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                    print(twt)
                    print("translated tweet - no problem!")
                    n = n + 1
                except Exception:
                    print("processing translation exception...")
                    try:
                        twt = emoji.demojize(tweets.text[:txt_b4_img])
                        counter = twt.count(":")
                        print(twt)
                        twt = twt.replace("#", "-")
                        translation = translator.translate(twt, dest="en")
                        print (twt)
                        twt = emoji.emojize(translation.text)
                        m = 0
                        for c in range(1, counter+1):
                            p = twt[m:].index(":")
                            if c % 2 == 0:
                                twt = twt[:p + m+1] + " " + twt[p+ m+1:]
                                m = p + m+ 1
                            else:
                                twt = twt[:p + m] + " :" + twt[p + m +2:]
                                m = p + m + 2
                        print(twt)
                        twt = emoji.emojize(twt)
                        twt = twt.replace("-", "#")
                        twt = twt.replace("# ", "#")
                        url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                        #api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                        print(twt)
                        print("translated exception!")
                    except Exception:
                        print("error")

def like_BTS():
    for tweets in bts_timeline:
        if tweets.favorited is False:
            tweets.favorite()            

while last_tweet_time < bts_timeline[0].created_at:
    translate_BTS()
    like_BTS()
    time.sleep(3600)
else:
    print("no new BTS tweets :(")
    time.sleep(3600)
