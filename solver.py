import itertools
from collections import defaultdict
import networkx as nx
import numpy as np

# (a,b,c) -> (a:{{b,c}}), (b:{{a,c}}), (c:{{a,b}})
# (b,c,d) -> (b:{{c,d}}), (c:{{b,d}}), (d:{{b,c}})
def solver(sent_tuples):
    stats = []
    outs = [enum(x) for x in sent_tuples]
    count = 1
    for combination in itertools.product(*outs):
        if count % 1000 == 0:
            print count
        count = count+1
        d = {}
        G = nx.DiGraph()
        for key,val in combination:
            for v in val:
                G.add_edge(key,v)

        try:
            k = nx.simple_cycles(G).next()
            #print combination
        except StopIteration:
            stats.append(combination)
    return stats

def enum(sent_tuple):
    out = []
    for i in range(len(sent_tuple)):
        out.append((sent_tuple[i], set(sent_tuple[0:i]).union(set(sent_tuple[i+1:]))))
    return out

vars = 'abcde'
k = [x for x in itertools.permutations(vars,3)]

np.random.shuffle(k)
print k[:11]
print len(solver(k[:11]))

