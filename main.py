#coding=utf-8
if __name__=="__main__":
    from apriori import apriori
    from generateRules import generateRules
    from kgenerateRules import kgenerateRules
    from loadData import loadSimpleData

    dataSet=loadSimpleData()
    L,suppData = apriori(dataSet)
    #L是所有频繁项集的集合,L1,L2,...,L[0]是频繁1-项集,L[1]是频繁2-项集,...,这么做是为了后面挖掘关键规则方便把.suppData:是所有候选项集的支持度集合
    i = 0
    for one in L:
        print "项数为 %s 的频繁项集：" % (i + 1), one,"\n"
        i +=1
    print suppData

    print "minConf=0.7时："
    # 挖掘整个频繁项集的关联规则
    # rules = generateRules(L,suppData, minConf=0.7)
    # print rules

    # 实际项目中,一般不需要挖掘整个频繁项集的关联规则,但是可能需要挖掘频繁2-项集,3-项集的关联规则
    krules=kgenerateRules(L[2],3,suppData, minConf=0.7)
    print krules
