# -*- coding: utf-8 -*-
# @project：wholee_get_walks
# @author:caojinlei
# @file: preprocess.py
# @time: 2021/05/27

from utils.Logginger import init_logger

logger = init_logger("get edges and nodes", logging_path='output/')


def get_data(path, edges_path, nodes_path):
    with open(path, 'r') as f:
        edges_list = []
        nodes_list = []
        for line in f.readlines():
            length = int(line.split(';')[0])
            pid_walks_list = line.strip().split(';')[1].split(',')
            nodes_class_list = eval(line.strip().split(';')[2])
            nodes_list.append(pid_walks_list[length - 1] + ' ' + nodes_class_list[length - 1])
            for i in range(length - 1):
                nodes_class = pid_walks_list[i] + ' ' + nodes_class_list[i]
                nodes_list.append(nodes_class)
                if pid_walks_list[i] == pid_walks_list[i + 1]:
                    continue
                else:
                    edge = pid_walks_list[i] + ' ' + pid_walks_list[i + 1]
                    edges_list.append(edge)
        edges_set = set(edges_list)
        nodes_set = set(nodes_list)
    logger.info(f'The process completes and fetch nodes :{len(nodes_set)}/ edges:{len(edges_set)}')
    with open(edges_path, 'w') as f:
        for edge in edges_set:
            f.write(edge)
            f.write('\n')
    logger.info('write edges_set')
    with open(nodes_path, 'w') as f:
        for node in nodes_set:
            f.write(node)
            f.write('\n')
    logger.info('write nodes_set')


if __name__ == '__main__':
    path = '../input/pid_walks.csv'
    edges_path = '../input/pid_edges.csv'
    nodes_path = '../input/pid_nodes.csv'
    get_data(path, edges_path, nodes_path)
