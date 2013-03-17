from __future__ import division
from django.shortcuts import *
import nltk.tokenize as tokenize
from django.template.context import *
import nltk
import random
import twitter
from collections import Counter
import imdb
random.seed(3)

def home(request):
    s=[]
    api=connect()
    if api.VerifyCredentials():
        if request.method=='POST':
            movie=request.POST['movie']
            reviews = []
            reviews_final = []
            for i in range(1,2):
                reviews.extend([(x.AsDict()['text'], api.GetRetweets(x.AsDict()['id'])) for x in api.GetSearch(term='#'+str(movie),per_page=100, page=i)])
            print reviews
            for line, val in reviews:
                 line=line
                 line=line.split()
                 if val:
                    for word in line:
                         if word.startswith('#') or word.startswith('@'):
                             line.remove(word)
                    line=' '.join(line)
                    reviews_final.extend([line, val])
            total_rating=0
            for each in reviews_final:
                rating+=each[1]*wrapper([each[0]])
                total_rating+=each[1]*1.5
            rating/= total_rating
            print rating
    return render_to_response('home.html',locals(),context_instance=RequestContext(request))

def bag_of_words(words):
    return dict([word, True] for word in words)

def connect():
    api = twitter.Api(consumer_key='20GUN4VeGC6femOun8VdzA',consumer_secret='gmouyeFmCXQQANzEgU9zWfC2QRvDQYYxBlpCv5cA1KI', access_token_key='1273494510-jSQemAFyFlDg5yDFtqHWpkNwt2zUPnptxNo17Ib', access_token_secret='cCk6owpDysCqRLbQyenmuMevGrbEV7oX3wNVRy34')
    return api

def wrapper(review):
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

    c=[]
    for line in review:
        words = tokenize.word_tokenize(line)
        feats = bag_of_words(words)
        c.append(classifier.classify(feats))
    for element in c:
        if element == 'pos':
            element = 1.5
        else:
            element = 0
    return c
