import tweepy as tp
import datetime
import emoji

consumer_key = "0Mily48PNIlHZ6XpD7xTbIvn3"
consumer_secret = "gIhQdvo2FoI0VgpmtTLxjFWXA0BFmMopIRKmB8HcxcIYh4EuZQ"
access_token = "1173765313323773952-Ngg7n5Hmr2kETxR7NqADJp6nLLIX9M"
access_secret = "aUDKSF9gwDaowjQHxcUyzXp8JPIwLvJArwuguYCDG8haS"

auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

print("creating BTS translation...")

from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.co.kr',
    ])

bts_timeline = api.user_timeline("BTS_twt")
me_timeline = api.user_timeline(1173765313323773952)

n = 0
#last_tweet_time = datetime.datetime(2019,9,18)
last_tweet_time = me_timeline[n].created_at

for tweets in bts_timeline:
    try:
        #if BTS tweet was posted after my last retweet and there is no media file
        if last_tweet_time < tweets.created_at:
            if tweets.entities["urls"] != "":
                txt_b4_img = tweets.text.find("https://")
            else:
                txt_b4_img = len(tweets.text)
            no_pic_twt = tweets.text[:txt_b4_img]
            twt = no_pic_twt.replace("#", "-")
            translation = translator.translate(twt, dest='en')
            twt = translation.text
            twt = twt.replace("-", "#")
            twt = twt.replace("# ", "#")
            url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
            api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
        n = n + 1
    except Exception:
        #handle emojis in tweets that break translation
        print("processing translation exception...")
        if tweets.entities["urls"] != "":
            txt_b4_img = tweets.text.find("https://")
        else:
            txt_b4_img = len(tweets.text)
        new = emoji.demojize(tweets.text[:txt_b4_img])
        twt = new.replace("#", "-")
        translation = translator.translate(twt, dest="en")
        new1 = emoji.emojize(translation.text)
        twt = new1.replace("-", "#")
        twt = new1.replace("# ", "#")
        url = "https://twitter.com/BTS_twt/status/" + str(tweets.id)
        api.update_status('@BTS_twt #BotTranslation: ' + twt, tweets.id, attachment_url= url)
    if tweets.favorited is False:
        tweets.favorite()


#btstweet = (str(bts_timeline[0].id) + ' - ' + bts_timeline[0].text)
#print (str(bts_timeline[0].id) + ' - ' + bts_timeline[0].text)

#n = 0

#print api.entities.get('hashtags')

#translation = translator.translate(twt, dest='en')

#url = "https://twitter.com/BTS_twt/status/" + str(bts_timeline[n].id)
#api.update_status("Translation: " + translation.text,bts_timeline[1].id)
#api.update_status('@BTS_twt Translation: ' + translation.text, bts_timeline[1].id, attachment_url= url)
