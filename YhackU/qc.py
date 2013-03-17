import nltk
from nltk.corpus import qc
import random
import string

s = qc.tuples()

temp = []
bad=['the']

for x in string.punctuation:
    bad.append(x)

for x,y in s:
    temp += nltk.word_tokenize(y)

all_words = nltk.FreqDist(w.lower() for w in temp if w.isalpha() and w not in bad)

word_features = all_words.keys()[:800]

def qc_features(question):
    words = question.split()
    for val in bad:
        if val in words:
            words.remove(val)
    features = {}
    features['(Words are)'] = words[1]+' '+words[0]
    words=set(words)
    for word in words:
        features['contains(%s)' % word] = (word in words)
    return features

def further_qc_features(question):
    words=set(question.split()[2:])
    for val in bad:
        if val in words:
            words.remove(val)
    features={}
    for word in word_features:
        features['contains(%s)' % word] = (word in words)
    return features

print "Processing data"
featuresets = [(qc_features(d),c.split(':')[0]) for (c,d) in s]
advanced_featuresets = [(further_qc_features(d),c.split(':')[0]) for (c,d) in s]
print "Done..."
train, dev, test = featuresets[:5500] , featuresets[5500:5600], featuresets
atrain, atest = advanced_featuresets[:5500],advanced_featuresets
print "Learning"
classifier = nltk.NaiveBayesClassifier.train(train)
advanced_classifier = nltk.NaiveBayesClassifier.train(train)
print "Done..."
print "Running Tests"
print nltk.classify.accuracy(classifier, test)
while True:
    q=raw_input()
    genre= classifier.classify(qc_features(q))
    if genre in ['LOC','NUM']:
         genre=advanced_classifier.classify(further_qc_features(q))
         print genre
    else:
         print genre
classifier.show_most_informative_features(5)
