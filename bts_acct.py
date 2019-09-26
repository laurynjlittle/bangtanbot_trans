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
translator = Translator(service_urls=[
      'translate.google.co.kr',
    ])

bts_timeline = api.user_timeline("BTS_twt")
me_timeline = api.user_timeline(1173765313323773952)

n = 0
#last_tweet_time = datetime.datetime(2019,9,10)
last_tweet_time = me_timeline[n].created_at

def emojis_BTS():
    #handle emojis in tweets that break translation
    print("processing translation exception...")
    for tweets in reversed(bts_timeline):
        if last_tweet_time < tweets.created_at:
            try:
                if tweets.entities["urls"] != "":
                    txt_b4_img = tweets.text.find("https://")
                else:
                    txt_b4_img = len(tweets.text)
                twt = emoji.demojize(tweets.text[:txt_b4_img])
                print(twt)
                counter = twt.count(":")
                twt = twt_tx.replace("#", "-")
                translation = translator.translate(twt, dest="en")
                twt = emoji.emojize(translation.text)
                m = 0
                for c in range(1, counter+1):
                    p = twt[m:].index(":")
                    if c % 2 == 0:
                        twt = twt[:p + m+1] + twt[p+ m+1:]
                        m = p + m+ 1
                    else:
                        twt = twt[:p + m] + " :" + twt[p + m +2:]
                        m = p + m + 2
                print(twt)
                twt = emoji.emojize(twt)
                twt = twt.replace("-", "#")
                twt = twt.replace("# ", "#")
                url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                print(twt)
                print("translated exception!")
            except Exception:
                print("error")

def translate_BTS():
    print("creating BTS translation...")

    for tweets in reversed(bts_timeline):
        if last_tweet_time < tweets.created_at:
        #if BTS tweet was posted after my last retweet and there is no media file
            try:
                if tweets.entities["urls"] != "":
                    txt_b4_img = tweets.text.find("https://")
                else:
                    txt_b4_img = len(tweets.text)
                twt_tx = tweets.text[:txt_b4_img]
                print(twt_tx)
                twt = twt_tx.replace("#", "-")
                translation = translator.translate(twt, dest='en')
                twt = translation.text
                twt = twt.replace("-", "#")
                twt = twt.replace("# ", "#")
                url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                print(twt)
                print("translated tweet - no problem!")
                n = n + 1
            except Exception:
            #handle emojis in tweets that break translation
                  emojis_BTS()

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
