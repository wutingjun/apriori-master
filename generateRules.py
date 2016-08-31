#coding=utf-8

from apriori import  aprioriGen
def generateRules(L, supportData, minSup=0.7): #L:存储着所有的频繁项集 supportData:所有候选项集的支持度
    bigRuleList = []
    for i in range(1, len(L)): #频繁1-项集没有什么可以挖掘的,挖掘都是从频繁2-项集开始
        for freqSet in L[i]:
            #freqSet是频繁k-项集中的一项,item是freqSet的每一个元素
            H1 = [frozenset([item]) for item in freqSet]
            print L[i]
            print H1
            if (i > 1):
                # 三个及以上元素的集合
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minSup)
            else:
                # 两个元素的集合.这两个元素是相对的,每个元素有可能是一个item集合,不然怎么算(A,B)->C的置信度
                # freqSet:频繁项, H1:频繁项中的每一个元素组成的列表, supportData:所有候选项集的支持度集合, bigRuleList:存储挖掘出来的关联规则,A->B,B->A置信度这些数据, minSup:最小支持度
                calcConf(freqSet, H1, supportData, bigRuleList, minSup)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minSup=0.7):
    ''' 对候选规则集进行评估 '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minSup:
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    ''' 生成候选规则集 '''
    m = len(H[0])
    print m
    if (len(freqSet) > (m + 1)):
        Hmpl = aprioriGen(H, m + 1) #基于H中每一项的构建比自己多一项的频繁项集
        Hmpl = calcConf(freqSet, Hmpl, supportData, brl, minConf) #筛选出满足置信度的频繁项
        #从这里看出,对于频繁多项集的关联规则的生成是基于二项集的基础上完成的
        if (len(Hmpl) > 1):
            rulesFromConseq(freqSet, Hmpl, supportData, brl, minConf)



