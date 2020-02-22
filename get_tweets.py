import twitter
from typing import List, Dict

keys = {'access_token': '1231336266597142528-2N7I91ndaCQ9BCLWeyh6uG7eiKO0zO',
        'access_token_secret': 'DSQ8cLJsnvlX5bH8uJLid9eyISRGCQB7P91QqS1rmWUYU',
        'consumer_api_key': 'FgygPBQmkfJXJY7rzkqixy0yQ',
        'consumer_api_secret': 'CxQnDr7Wdmsogss0KmLqf2c7QVsfRxq7KbqLdttqOwh66StFgo'}


def get_tweets_by_hashtag(hashtag_str: str, num_tweets: int) -> List[Dict]:
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
                                                                           result_type='recent',
                                                                           count=num_tweets))

    tweet_attributes = [{'favorite_count': t.favorite_count, 'retweet_count': t.retweet_count,
                         'hashtags': [h.text for h in t.hashtags],
                         'url': 'https://twitter.com/{screen_name}/status/{id}'.format(screen_name=t.user.screen_name,
                                                                                       id=t.id_str)}
                        for t in tweets]

    return tweet_attributes

#  print(get_tweets_by_hashtag("trump", 20))
