# -*- coding: utf-8 -*-
# @project：wholee_get_walks
# @author:caojinlei
# @file: utils.py
# @time: 2021/05/28
from utils.Logginger import init_logger
import numpy as np
import networkx as nx
from tqdm import tqdm
import random
from random import sample
logger = init_logger("embedding_merge", logging_path='output/')


def get_negative_samples(G, test_pos_list):
    count = 0
    nodes_list = list(G.nodes())
    random.shuffle(nodes_list)
    break_number = len(test_pos_list)
    test_neg_list = []
    for x in range(100):
        for i in range(len(nodes_list)):
            cur_node = nodes_list[i]
            random_node = random.choice(nodes_list)
            while random_node in list(G.adj[cur_node]):
                logger.info(f'{cur_node}-{random_node} is positive sample')
                random_node = random.choice(nodes_list)
            test_neg_list.append((cur_node,random_node))
            count += 1
            if count % 100000 == 0:
                logger.info(f'negative sample {count}')
            if count >= break_number:
                break
        if count >= break_number:
            break
    return test_neg_list


def embedding_merge(nodes_pre, nodes_lat, nodes_pre_neg, nodes_lat_neg, embedding, num_pairs, mode='reduce'):
    logger.info('Embedding merge ...')
    length = len(nodes_pre)
    if length < num_pairs:
        num = length
    else:
        num = num_pairs
    embedding_merge_dict = {}
    link_list = []
    target_list = []
    for i in tqdm(range(num)):
        emb_pre = embedding[nodes_pre[i]]
        emb_lat = embedding[nodes_lat[i]]
        if mode == 'reduce':
            emb_merge = emb_lat - emb_pre
        elif mode == 'concat':
            emb_merge = np.r_[emb_lat, emb_pre]
        else:
            emb_merge = emb_lat + emb_pre
        link = nodes_pre[i] + '-' + nodes_lat[i]
        embedding_merge_dict[link] = emb_merge
        link_list.append(link)
        target_list.append(1)

        neg_emb_pre = embedding[nodes_pre_neg[i]]
        neg_emb_lat = embedding[nodes_lat_neg[i]]
        if mode == 'reduce':
            neg_emb_merge = neg_emb_pre - neg_emb_lat
        elif mode == 'concat':
            neg_emb_merge = np.r_[neg_emb_pre, neg_emb_lat]
        else:
            neg_emb_merge = neg_emb_pre + neg_emb_lat
        neg_link = nodes_pre_neg[i] + '-' + nodes_lat_neg[i]
        embedding_merge_dict[neg_link] = neg_emb_merge
        link_list.append(neg_link)
        target_list.append(0)
    logger.info('Embedding merge done!')
    return link_list, target_list, embedding_merge_dict


def edges_sample(G,sample_frac):
    edges_list = list(G.edges())
    pop = int(len(edges_list)*sample_frac)
    test_pos_edges = random.sample(edges_list,pop)
    return test_pos_edges
