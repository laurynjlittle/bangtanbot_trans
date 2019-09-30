import tweepy as tp
import datetime
import time
import emoji
import re

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
                        BTS_names = ("JIMIN","JHOPE", "NAMJOON", "RM", "JIN", "JK", "V", "JUNGKOOK", "TAEHYUNG", "SUGA", "YOONGI")
                        if hashtags['text'].upper() in BTS_names:
                            twt = twt
                        #else, translate hashtag and replace back into tweet with no whitespace
                        else:
                            print(hashtags['text'])
                            hashtag_trans = translator.translate(hashtags['text']).text
                            print(hashtag_trans)
                            hashtag_index = hashtags['indices']
                            twt = twt.replace("#" + hashtags['text'],"#" + (hashtag_trans.replace(" ","")))
                            print(twt)
                    #variable replace hashtags so they aren't translated again
                    #match tweet for '#' and add to hashtag list to store, and replace with T + number(T0, T1, etc.), then add back into tweet after translation
                    VAR, REPL = re.compile(r'#(\w+)'), re.compile(r'_H(\d+)_')
                    hashtag_list = []
                    #replace function stores hashtag in list and replaces hashtag in tweet with number
                    def replace(hashtag):
                        hashtag_list.append(hashtag.group())
                        return "_H%d_" %(len(hashtag_list)-1)
                    #restore function returns original hashtag back to tweet where T + number was placed
                    def restore(hashtag):
                        return hashtag_list[int(hashtag.group(1))]
                    twt = VAR.sub(replace, twt)
                    twt_trans = translator.translate(twt, dest = 'en').text
                    twt = REPL.sub(restore, twt_trans)
                    url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
                    api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                    print(twt)
                    print("translated tweet - no problem!")
                #exception code if translation attempt breaks on emojis
                except Exception:
                    print("processing translation exception...")
                    #try to remove emojis then translate then replace emojis before posting
                    try:
                     #remove emoji image and replace with emoji text instead
                        twt = emoji.demojize(twt)
                        #variable replace hashtags so they aren't translated again
                        #match tweet for ':' and add to emoji list to store, and replace with T + number(T0, T1, etc.), then add back into tweet after translation
                        EVAR, EREPL = re.compile(r':(\w+):'), re.compile(r'_E(\d+)_')
                        emoji_list = []
                        #replace function stores emoji text in list and replaces emoji in tweet with number
                        def replace(emoji):
                            emoji_list.append(emoji.group())
                            return "_E%d_" %(len(emoji_list)-1)
                        #restore function returns original emoji text back to tweet where T + number was placed
                        def restore(emoji):
                            return emoji_list[int(emoji.group(1))]
                        twt = EVAR.sub(replace, twt)
                        print(emoji_list)
                        print(twt)
                        twt_trans = translator.translate(twt, dest = 'en').text
                        twt = EREPL.sub(restore, twt_trans)
                        twt = emoji.emojize(twt)
                        #if tweets also has hashtags, then replace & restore as well
                        print(twt)
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
