# -*- coding: utf-8 -*-
# @project：wholee_get_walks
# @author:caojinlei
# @file: run.py
# @time: 2021/05/27
from models.random_walk import *
from models.embedding import Embedding
from utils.classify import NodeClassify, LinkPredict
from sklearn.linear_model import LogisticRegression
from data_load.data_load import *
import pandas as pd
import networkx as nx
import argparse
from utils.utils import *
from utils.preprocess import get_data
from utils.Logginger import init_logger

logger = init_logger("main", logging_path='output/')


def argments():
    """
    外部可配参数
    """
    parser = argparse.ArgumentParser(description='Random walk')
    parser.add_argument('-r', '--random', action='store_false', default=True, help='Whether to use random walk')
    parser.add_argument('-m', '--method', type=str, default='n',
                        help='Classify_method : node classify/link')
    parser.add_argument('-sf', '--sample_frac', type=float, default=0.3, metavar='N',
                        help='Test size')
    parser.add_argument('-wl', '--walk_length', type=int, default=10, metavar='N',
                        help='Generated walk length')
    parser.add_argument('-rp', '--random_processes', type=int, default=3, metavar='N',
                        help='Number of random walk processes')
    parser.add_argument('-ns', '--seq_num', type=int, default=1, metavar='N',
                        help='The sequence number')
    parser.add_argument('-v', '--verbose', type=int, default=1, metavar='N',
                        help='The verbose')
    parser.add_argument('-e', '--to_excel', action='store_true', default=False,
                        help='Whether to excel the result')
    return parser.parse_args()


def cmd_entry(args):
    walk_path = 'input/pid_walks.csv'
    edges_path = 'input/pid_edges.csv'
    nodes_path = 'input/pid_nodes.csv'
    out_path = 'output/results.xlsx'
    random = args.random
    classify_method = args.method
    try:
        G = nx.read_edgelist(edges_path, nodetype=None)
    except Exception as e:
        logger.error(e)
        get_data(walk_path, edges_path, nodes_path)
        G = nx.read_edgelist(edges_path, nodetype=None)
    if classify_method == 'l':
        test_pos_list = edges_sample(G, sample_frac=args.sample_frac)  # 采样正样本
        test_neg_list = get_negative_samples(G, test_pos_list)
        G.remove_edges_from(test_pos_list)
    else:
        X, Y = get_nodes_class(nodes_path)
        G.add_nodes_from(list(set(X) - set(list(G.nodes()))))  # 增加孤立点
    if random:
        random_walk = RandomWalks(G, args.walk_length, args.seq_num, args.random_processes, verbose=args.verbose)
        walks = random_walk.run()
        logger.info('Load random walk date')
    else:
        walks = get_base_seq(walk_path)
        logger.info('Load base date')
    embedding_model = Embedding(G, walks)
    embedding_model.train(workers=5)
    embedding_dict = embedding_model.get_embedding()

    # 结果预测
    if classify_method == 'n':
        base_model = LogisticRegression(solver='sag', n_jobs=3, max_iter=200, verbose=args.verbose)
        node_classify = NodeClassify(X, Y, embedding_dict, base_model)
        node_classify.train()
        score = node_classify.evaluate()

    else:
        link_predict = LinkPredict(test_pos_list, test_neg_list, embedding_dict)
        pos_sim_list, neg_sim_list = link_predict.train()
        pos_sim_list = sorted(pos_sim_list, reverse=True)
        neg_sim_list = sorted(neg_sim_list, reverse=True)
        topk_list = [50, 100, 150, 200, 250]
        score = link_predict.evaluate(pos_sim_list, neg_sim_list, topk_list)
    if args.to_excel:
        df_score = pd.DataFrame(score, index=[0]).T
        print(df_score)
        df_score.to_excel(out_path)
    return score


if __name__ == '__main__':
    args = argments()
    print(args)
    score = cmd_entry(args)
