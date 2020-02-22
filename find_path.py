from get_tweets import get_tweets_by_hashtag
##############################################################
#                   Private Functions
##############################################################
def __get_related_tweets(hashtag1, hashtag2, num_tweets):
    '''
    Get a list of tweets that contains both hashtags

    Inputs:
        hashtag1: string hashtag to look for
        hashtag2: string hashtag to filter by
    Returns:
        list of strings of urls that relate the two hashtags
    '''
    tweets = get_tweets_by_hashtag(hashtag1, num_tweets)
    for twt in tweets:
        

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
    for i in range(len(tweet_path) -1):
        hashtag1 = path[i]
        hashtag2 = path[i+1] 

    return tweet_path