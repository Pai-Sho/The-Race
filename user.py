from treelib import Node, Tree
from sort_hashtags import get_top_linked_hashtags
from get_tweets import get_tweets_by_hashtag
from utils import *
from Agent import *

class User(Agent):

    def __init__(self, max_depth, num_children, start_hashtag, end_hashtag, num_tweets=100, DEBUG=False):
        return super().__init__(max_depth, num_children, num_tweets, DEBUG)
        self.n_show = 5
        self.current_side = 0
        self.init_search(start_hashtag, end_hashtag)

    def get_leaves(self, start=True):
        return super().get_leaves(start)

    def get_hashtags(self, hashtag, tree='s'):
        return super().get_hashtags(hashtag, tree)

    def get_parents(self, tag, start=True):
        return super().get_parents(tag, start)

    def find_path(self):
        return super().find_path()

    def run_round(self, first=False):
        '''
        Run a round of the search algorithm

        Inputs:
            None
        Outputs:
            list. List of strings of hashtags of path from start to end if found otherwise an empty list
        '''
        s_leaves = self.get_leaves()
        e_leaves = self.get_leaves(start=False)

        # add leaves to start_tree
        for s_leaf in s_leaves:
            related_tags = self.get_hashtags(s_leaf.identifier)
            #if first and len(related_tags) == 0:
            #    raise Exception('#{} has no recent related hashtags'.format(s_leaf.identifier))
            for rt in related_tags:
                tag = rt[0]
                c = rt[1]
                self.start_tree.create_node(tag, tag, parent=s_leaf.identifier, data=c)

        # add leaves to end_tree
        for e_leaf in e_leaves:
            related_tags = self.get_hashtags(e_leaf.identifier, tree='e')
            #if first and len(related_tags) == 0:
            #    raise Exception('#{} has no recent related hashtags'.format(e_leaf.identifier))
            for rt in related_tags:
                tag = rt[0]
                c = rt[1]
                self.end_tree.create_node(tag, tag, parent=e_leaf.identifier, data=c)

        path = self.find_path()

        # find a path
        return path

    def print_round_info(self, round):
        '''
        print round information

        Inputs:
            round:  round number just completed
        Outputs:
            None
        '''
        print('=============================')
        print('end of round {}\n'.format(round))
        print('starting tree:')
        self.start_tree.show()
        print('\nending tree:')
        self.end_tree.show()

    def init_search(self, start_hashtag, end_hashtag):
        """
        Perform graph search from start hashtag to end hashtag

        Inputs:
            start_hashtag:  string hashtag to start at
            end_hashtag:    string hashtag to end at

        Outputs:
            List of hashtag strings from start to finish. If no path found return []
        """
        # init tree and start and end hashtags
        self.start_hashtag = start_hashtag.lower()
        self.end_hashtag = end_hashtag.lower()
        self.start_tree.create_node(start_hashtag, start_hashtag)
        self.end_tree.create_node(end_hashtag, end_hashtag)

        return

    def append_search(self, clicked_hashtag, side):

        if side == 0:
            parent = self.start_tree.get_node(clicked_hashtag)
            tweets = get_tweets_by_hashtag(clicked_hashtag, self.num_tweets)
            related_hashtags = get_top_linked_hashtags(tweets, self.n_show)
            for hashtag in related_hashtags:
                tag = hashtag[0]
                c = hashtag[1]
                self.start_tree.create_node(tag, tag, parent=parent.identifier, data=c)
            self.current_side = 1
            return

        else:
            parent = self.start_tree.get_node(clicked_hashtag)
            tweets = get_tweets_by_hashtag(clicked_hashtag, self.num_tweets)
            hashtags = get_top_linked_hashtags(tweets, self.n_show)
            for rt in related_tags:
                tag = rt[0]
                c = rt[1]
                self.end_tree.create_node(tag, tag, parent=parent.identifier, data=c)
            self.current_side = 0
            return
