from typing import List, Dict, Optional

from get_tweets import get_tweets_by_hashtag, get_tweets_by_hashtag_pair


##############################################################
#                   Private Functions
##############################################################
def __get_related_tweet(hashtag1: str, hashtag2: str, num_tweets: int) -> Optional[Dict]:
    '''
    Get a list of tweets that contains both hashtags

    Inputs:
        hashtag1: string hashtag to look for
        hashtag2: string hashtag to filter by
    Returns:
        list of strings of urls that relate the two hashtags
    '''
    contains_both = []

    tweets = get_tweets_by_hashtag_pair(hashtag1, hashtag2, num_tweets)
    print(hashtag1, hashtag2)
    print([t['hashtags'] for t in tweets])
    for twt in tweets:
        if hashtag2 in twt['hashtags']:
            return twt['url']

    raise Exception("No related tweet")

##############################################################
#                   Public Functions
##############################################################
def find_path(path, num_tweets=100):
    '''
    find a path of tweets (URLs) from a path of hashtags

    Inputs:
        path:   list of strings of hashtags used
    Outputs:
        list of strings of URLs to tweets that made the path
    '''
    tweet_path = []
    for i in range(len(path) - 1):
        hashtag1 = path[i]
        hashtag2 = path[i+1]
        related_tweet = __get_related_tweet(hashtag1, hashtag2, num_tweets)
        print("\n\nrelated:", related_tweet)
        tweet_path.append(related_tweet)

    return tweet_path


#print(find_path(["trump", "Bernie", "socialist"]))