# -*- coding: utf-8 -*-
# @project：wholee_get_walks
# @author:caojinlei
# @file: word2vec_model.py
# @time: 2021/05/28
from gensim.models import Word2Vec
from utils.Logginger import init_logger
import logging

logger = init_logger("get embedding", logging_path='output/')


class Embedding:
    def __init__(self, G, sentences):
        self.sentences = sentences
        self.G = G
        self.nodes = list(G.nodes())

    def train(self, vector_size=128, window_size=5, epochs=5, **kwargs):
        kwargs["sentences"] = self.sentences
        kwargs["vector_size"] = vector_size
        kwargs["window"] = window_size
        kwargs["epochs"] = epochs
        kwargs["sg"] = 1  # skip gram
        kwargs["hs"] = 0  # negative
        kwargs['compute_loss'] = True
        kwargs["workers"] = kwargs.get("workers", 3)
        kwargs["min_count"] = kwargs.get("min_count", 0)

        logger.info("Learning embedding vectors...")
        model = Word2Vec(**kwargs)
        logger.info("Learning embedding vectors done!")
        self.model =model
        return model

    def get_embedding(self):
        embedding_dict = {}
        for node in self.nodes:
            embedding_dict[node] = self.model.wv[node]
        return embedding_dict
