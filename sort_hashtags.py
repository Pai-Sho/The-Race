import collections


def get_top_linked_hashtags(tweets, num_hashtags):
        """
        Get most frequent distinct hashtags from json tweet list

        Inputs:
            tweets:         List of dictionaries containing tweet information
            num_hashtags:   Number of top hashtags to save

        Outputs:
            top_n_hashtages:  List of top 'num_hashtags' hashtags from input tweets
        """

        english_tweets = [tweet for tweet in tweets if tweet['lang'] == 'en']

        all_hashtags = [t for tweet in english_tweets for t in tweet['hashtags']]

        distinct_hashtags = collections.Counter(all_hashtags)

        top_n_hashtags = distinct_hashtags.most_common(num_hashtags)

        return top_n_hashtags
