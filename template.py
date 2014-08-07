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
    return '"{}" in operator slot {} for template {}'.format(self.word, self.slot, self.templateNumber)

class Template:
  def __init__(self, concepts):
    self.concepts = concepts

class Template1(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.concepts0 = self.concepts[0]
    self.concepts1 = self.concepts[1]
    self.concepts2 = self.concepts[2]
    self.number = 1

  def toTuple(self):
    return self.concepts0, self.concepts1, self.concepts2

class Template2(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.concepts0 = self.concepts[1]
    self.concepts1 = self.concepts[2]
    self.concepts2 = self.concepts[0]
    self.number = 2

  def toTuple(self):
    return self.concepts0, self.concepts1, self.concepts2

class Template3(Template):
  def __init__(self, concepts):
    Template.__init__(self, concepts)
    self.concepts0 = self.concepts[2]
    self.concepts1 = self.concepts[0]
    self.concepts2 = self.concepts[1]
    self.number = 3

  def toTuple(self):
    return self.concepts0, self.concepts1, self.concepts2

def main():
  sent = 'Distance is speed times time'
  print sent
  concepts = extractConcepts(sent)
  t1 = Template1(concepts)
  print t1.toTuple()

  features = extractFeatures(sent, t1)
  for f in features: print f.toString()

  return 0

if __name__ == "__main__":
  sys.exit(main())