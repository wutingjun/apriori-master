#coding=utf-8

import loadData
#D表示原数据集，Ck表示候选集合的列表，minSupport表示最小支持度
#该函数通过扫描一遍原数据集D,求出CK每一项出现的次数,用于从Ck生成Lk，Lk表示满足最低支持度的元素集合,即频繁项集
def scanD(D,Ck,minSupport):
    ssCnt = {}#存储Ck每一个项在D中出现的次数
    for tid in D:
        for can in Ck:
            #issubset：表示如果集合can中的每一元素都在tid中则返回true
            if can.issubset(tid):
                #统计各个集合can出现的次数，存入ssCnt字典中，字典的key是集合，value是统计出现的次数
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    freqList = []
    supportData = {}
    for key in ssCnt:
        #计算每个项集的支持度，如果满足条件则把该项集加入到freqList列表中
        support = ssCnt[key]/numItems
        if support >= minSupport:
            freqList.insert(0, key)
            #构建支持的项集的字典,之前是记录下所有项的支持度计算,感觉没有必要.挖掘频繁项集也是在频繁项集的基础上完成的
            supportData[key] = support
    return freqList,supportData

#Create Ck,CaprioriGen()的输人参数为频繁项集列表Lk-1与候选项集元素个数k，输出为Ck
#之前一直在考虑对LK[i],Lk[j]取前k-1项排序后比较是否合理.[A,C,B],[A,B,D]不会连接的,是否会漏掉[A,B,C,D]这个频繁项([A,B,C],[A,B,D]连接形成的)?
#不会的.因为[A,B,C,D]是频繁项集,一定会出现[A,C,D]是频繁项集,所以后面还是会有[A,C,D]的,不用担心顺序影响到频繁项集的生成.只要排序遵循的是一个规则就没有问题.
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #前k-2项相同时合并两个集合
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])

    return retList

def apriori(dataSet, minSupport=0.5):
    C1 = loadData.createC1(dataSet)  #创建C1
    D = map(set,dataSet) #将整个数据集,转换成一个集合列表,这样做是为了方便判断一个集合是否是另一个集合的子集(在判断是否是频繁项集的时候会用到)

    L1,supportData = scanD(D, C1, minSupport)
    L = [L1]
    #若两个项集的长度为k - 1,则必须前k-2项相同才可连接，即求并集，所以[:k-2]的实际作用为取列表的前k-1个元素
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk,supK = scanD(D,Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k +=1
    return L,supportData #L:所有的频繁项集 supportData:所有候选项集的支持度

