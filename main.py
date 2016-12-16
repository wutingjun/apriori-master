#coding=utf-8
if __name__=="__main__":
    from apriori import apriori
    from generateRules import generateRules
    from kgenerateRules import kgenerateRules
    from loadData import loadSimpleData

    dataSet=loadSimpleData('itemsSet.txt')
    # apriori的输入是一个列表,列表的每个元素是项的集合
    L,suppData = apriori(dataSet)
    #L是所有频繁项集的集合,L[0]=L1是频繁1-项集,L[1]=L2是频繁2-项集,...,这么做是为了取数方便,生成Li需要先生成Li-1,这需要把这些数据存在L中方便取
    # suppData:频繁项集支持度集合
    i = 0
    for one in L:
        print "项数为 %s 的频繁项集：" % (i + 1), one,"\n"
        i +=1
    print suppData

    print '-----------------------------------------------------------------'
    print "minConf=0.7时,挖掘出来的关联规则如下："
    # 根据频繁项集的挖掘关联规则
    rules = generateRules(L,suppData, minConf=0.7)
    print rules

    # 实际项目中,一般不需要挖掘整个频繁项集的关联规则,但是可能需要挖掘频繁2-项集,3-项集的关联规则
    print '-----------------------------------------------------------------------------'
    krules=kgenerateRules(L[2],3,suppData, minConf=0.7)
    print krules
