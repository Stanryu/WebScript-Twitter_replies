# -*- coding:utf-8 -*-

import pymongo


class TBS_bd(object):
    """docstring for TBS_bd."""
    def __init__(self, url = None, porta = None):
        super(TBS_bd, self).__init__()
        self.client = pymongo.MongoClient(url,porta)
        self.db = self.client.tbs_bd_tweets_comments

        ####### Coleções #######
        # self.user = self.db.user
        # self.reply = self.db.reply
        # self.tweet = self.db.tweet

    # def insert_tweet_document(self, message_key, post_text, author_id, data = None):
    #     try:
    #         self.tweet.insert_one({"_id":int(message_key), "post_text":post_text, "author_id":author_id})
    #     except Exception as e:
    #         #print(e)
    #         print("exceção!")
    #         self.tweet.update({"_id":int(message_key)}, {"post_text":post_text, "author_id":author_id})
    #
    #
    # def insert_user(self, id, screen_name):
    #     try:
    #         self.user.insert_one({"_id":int(id), "screen_name":screen_name})
    #     except Exception as e:
    #         #print(e)
    #         print("exceção!")
    #         self.user.update({"_id":int(id)}, {"screen_name":screen_name})
    #
    #
    # def insert_reply(self, reply_text, reply_to,  message_key = None):
    #     try:
    #         self.reply.insert_one({"_id":int(message_key), "reply_text":reply_text, "reply_to":int(reply_to)})
    #     except Exception as e:
    #         #print(e)
    #         print("exceção!")
    #         self.reply.update({"_id":int(message_key)}, {"reply_text":reply_text, "reply_to":int(reply_to)})


    def get_tweets(self, screen_name):
        all_tweets = []
        user_id = None
        myquery = {"screen_name":screen_name}
        tweets = self.user.find(myquery)
        for i in tweets:
            user_id = i["_id"]
            break
        myquery = {"author_id":user_id}
        for i in self.tweet.find(myquery):
            all_tweets.append(i["_id"])

        return all_tweets


    def print_teables(self):
        for i in self.user.find():
            print(i["screen_name"])
            myquery = {"author_id":200}
            for j in self.tweet.find(myquery):
                print(" ->", j["post_text"])
                myquery2 = {"reply_to":j["_id"]}
                for k in self.reply.find(myquery2):
                    print("  -->", k["reply_text"])


if __name__ == '__main__':
    tbs = TBS_bd()
    tbs.insert_tweet(123, "postei e sai correndo", 200)
    tbs.insert_user(200, "petrobras")
    tbs.insert_reply(562, "oi", 123)
    tbs.insert_reply(563, "olá", 123)

    #tbs.print_teables()

    print(tbs.get_tweets("petrobras"))


    tbs.tweet.drop()
    tbs.user.drop()
    tbs.reply.drop()
