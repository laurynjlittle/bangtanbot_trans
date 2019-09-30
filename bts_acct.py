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
                    #remove emoji characters from tweet
                    twt = emoji.demojize(twt)
                    #tweet translates hashtags weird, translate hashtags individually and replace back into tweet
                    for hashtags in tweets.entities["hashtags"]:
                        #if hashtag is BTS name, don't translate
                        BTS_names = ("JIMIN","JHOPE", "NAMJOON", "RM", "JIN", "JK", "V", "JUNGKOOK", "TAEHYUNG", "SUGA", "YOONGI")
                        if hashtags['text'].upper() in BTS_names:
                            twt = twt
                        #else, translate hashtag and replace back into tweet with no whitespace
                        else:
                            hashtag_trans = translator.translate(hashtags['text']).text
                            hashtag_index = hashtags['indices']
                            twt = twt.replace("#" + hashtags['text'],"#" + (hashtag_trans.replace(" ","")))
                            print(twt)
                    #variable replace hashtags and emojis so they aren't translated
                    #match tweet for '#' or ":" and add to hashtag/emoji list to store, and replace with H or E + number(H0, H1, etc.), then add back into tweet after translation
                    HVAR, HREPL = re.compile(r'#(\w+)'), re.compile(r'_H(\d+)_') #replace/restore for hashtag
                    EVAR, EREPL = re.compile(r':(\w+):'), re.compile(r'_E(\d+)_') #replace/restore for emojis
                    hashtag_list = []
                    emoji_list = []
                    #replace function stores hashtag in list and replaces with H0, H1, etc.
                    def h_replace(hashtag):
                        hashtag_list.append(hashtag.group())
                        return "_H%d_" %(len(hashtag_list)-1)
                    #restore function returns original hashtag back to tweet where H + number was placed
                    def h_restore(hashtag):
                        return hashtag_list[int(hashtag.group(1))]
                    #replace function stores emoji text in list and replaces emoji in tweet with E0, E1, etc.
                    def emoji_replace(emoji):
                        emoji_list.append(emoji.group())
                        return "_E%d_" %(len(emoji_list)-1)
                    #restore function returns original emoji text back to tweet where E + number was placed
                    def emoji_restore(emoji):
                        return emoji_list[int(emoji.group(1))]
                    #replace hashtag/emoji with placeholder text that wont be translated
                    twt = HVAR.sub(h_replace, twt)
                    twt = EVAR.sub(emoji_replace, twt)
                    #translate tweet, ignoring placeholders for emoji and hashtags
                    twt_trans = translator.translate(twt, src='ko', dest = 'en').text
                    #return tweet to normal and replace emoji/hashtags back from placeholders
                    twt = HREPL.sub(h_restore, twt_trans)
                    twt = EREPL.sub(emoji_restore, twt_trans)
                    #add emojis characters back to tweet
                    twt = emoji.emojize(twt)
                    url = ("https://twitter.com/BTS_twt/status/" + str(tweets.id))
                    #api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
                    print(twt)
                    print("translated tweet - no problem!")
                except exception:
                    print("error tweeting - try again")
             
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
