# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from twitter_user import User
from timeline_twitter import save_timeline
from tbs_db import*
from comments import*

### List of perfils - twitter ###
#user_list = {"petrobras":{}, "tilibra_oficial":{}, "cocacola_br":{}, "netflixbrasil":{}, "acerdobrasil":{}, "philco_brasil":{}}
#user_list = ["Petrobras", "lucianohuck", "danilogentili", "cocacola_br", "10ronaldinho", "pontofrio", "accenture_br"]
user_list = ["oboticario"]

### Open Mongo Data base
tbs = TBS_bd()



#driver = webdriver.Firefox(executable_path=r'C:\Program Files\WebDriversSelenium\geckodriver.exe')
driver = webdriver.PhantomJS(executable_path=r'C:\Program Files\WebDriversSelenium\phantomjs-2.1.1-windows\bin\phantomjs.exe')

### For user of list - Get tweets with replies
for user in user_list:
    ### create collection on Data Base with name of user ###
    empresa = tbs.db[user]

    ### Get all tweets of user
    ### each tweet in all_tweets is a document with informations about it
    all_tweets = save_timeline(user)

    print(user+" - tweets: "+str(len(all_tweets)))
    temp = User(user)

    ### For each tweet, get all replies.
    for tweet in all_tweets:
        link = temp.generate_link_tweet(tweet["_id"])
        driver.get(link)
        replies = get_comments(driver)

        ### Format the replies to utf-8
        for index, reply in enumerate(replies):
            replies[index] = replies[index].text.encode('utf-8', 'ignore')

        ### Add replies to document with _id equals id of tweet ###
        tweet["replies"] = replies

        ######### Insert Document tweet in collection of Twitter user referenced #########
        try:
            empresa.insert_one(tweet)
        except Exception as e:
            empresa.update_one(
                {"_id":int(tweet["_id"])},
                {"$set":tweet}
            )
        break




    print(tbs.db.name)
    print(tbs.db.list_collection_names())


driver.close()
