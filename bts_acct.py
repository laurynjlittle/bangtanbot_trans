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
        #if BTS tweet is newer than the last time bot tweeted, go through nested loop to translate & post
        if last_tweet_time < tweets.created_at:
            #if tweet is in English
            if tweets.lang == 'en':
                print("tweet is in English - no translation needed")
                #if tweet has https link -- img then find index of https to remove from tweet text
                if tweets.text.find("https://") >= 0:
                    txt_b4_img = tweets.text.find("https://")
                    twt = tweets.text[:txt_b4_img]
                    print(twt)
                    url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                    api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                #else, if no https link, post tweet text as-is
                else:
                    twt = tweets.text
                    print(twt)
                    url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                    api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
            #if tweet is not in English, then run translation
            else:
                print("creating BTS translation...")
                print(tweets.text)
                #try to remove https link -- img to clean up tweet to text only
                try:
                    if tweets.text.find("https://") >= 0:
                        txt_b4_img = tweets.text.find("https://")
                        twt = tweets.text[:txt_b4_img]
                    else:
                        twt = tweets.text
                    print(twt)
                    #tweet translates hashtags weird remove and replace with hyphen and then replace back to hashtag
                    for hashtags in tweets.entities["hashtags"]:
                        #if hashtag is BTS name, don't translate
                        if hashtags['text'].upper() in ("Jhope", "Namjoon", "RM", "Jin", "JK", "V", "Jungkook", "Taehyung", "Suga", "Yoongi").upper():
                            twt = twt
                        #else, translate hashtag and replace back into tweet with no whitespace
                        else:
                            hashtag_trans = translator.translate(hashtags['text']).text
                            print(translator.translate(hashtags['text']).text)
                            hashtag_index = hashtags['indices']
                            print(hashtag_index)
                            print(twt[hashtag_index[0]])
                            twt = twt.replace("#" + hashtags['text'],"#" + (hashtag_trans.replace(" ","")))
                    #translate tweet to english and store as new text
                    translation = translator.translate(twt, dest='en')
                    twt = translation.text
                    url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                    api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                    print(twt)
                    print("translated tweet - no problem!")
                    n = n + 1
                #exception code if translation attempt breaks on emojis
                except Exception:
                    print("processing translation exception...")
                    #try to remove emojis then translate then replace emojis before posting
                    try:
                        #remove emoji image and replace with emoji text instead
                        for hashtags in tweets.entities["hashtags"]:
                        #if hashtag is BTS name, don't translate
                        if hashtags['text'].upper() in ("Jhope", "Namjoon", "RM", "Jin", "JK", "V", "Jungkook", "Taehyung", "Suga", "Yoongi").upper():
                            twt = twt
                        #else, translate hashtag and replace back into tweet with no whitespace
                        else:
                            hashtag_trans = translator.translate(hashtags['text']).text
                            print(translator.translate(hashtags['text']).text)
                            hashtag_index = hashtags['indices']
                            print(hashtag_index)
                            print(twt[hashtag_index[0]])
                            twt = twt.replace("#" + hashtags['text'],"#" + (hashtag_trans.replace(" ","")))
                        #remove emojis and store as new text    
                        twt = emoji.demojize(tweets.text[:txt_b4_img])
                        counter = twt.count(":")
                        twt = twt.replace("#", "-")
                        translation = translator.translate(twt, dest="en")
                        twt = emoji.emojize(translation.text)
                        m = 0
                        #for c in range(1, counter+1):
                         #   p = twt[m:].index(":")
                         #   if c % 2 == 0:
                         #       twt = twt[:p + m+1] + " " + twt[p+ m+1:]
                         #       m = p + m+ 1
                         #   else:
                         #       twt = twt[:p + m] + " :" + twt[p + m +2:]
                         #       m = p + m + 2
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
