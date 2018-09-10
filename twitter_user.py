# -*- coding:utf-8 -*-

class User(object):
    """docstring for User."""
    def __init__(self, name):
        super(User, self).__init__()
        self.screen_name = name

    def generate_link_tweet(self, tweet_id):
        url_basic = ['https://twitter.com/','/status/']
        url = url_basic[:]
        url.insert(1,self.screen_name)
        url.append(str(tweet_id))
        url = ''.join(url)
        return url
