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
def translate_BTS():
    print("creating BTS translation...")

    bts_timeline = api.user_timeline("BTS_twt")
    me_timeline = api.user_timeline(1173765313323773952)

    n = 0
    #last_tweet_time = datetime.datetime(2019,9,10)
    last_tweet_time = me_timeline[n].created_at


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
                print("processing translation exception...")
                if tweets.entities["urls"] != "":
                    txt_b4_img = tweets.text.find("https://")
                else:
                    txt_b4_img = len(tweets.text)
                twt_tx = emoji.demojize(tweets.text[:txt_b4_img])
                print(twt_tx)
                twt = twt_tx.replace("#", "-")
                translation = translator.translate(twt, dest="en")
                new1 = emoji.emojize(translation.text)
                twt = new1.replace("-", "#")
                twt = new1.replace("# ", "#")
                url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                print(twt)
                print("translated exception!")
        if tweets.favorited is False:
            tweets.favorite()

while True:
    translate_BTS()
    time.sleep(500)
