from treelib import Node, Tree
from sort_hashtags import get_top_linked_hashtags
from get_tweets import get_tweets_by_hashtag
from utils import *

class Agent(object):

    def __init__(self, max_depth, num_children, num_tweets=100, DEBUG=False):
        self.start_tree = Tree()
        self.end_tree = Tree()
        self.max_depth = max_depth
        self.num_children = num_children
        self.start_hashtag = ''
        self.end_hashtag = ''
        self.num_tweets = num_tweets
        self.DEBUG = DEBUG
        return

    ###############################################################################
    #                   PRIVATE FUNCTIONS
    ###############################################################################

    def get_leaves(self, start=True):
        '''
        Get the leaves of a tree

        Inputs:
            start: boolean set to true if getting start tree leaves, false if end tree leaves
        Outputs:
            list of leaves (in the form of treelib Nodes)
        '''
        return self.start_tree.leaves(self.start_hashtag) if start else self.end_tree.leaves(self.end_hashtag)

    def get_hashtags(self, hashtag, tree='s'):
        '''
        Get the related hashtags (no repeats) of a hashtag

        Inputs:
            hashtag:    string hashtag to find related hashtags
            tree:       string tree to check for repeats in. 's' or 'e'. Default='s'
        Outputs:
            list of tuples of the form (hashtag, number)
        '''
        tweets = get_tweets_by_hashtag(hashtag, self.num_tweets)
        hashtags = get_top_linked_hashtags(tweets, self.num_children * 2)

        t = self.start_tree if tree == 's' else self.end_tree
        good_tags = [x for x in hashtags if not t.contains(x[0])]

        #good_tags.sort(key=lambda x: x[1])
        return good_tags[:self.num_children]

    def get_parents(self, tag, start=True):
        t = self.start_tree if start else self.end_tree
        r_tag = self.start_hashtag if start else self.end_hashtag
        # Edge case when things are too close
        if r_tag == tag:
            return [tag] if start else ['', tag]
        path = [tag]
        parent = t.parent(tag)
        while parent.identifier != r_tag:
            path.insert(0, parent.identifier) if start else path.append(parent.identifier)
            parent = t.parent(parent.identifier)

        path.insert(0, r_tag) if start else path.append(r_tag)
        return path

    def find_path(self):
        '''
        see if a path exists between the two trees

        Inputs:
            none
        Outputs:
            list. List has a path of hashtags if path found otherwise empty list
        '''
        path = []

        # search through all start tree leaves
        s_leaves = self.start_tree.all_nodes()
        #s_leaves = self.__get_leaves()
        for s_leaf in s_leaves:
            if self.end_tree.contains(s_leaf.identifier):
                path = self.get_parents(s_leaf.identifier) + self.get_parents(s_leaf.identifier, start=False)[1:]

        if len(path) > 0:
            return path

        # search through all start tree leaves
        e_leaves = self.get_leaves(start=False)
        for e_leaf in e_leaves:
            if self.start_tree.contains(e_leaf.identifier):
                path = self.get_parents(e_leaf.identifier) + self.get_parents(e_leaf.identifier, start=False)[1:]

        return path
