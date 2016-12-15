#coding=utf-8

import pandas as pd

def loadSimpleData(filename):
    simpDat=[]

    df=pd.read_csv(filename,sep='\t')
    for index,row in df.iterrows():
        itemsList=row['items'].strip().split(',')
        simpDat.append(itemsList)

    return simpDat


def createC1(dataSet):
    C1=[] #C1为1项的集合
    for ele in dataSet:
        for item in ele:
            if not [item] in C1: #遍历数据集中的每一条交易
                C1.append([item]) #遍历每一条交易中的每个商品
    C1.sort()
    #map函数表示遍历C1中的每一个元素执行forzenset，frozenset表示“冰冻”的集合，即不可改变
    return map(frozenset,C1)
