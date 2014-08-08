import itertools
from collections import defaultdict
import networkx as nx
import numpy as np

def validModels(world):
    return {"validworlds":1}

def featureConsistentTemplates(world):
    features = dict()
    consistDict = dict()
    for a,feat in world:
        words = ','.join([f.word for f in feat])
        temp = feat[0].templateNumber
        if words in consistDict and consistDict[words] != temp:
            features[words] = -1
        else:
            consistDict[words] = temp
            features[words] = temp
    out = {}

    for (wordPair1, wordPair2) in itertools.product(features.keys(),features.keys()):
        if wordPair1 != wordPair2 and features[wordPair1] >= 0 and features[wordPair2] >= 0:
          out["%s,%d,%s,%d" % (wordPair1,features[wordPair1],wordPair2,features[wordPair2])] = 1


    for key, val in features.iteritems():
      if val >= 0:
        out["%s,%d" %(key,val)] = 1
    return out

# (a,b,c) -> (a:{{b,c}}), (b:{{a,c}}), (c:{{a,b}})
# (b,c,d) -> (b:{{c,d}}), (c:{{b,d}}), (d:{{b,c}})
def solver(sent_tuples, featureset):
    stats = {}
    globalStats = {}
    #outs = [enum(x) for x in sent_tuples]
    count = 1
    for combination in itertools.product(*sent_tuples):
        # print combination
        # if count % 1000 == 0:
        #     print count
        # count = count+1
        G = nx.DiGraph()
        for c in combination:
            key = c[0][0]
            val = c[0][1]
            for v in val:
                G.add_edge(key,v)
            if c not in stats:
                stats[c] = 0
        try:
            k = nx.simple_cycles(G).next()
        except StopIteration:
            for f in featureset:
                feature = f(combination)
                for k in feature:
                    if k in globalStats:
                        globalStats[k] += feature[k]
                    else:
                        globalStats[k] = feature[k]
            for c in combination:
                stats[c] = stats[c] + 1

    return (stats, globalStats)

def enum(sent_tuple):
    out = []
    for i in range(len(sent_tuple)):
        out.append((sent_tuple[i], set(sent_tuple[0:i]).union(set(sent_tuple[i+1:]))))
    return out

# print solver([[("a",frozenset({"b","c"})),("c",frozenset({"b","a"}))],[("c",frozenset({"d","a"}))]])


