import math
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'yUNVJt7FXanj5wV1RUOBQnDlY'
        consumer_secret = 'pjs72BsMIGhmzsTdbd7YNJdAUYSgZQDzPfcc2LZLHHn9zdbKma'
        access_token = '2215814282-XGV9fci1oX8p1Qb03KRJgLXSl7kGdyTV2xRA2l1'
        access_token_secret = 'bOubbtfsq1iTdVQQxGjUB64oELhUfxrSIWCVFmQs45DH7'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

            # Making life easier down the road.
            self.error = None
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+: / {2}/ \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
            self.error = str(e)


def go(tweet):
    # creating object of TwitterClient Class
    api = TwitterClient()
    
    # calling function to get tweets
    tweets = api.get_tweets(query=tweet, count=200)

    positive_percentage = None
    negative_percentage = None
    neutral_percentage = None

    ptweets = None
    ntweets = None
    neutweets = None

    # Some validation.
    if tweets == None:
        # Since the error is already present, just pass.
        pass
    else:
        ptweets = []
        ntweets = []
        neutweets = []

        for tw in tweets:
            if tw['sentiment'] == 'positive':
                # picking positive tweets from tweets
                ptweets.append(tw)
            elif tw['sentiment'] == 'negative':
                # picking negative tweets from tweets
                ntweets.append(tw)
            else:
                # picking neutral tweets from tweets
                neutweets.append(tw)
                
        # percentage of positive tweets
        positive_percentage = round(100 * len(ptweets) / len(tweets), 2)
        print("Positive tweets percentage: {} %".format(positive_percentage))
        
        # percentage of negative tweets
        negative_percentage = round(100 * len(ntweets) / len(tweets), 2)
        print("Negative tweets percentage: {} %".format(negative_percentage))

        # percentage of neutral tweets
        neutral_percentage = round(100 - positive_percentage - negative_percentage, 2)
        print("Neutral tweets percentage: {} % \
            ".format(neutral_percentage))

        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:10]:
            print(tweet['text'])

        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in ntweets[:10]:
            print(tweet['text'])

    return (positive_percentage, ptweets, negative_percentage, ntweets, neutral_percentage, neutweets, api.error)

# if __name__ == "__main__":
#     # calling main function
#     main()
