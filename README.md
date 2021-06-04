# README

## 原论文

参考《DeepWalk: Online Learning of Social Representations》

## 代码结构

```
├── data_load
│   ├── __pycache__
│   └── data_load.py
├── input
│   ├── pid_edges.csv
│   ├── pid_nodes.csv
│   ├── pid_walks.csv
├── models
│   ├── __init__.py
│   ├── __pycache__
│   ├── embedding.py
│   └── random_walk.py
├── output
│   ├── all.log
│   ├── all.log.2021-05-28
│   └── error.log
├── run.py
├── utils
│   ├── Logginger.py
│   ├── __pycache__
│   ├── classify.py
│   ├── download_pidwalk.py
│   ├── preprocess.py
│   └── utils.py
```

## 原始数据格式

```
7;a,b,c,d,e,f,b;['627', '0', '601', '601', '607', '607', '0']
```

length；点击序列；类目

## 主程序

```
python run.py -r 
```

## 参数说明

- random：是否使用随机游走，默认使用
- method：用node classify 还是link predict做预测
- sample_frac：测试样本采集比例
- walk_length：随机游走长度
- seq_num：序列总构造倍数，按节点为基数，如果是3，seq就是基数的3倍
- random_processes：随机游走并行的个数
- verbose：是否打开日志
- to_excel：预测是结果是否要输出