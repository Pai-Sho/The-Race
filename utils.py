from get_tweets import get_tweets_by_hashtag

def has_n_tweets(hashtag, n=100):
    '''
    Determines if a hashtag has set number of tweets about it

    Inputs:
        hashtag:    string the hashtag in quesiton
        n:          int number of tweets this hashtag should have. Default=100
    Outputs:
        True if the hashtag has at least n tweets in it False otherwise
    '''
    return True if len(get_tweets_by_hashtag(hashtag, n)) >= n else False
