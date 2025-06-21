import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import json
import pickle 
import random
import os


intent_file = "intents_3.json"
NO_OF_NEURONS = 20
NO_OF_EPOCH = 500

def preprocess():
    with open(intent_file) as file:
        data = json.load(file)


    words = []  # for tokenized pattern or vocabulary of the model
    labels = [] # list of all intent
    docs_x = [] # original pattern
    docs_y = [] # intent associated with that pattern

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            tokens = nltk.word_tokenize(pattern)

            words.extend(stemmer.stem(w.lower()) for w in tokens if w != "?")
            docs_x.append([stemmer.stem(w.lower()) for w in tokens])
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    # remove duplicates    
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    # empty list for output 
    out_empty = [0 for _ in range(len(labels))]

    # performing one-hot encoding for training data and output
    # training --> pattern 
    # output --> labels
    for intent, pattern in zip(docs_y, docs_x):
        bag = []
        
        for w in words:
            if w in pattern:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(intent)] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)
    
    return training, output, words, labels


def train_model(training, output):
    tensorflow.compat.v1.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, NO_OF_NEURONS)
    net = tflearn.fully_connected(net, NO_OF_NEURONS)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)

    model.fit(training, output, n_epoch=NO_OF_EPOCH, batch_size=8, show_metric=True)
    model.save("models/model.tflearn")


def main():
    try:
        with open("data.pickle", "rb") as file:
            words, labels, training, output = pickle.load(file)
    except:
        print("processing data...")
        training, output, words, labels = preprocess()
    
    
    print("training model...")
    train_model(training, output)
      

if __name__=="__main__":
    main()