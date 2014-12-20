from twitter import *
import json


api_key = "aJbjcTTu4Hf7otelyWtqiMR1n"
api_secret = "m2Brlj4xHJdLjD7ou15iRLnOsBJd9Lcx0D3C9CoFxsfUBW3fPB"
access_token = "210245671-w3OXRa58ixgejpwfm3kbHYNWbmS0MokXmfVCVq1I"
access_secret = "P1ZivrAE2plbA7oWiZkCUlk6xNaBCAk0ouk9V9GTJ8RqM"

print "Make API calls"
#ts = TwitterStream(auth=OAuth(access_token, access_secret, api_key, api_secret))
t = Twitter(auth=OAuth(access_token, access_secret, api_key, api_secret))


tweets = []

#check = ts.statuses.filter(track="#ebay")



def TwitterSearch(twitterApi, query, approxCount, **kw):
    searchResults = twitterApi.search.tweets(q= query, count=100, **kw)
    statuses = searchResults['statuses']
    
    tweets = []
    
    while len(tweets) < approxCount:
        for tweet in statuses:
            if len(tweet["entities"]["urls"]) == 0:
                print "============="
                print tweet['text']
                tweet_dict = {'text': tweet['text'],
                              'hashtags': [x['text'] for x in tweet['entities']["hashtags"]],
                              'retweet_count': tweet['retweet_count'],
                              'user': tweet['user']['followers_count']
                             }
                tweets.append(tweet_dict)
        print "Writing " + str(len(tweets)) + " tweets"
        f = open("data/" + query + ".json", "w")
        f.write(json.dumps(tweets, indent=4))
        try:
            nextResults = searchResults['search_metadata']['next_results']
        except KeyError, e:
            break
        kwargs = dict([ kv.split('=') for kv in nextResults[1:].split("&") ])
        nextResults = twitterApi.search.tweets(**kwargs)
        statuses = nextResults['statuses']




#check = t.search.tweets(q="#dell", count=100)


TwitterSearch(t, "#xperia", 20)


'''
for tweet in check['statuses']:
    #for tweet in check:
    if len(tweet["entities"]["urls"]) == 0:
        tweet_dict = {'text': tweet['text'],
                       'hashtags': [x['text'] for x in tweet['entities']["hashtags"]],
                       'retweet_count': tweet['retweet_count'],
                       'user': tweet['user']
                      }
        tweets.append(tweet_dict)
        print json.dumps(tweet_dict, indent=4)
        raw_input()
    else:
        print "DAMAL"'''
