#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import pandas as pd
import configparser


def save_timeline(screen_name):

    config = configparser.ConfigParser()
    config.read("tweepy.ini")

    #Twitter API credentials
    consumer_key = config['consumer']['consumer_key']
    consumer_secret = config['consumer']['consumer_secret']
    access_key = config['access']['access_key']
    access_secret = config['access']['access_secret']

    config = configparser.ConfigParser()
    config.read('tweepy.ini')

    #Twitter only allows access to a users most recent 3240 tweets with this method


    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1



    tweets = []
    for tweet in alltweets:
        tweets.append({
        'original_post_id': tweet.in_reply_to_status_id_str,
        'location': tweet.user.location,
        'screen_name': tweet.user.screen_name,
        'geo': tweet.geo,
        'source': tweet.source,
        'userid': tweet.user.id_str,
        'shares':tweet.retweet_count,
        'likes':tweet.favorite_count,
        '_id':int(tweet.id_str),
        'text':tweet.text.encode('utf-8').strip(),
        'created_at':str(tweet.created_at)})




    #df = pd.DataFrame(tweets)
    #df['data'] = df['created_at'].str[0:10]
    #name = tweet.user.screen_name
    #df.to_csv("output/tweets_conta_" + name + ".csv", sep=',', encoding='utf-8')


    print("Timeline " + screen_name + " gravada com sucesso!!!")
    return tweets
