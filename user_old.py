from typing import List
from get_tweets import get_tweets_by_hashtag
from sort_hashtags import get_top_linked_hashtags

def user_round(input_hashtag, n_show=10, num_tweets=100) -> List[str]:
    '''
    gets hashtags associated with the input hashtag

    Inputs:
        input_hashtag:  string hashtag from last round
        n_show:         int number of related hashtags to return
        num_tweets:     int number of tweets to request
    Outputs:
        list of strings of related hashtags
    '''
    tweets = get_tweets_by_hashtag(input_hashtag, num_tweets)
    hashtags = get_top_linked_hashtags(tweets, n_show)
    return [x[0] for x in hashtags]