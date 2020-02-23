from treelib import Node, Tree
from sort_hashtags import get_top_linked_hashtags
from get_tweets import get_tweets_by_hashtag
from utils import *

class Bot:

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

    def __get_leaves(self, start=True):
        '''
        Get the leaves of a tree

        Inputs:
            start: boolean set to true if getting start tree leaves, false if end tree leaves
        Outputs:
            list of leaves (in the form of treelib Nodes)
        '''
        return self.start_tree.leaves(self.start_hashtag) if start else self.end_tree.leaves(self.end_hashtag)

    def __get_hashtags(self, hashtag, tree='s'):
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

    def __get_parents(self, tag, start=True):
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

    def __find_path(self):
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
                path = self.__get_parents(s_leaf.identifier)[:-1] + self.__get_parents(s_leaf.identifier, start=False)[1:]

        if len(path) > 0:
            return path

        # search through all start tree leaves
        e_leaves = self.__get_leaves(start=False)
        for e_leaf in e_leaves:
            if self.start_tree.contains(e_leaf.identifier):
                path = self.__get_parents(e_leaf.identifier) + self.__get_parents(e_leaf.identifier, start=False)[1:]

        return path

    def __run_round(self, first=False):
        '''
        Run a round of the search algorithm

        Inputs:
            None
        Outputs:
            list. List of strings of hashtags of path from start to end if found otherwise an empty list
        '''
        s_leaves = self.__get_leaves()
        e_leaves = self.__get_leaves(start=False)

        # add leaves to start_tree
        for s_leaf in s_leaves:
            related_tags = self.__get_hashtags(s_leaf.identifier)
            if first and len(related_tags) == 0:
                raise Exception("nope")
            for rt in related_tags:
                tag = rt[0]
                c = rt[1]
                self.start_tree.create_node(tag, tag, parent=s_leaf.identifier, data=c)

        # add leaves to end_tree
        for e_leaf in e_leaves:
            related_tags = self.__get_hashtags(e_leaf.identifier, tree='e')
            if first and len(related_tags) == 0:
                raise Exception("nope")
            for rt in related_tags:
                tag = rt[0]
                c = rt[1]
                self.end_tree.create_node(tag, tag, parent=e_leaf.identifier, data=c)

        path = self.__find_path()

        # find a path
        return path

    def __print_round_info(self, round):
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

    #######################################################################
    #               Public Functions
    #######################################################################

    def search(self, start_hashtag, end_hashtag):
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

        path = []
        for i in range(self.max_depth):
            '''
            get_tweets_by_hashtag(hashtag_str, num_tweets)
            get_top_linked_hashtags(tweets, num_hashtags)
            '''
            first = True if i==0 else False
            path = self.__run_round(first=first)
            self.DEBUG and self.__print_round_info(i)

            if len(path) > 0:
                return path

        return path
