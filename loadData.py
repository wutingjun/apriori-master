#coding=utf-8

def loadSimpleData():
    simpDat=[]
    fileIn=open('itemsSet.txt')
    for line in fileIn.readlines():
        lineArr=line.strip().split(',')
        simpDat.append(lineArr)
    fileIn.close()

    return simpDat


def createC1(dataSet):
    C1=[] #C1为大小为1的项的集合
    for tid in dataSet:
        for item in tid:
            if not [item] in C1: #遍历数据集中的每一条交易
                C1.append([item]) #遍历每一条交易中的每个商品
    C1.sort()
    #map函数表示遍历C1中的每一个元素执行forzenset，frozenset表示“冰冻”的集合，即不可改变
    return map(frozenset,C1)
