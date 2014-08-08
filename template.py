import string
import sys

CONCEPTS = {'distance': 'd', 'speed': 's', 'time': 't',
            'power': 'p', 'energy': 'e', 'force': 'f',
            'acceleration': 'a'}

RELATIONS = ['is', 'times', 'divided by']

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

  def toString(self):
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
    self.body = set(self.concepts[1:3])
    self.number = 0

  def toTuple(self):
    return self.head, self.body

class Template1(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.head = self.concepts[1]
    self.body = {self.concepts[0], self.concepts[2]}
    self.number = 1

  def toTuple(self):
    return self.head, self.body

class Template2(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.head = self.concepts[2]
    self.body = set(self.concepts[0:2])
    self.number = 2

  def toTuple(self):
    return self.head, self.body

def generateTuplesForOneSentence(sentence):
  concepts = extractConcepts(sentence)
  tuples = (
    Template0(concepts).toTuple(), Template1(concepts).toTuple(), Template2(concepts).toTuple())
  return tuples

def generateTuples(sentences):
  tuples = map(generateTuplesForOneSentence, sentences)
  return tuples

def main():
  sentences = ['distance is speed times time', 'force is mass times acceleration',
               'speed is acceleration times time', 'power is speed times force',
               'energy is force times distance', 'energy is power times time']
  tuples = generateTuples(sentences)

  features = extractFeatures(sentences[0],
                             Template0(extractConcepts(sentences[0])))
  for f in features: print f.toString()

if __name__ == "__main__":
  sys.exit(main())