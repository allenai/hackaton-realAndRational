import itertools
from collections import defaultdict
import networkx as nx
import numpy as np

# (a,b,c) -> (a:{{b,c}}), (b:{{a,c}}), (c:{{a,b}})
# (b,c,d) -> (b:{{c,d}}), (c:{{b,d}}), (d:{{b,c}})
def solver(sent_tuples):
    stats = {}
    #outs = [enum(x) for x in sent_tuples]
    count = 1
    for combination in itertools.product(*sent_tuples):
        print combination
        if count % 1000 == 0:
            print count
        count = count+1
        G = nx.DiGraph()
        for key,val in combination:
            for v in val:
                G.add_edge(key,v)
        try:
            k = nx.simple_cycles(G).next()
        except StopIteration:
            for c in combination:
                if c in stats:
                    stats[c] = stats[c] + 1
                else:
                    stats[c] = 1
    return stats

def enum(sent_tuple):
    out = []
    for i in range(len(sent_tuple)):
        out.append((sent_tuple[i], set(sent_tuple[0:i]).union(set(sent_tuple[i+1:]))))
    return out

print solver([[("a",frozenset({"b","c"})),("c",frozenset({"b","a"}))],[("c",frozenset({"d","a"}))]])


