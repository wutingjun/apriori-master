#coding=utf-8

from apriori import  aprioriGen
def generateRules(L, supportData, minConf=0.7): #L:存储着所有的频繁项集 supportData:所有候选项集的支持度
    relationRuleList = []    #用来存储产生的关联规则
    for i in range(1, len(L)): #频繁1-项集没有什么可以挖掘的,挖掘都是从频繁2-项集开始
        for freqSet in L[i]:
            # freqSet是频繁k-项集中的一项,item是freqSet的每一个元素
            # 思路:对每一个频繁K(K>2)-项集中的每一项freqSet逐个挖掘满足支持度和置信度的关联规则.具体过程见50～54行
            H1 = [frozenset([item]) for item in freqSet]
            # print L[i]
            print H1
            # 这个if-else语句可以合并,但是不合并更好理解,还是不合并吧
            if (i > 1):
                # 三个及以上元素的集合
                rulesFromConseq(freqSet, H1, supportData, relationRuleList, minConf)
            else:
                # 两个元素的集合.
                # 这两个元素是相对的,每个元素有可能是一个item集合,不然怎么算(A,B)->C的置信度
                # freqSet:频繁项, H1:freqSet的频繁子项组成的频繁项集, supportData:所有候选项集的支持度集合, bigRuleList:存储挖掘出来的关联规则,A->B,B->A置信度这些数据, minConf:最小置信度
                # 这个函数有两个目的,1是求(freqSet-H1[i])->H1[i]置信度,2是剪枝,返回满足置信度的H[i]，剪什么见34～35行解释
                calcConf(freqSet, H1, supportData, relationRuleList, minConf)
    return relationRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    ''' 计算H[i]->freqSet-H[i]的置信度,并返回满足置信度的H[i] '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    # 其实这也相当于一个剪枝过程,例如:ABC->D不满足minConf要求，即ABCD/ABC<minConf,这样AB->CD,AC->BD,BC->AD也不会满足minConf要求,因为ABCD/(AB,AC,BC)<ABCD/ABC<minConf
    # 若ABCD/ABC>minConf,这三个有可能满足minConf要求，所以需要加入prunedH，然后生成*D,再判断。这才是为什么要prunedH.append(conseq)这一句正确的解释，之前的理解不对
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    # freqSet:频繁项, H:freqSet的子项组成的频繁项集, supportData:所有候选项集的支持度集合, brl:存储挖掘出来的关联规则,A->B,B->A置信度这些数据, minConf:最小置信度
    m = len(H[0])
    while (len(freqSet) > m):   #只有len(freqSet)>m时,在calcConf计算置信度时freqSet - conseq才不会为空,说明此时可以做子项之间的置信度
        H= calcConf(freqSet, H, supportData, brl, minConf) #计算(freqSet-H[i])->H[i]的置信度,并返回满足置信度的H[i]
        #如果H为空,这表明不存在比H[i]中更高的项满足(freqSet-H[i])->H[i]的minConf
        if (len(H)>1):
            H=aprioriGen(H, m + 1) #基于H中每一项(长度为m)的构建频繁m+1项集
            m+=1
        else:
            break

        #对于频繁5-项集来说,先计算所有计算所有频繁4-项->频繁1-项的置信度(如:(A,B,C,D)->(E),(A,B,C,E)->(D),...),并剪枝掉不满足minConf的conseq(1项)，原理见34～35行解释,
        #以频繁1项生成频繁2项集,计算频繁3项->频繁2项的置信度(如:(A,B,C)->(D,E),(A,B,D)->(C,E),...),并剪枝掉不满足minConf的conseq(2项)，原理见34～35行解释,
        #以频繁2项生成频繁3项集,计算所有频繁2项->频繁3项的置信度(如:(A,B)->(C,D,E),(A,C)->(B,D,E),...),并剪枝掉不满足minConf的conseq(3项)，原理见34～35行解释,
        #以频繁3项生成频繁4项集,计算所有频繁1项->频繁4项的置信度(如:(A)->(B,C,D,E),(B)->(A,C,D,E),...),并剪枝掉不满足minConf的conseq(4项)，原理见34～35行解释,
        #以频繁4项生成频繁5项集,到5项集了,停止循环;同时,如果中间筛选出的H为空,这表明不存在比H[i]中更高的项满足(freqSet-H[i])->H[i]的minConf



