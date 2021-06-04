# -*- coding: utf-8 -*-
# @project：wholee_get_walks
# @author:caojinlei
# @file: deepwalk.py
# @time: 2021/05/27
import random
import networkx as nx
import itertools
from joblib import Parallel, delayed


class RandomWalks:
    def __init__(self, G, walk_length, num_works, num_jobs, verbose=0):
        self.G = G
        self.nodes = list(G.nodes())
        self.walk_length = walk_length
        self.num_works = num_works
        self.num_jobs = num_jobs
        self.verbose = verbose

    def partition_num(self):
        n_works = self.num_works
        n_jobs = self.num_jobs
        if n_works % n_jobs == 0:
            return [n_works // n_jobs] * n_works
        else:
            return [n_works // n_jobs] * n_works + [n_works % n_jobs]

    def single_walks(self, start_node):
        walk = [start_node]
        while len(walk) < self.walk_length:
            cur = walk[-1]
            cur_nei = list(self.G.neighbors(cur))
            if len(cur_nei) > 0:
                walk.append(random.choice(cur_nei))
            else:
                break
        return walk

    def parallel_walks(self, num):
        walks = []
        for _ in range(num):
            random.shuffle(self.nodes)
            for node in self.nodes:
                walks.append(self.single_walks(node))
        return walks

    def run(self):
        results = Parallel(n_jobs=self.num_jobs, verbose=self.verbose)(
            delayed(self.parallel_walks)(num) for num in self.partition_num()
        )
        walks = list(itertools.chain(*results))
        return walks


if __name__ == '__main__':
    G = nx.read_edgelist('../input/pid_edges.csv', nodetype=None)
    random_walk = RandomWalks(G, 10, 1, 2, verbose=1)
    walks = random_walk.run()
