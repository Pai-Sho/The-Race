import twitter
from typing import List, Dict

keys = {'access_token': '1231336266597142528-2N7I91ndaCQ9BCLWeyh6uG7eiKO0zO',
        'access_token_secret': 'DSQ8cLJsnvlX5bH8uJLid9eyISRGCQB7P91QqS1rmWUYU',
        'consumer_api_key': 'FgygPBQmkfJXJY7rzkqixy0yQ',
        'consumer_api_secret': 'CxQnDr7Wdmsogss0KmLqf2c7QVsfRxq7KbqLdttqOwh66StFgo'}

keys2 = {'access_token': '824402227-3BGKXqBbVGdfyieTu1rXUgoHUDYH5dZViMHQl50V',
        'access_token_secret': 'Xv8MrDoZv2nX3R97XBd6d9q83TnSfVBvOEkB9YJyiEy2f',
        'consumer_api_key': 'bsDONudtGds6xnROaR6Ypp4xz',
        'consumer_api_secret': 'oklYvvXehchyiolR0twqkC5ffmj2MaA325Vn5PSydKsE24VeNc'
}

keys3 = {'access_token': '824776302079012864-O86by3AYa0aEPoFPHZIm7lldHJnIeGG',
        'access_token_secret': 'CWTPERGhJMdA9O1qjewq3xtMK5nsOVN52X1xUFBzFT3KK',
        'consumer_api_key': 'BmSrSOqFRJ0jqMy38858doyzi',
        'consumer_api_secret': 'MU20lkffcWbUMV8lj193yvB9NUo28xGiLnI8Vgb38zHBjiYhyd'
}

def get_tweet_embedding(url: str) -> str:
    '''
    Given a url find the dom object associated with it

    Inputs:
        url:    string url directed to tweets
    Outputs:
        string dom object to embed in page
    '''
    api = twitter.Api(consumer_key=keys['consumer_api_key'], consumer_secret=keys['consumer_api_secret'],
                      access_token_key=keys['access_token'], access_token_secret=keys['access_token_secret'])

    return api.GetStatusOembed(url=url, hide_thread=True, hide_media=True)['html']


def get_tweets_by_hashtag(hashtag_str: str, num_tweets: int, result_type: str='recent') -> List[Dict]:
    """
    Get top n tweets by hashtag by querying the twitter API

    Inputs:
        hashtag_str:   hashtag to search by
        num_tweets:    number of tweets containing hashtag to get

    Outputs:
        top_n_tweets:  List of dictionaries containing tweet info - favorite_count, retweet_count, hashtags, and url
    """
    api = twitter.Api(consumer_key=keys['consumer_api_key'], consumer_secret=keys['consumer_api_secret'],
                      access_token_key=keys['access_token'], access_token_secret=keys['access_token_secret'])

    tweets = api.GetSearch(
        raw_query="q=%23{query}&result_type={result_type}&count={count}".format(query=hashtag_str,
                                                                           result_type=result_type,
                                                                           count=num_tweets))

    tweet_attributes = [{'favorite_count': t.favorite_count, 'retweet_count': t.retweet_count,
                         'hashtags': [h.text.lower() for h in t.hashtags], 'lang': t.lang,
                         'url': 'https://twitter.com/{screen_name}/status/{id}'.format(screen_name=t.user.screen_name,
                                                                                       id=t.id_str)}
                        for t in tweets]

    return tweet_attributes


def get_tweets_by_hashtag_pair(hashtag_str1: str, hashtag_str2: str, num_tweets: int, result_type:str='recent') -> List[Dict]:
    """
    Get top n tweets by hashtag by querying the twitter API

    Inputs:
        hashtag_str:   hashtag to search by
        num_tweets:    number of tweets containing hashtag to get

    Outputs:
        top_n_tweets:  List of dictionaries containing tweet info - favorite_count, retweet_count, hashtags, and url
    """
    api = twitter.Api(consumer_key=keys['consumer_api_key'], consumer_secret=keys['consumer_api_secret'],
                      access_token_key=keys['access_token'], access_token_secret=keys['access_token_secret'])

    tweets = api.GetSearch(
        raw_query="q=%23{query1} %23{query2}&result_type={result_type}&count={count}".format(query1=hashtag_str1,
                                                                                             query2=hashtag_str2,
                                                                                             result_type=result_type,
                                                                                             count=num_tweets))

    tweet_attributes = [{'favorite_count': t.favorite_count, 'retweet_count': t.retweet_count,
                         'hashtags': [h.text.lower() for h in t.hashtags], 'lang': t.lang,
                         'url': 'https://twitter.com/{screen_name}/status/{id}'.format(screen_name=t.user.screen_name,
                                                                                       id=t.id_str)}
                        for t in tweets]

    return tweet_attributes


#print(get_tweets_by_hashtag("nike", 20))
# print(get_tweets_by_hashtag_pair("adidas", "nike", 20))
