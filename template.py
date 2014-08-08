import string
import sys
import solver
import pprint

CONCEPTS = {'distance': 'd', 'speed': 's', 'time': 't',
            'power': 'p', 'energy': 'e', 'force': 'f',
            'acceleration': 'a', 'mass': 'm'}

RELATIONS = ['is', 'times', 'divided']

def extractConcepts(sentence):
  words = string.split(sentence)
  concepts = []
  for word in words:
    if word.lower() in CONCEPTS:
      concepts.append(CONCEPTS[word.lower()])
  return tuple(concepts)

def extractFeatures(sentence, template):
  words = string.split(sentence)
  relations = []
  for word in words:
    if word.lower() in RELATIONS:
      relations.append(word.lower())
  features = []
  for i, relation in enumerate(relations):
    features.append(Feature(relation, i, template.number))
  return tuple(features)

class Feature:
  def __init__(self, word, slot, templateNumber):
    self.word = word
    self.slot = slot
    self.templateNumber = templateNumber

  def __repr__(self):
    return '"{}" in operator slot {} for template {}'.format(self.word,
                                                             self.slot,
                                                             self.templateNumber)

class Template:
  def __init__(self, concepts):
    self.concepts = concepts

class Template0(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.head = self.concepts[0]
    self.body = frozenset(self.concepts[1:3])
    self.number = 0

  def toTuple(self):
    return self.head, self.body

class Template1(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.head = self.concepts[1]
    self.body = frozenset({self.concepts[0], self.concepts[2]})
    self.number = 1

  def toTuple(self):
    return self.head, self.body

class Template2(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.head = self.concepts[2]
    self.body = frozenset(self.concepts[0:2])
    self.number = 2

  def toTuple(self):
    return self.head, self.body

def generateTuplesForOneSentence(sentence):
  concepts = extractConcepts(sentence)
  lst = [
    (Template0(concepts).toTuple(), extractFeatures(sentence, Template0(concepts))),
    (Template1(concepts).toTuple(), extractFeatures(sentence, Template1(concepts))),
    (Template2(concepts).toTuple(), extractFeatures(sentence, Template2(concepts)))]
  return lst

def generateTuples(sentences):
  tuples = map(generateTuplesForOneSentence, sentences)
  return tuples

def main():
  sentences = ['distance is speed times time', 'speed times time is distance',
               'force is mass times acceleration',
               'speed is acceleration times time', 'power is speed times force',
               'energy is force times distance', 'energy is power times time',
               'speed is distance divided by time'] # 'mass is force divided by acceleration',
               #'acceleration is speed divided by time']
  tuples = generateTuples(sentences)
  # [
  # [
  #     ('f', frozenset(['m', 'a']))
  #   ],
  #   [
  #     ('p', frozenset(['s', 'f']))
  #   ]
  # ]
  (solutions, globalStats) = solver.solver(tuples, [solver.featureConsistentTemplates, solver.validModels])

  # solMap = {}
  # for s in solutions.keys():
  #   varSet = set({s[0][0]}).union(s[0][1])
  #   k = (varSet,s[1][0].word,s[1][1].word)
  #   if not solMap.has_key(k):
  #     solMap[k] = solutions[s]
  #   elif solutions[s]>solMap[k]:
  #     solMap[k] = solutions[s]

  pprint.pprint(solutions)
  pprint.pprint(globalStats)

  f1TimesCount = 0
  f1DividedCount = 0
  f2TimesCount = 0
  f2DividedCount = 0
  f3TimesCount = 0
  f3DividedCount = 0

  for (k, c) in solutions.iteritems():
    if k[1][1].word == "times" and k[1][0].templateNumber == 0: f1TimesCount += c
    if k[1][1].word == "divided" and k[1][0].templateNumber == 0: f1DividedCount += c
    if k[1][1].word == "times" and k[1][0].templateNumber == 1: f2TimesCount += c
    if k[1][1].word == "divided" and k[1][0].templateNumber == 1: f2DividedCount += c
    if k[1][1].word == "times" and k[1][0].templateNumber == 2: f3TimesCount += c
    if k[1][1].word == "divided" and k[1][0].templateNumber == 2: f3DividedCount += c

  print f1TimesCount
  print f1DividedCount
  print f2TimesCount
  print f2DividedCount
  print f3TimesCount
  print f3DividedCount

  # for s in solMap.keys():
  #   print


  # features = extractFeatures(sentences[0],
  # Template0(extractConcepts(sentences[0])))
  # for f in features: print f.toString()

if __name__ == "__main__":
  sys.exit(main())
