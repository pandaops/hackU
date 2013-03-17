import nltk.tokenize as tokenize
import nltk
import random
random.seed(3)

def bag_of_words(words):
    return dict([word, True] for word in words)

def document_features(document):
    features = {}
    for word in word_features:
        features[word] = (word in document)
        # features['contains(%s)' % word] = (word in document_words)
    return features

movie_reviews = nltk.corpus.movie_reviews

documents = [(set(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]

train_set = [(document_features(d), c) for (d, c) in documents[:800]]

classifier = nltk.NaiveBayesClassifier.train(train_set)

classifier.show_most_informative_features()
for word in ('brilliant', 'hate'):
    # No hope in passing the tests if word is not in word_features
    assert word in word_features
    print('probability {w!r} is positive: {p:.2%}'.format(
        w = word, p = classifier.prob_classify({word : True}).prob('pos')))

tests = ["i love this city",
         "i hate this city",
         "This is magnificient",
         "This was horrible",
        "I will never watch this again",
        "I will watch this many times"]

for test in tests:
    words = tokenize.word_tokenize(test)
    feats = bag_of_words(words)
    print('{s} => {c}'.format(s = test, c = classifier.prob_classify(feats)))
