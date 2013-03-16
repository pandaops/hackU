import nltk
from nltk.corpus import qc
import random
import string

s = qc.tuples()

temp = []
bad=['the','is']

for x in string.punctuation:
    bad.append(x)

for x,y in s:
    temp += nltk.word_tokenize(y)

all_words = nltk.FreqDist(w.lower() for w in temp if w.isalpha() and w not in bad)

word_features = all_words.keys()[:800]

def qc_features(question):
    words = set(question.split())
    for val in bad:
        if val in words:
            words.remove(val)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in words)
    return features

print "Processing data"
featuresets = [(qc_features(d),c.split(':')[0]) for (c,d) in s]
print "Done..."
train, dev, test = featuresets , featuresets[5500:5600], featuresets[4780:4810]
print "Learning"
classifier = nltk.NaiveBayesClassifier.train(train)
print "Done..."
print "Running Tests"
print nltk.classify.accuracy(classifier, test)
while True:
    q=raw_input()
    print classifier.classify(qc_features(q))
print "Done..."
classifier.show_most_informative_features(5)
