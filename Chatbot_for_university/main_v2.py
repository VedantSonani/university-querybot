import training
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

from flask import Flask, render_template, request, jsonify
import tensorflow
import tflearn
import numpy
import os
import random
import pickle
import json

intent_file = "intents_3.json"
NO_OF_NEURONS = 20
app = Flask(__name__)

class chatbot:
    def __init__(self):
        with open("data.pickle", "rb") as file:
            self.words, self.labels, self.training, self.output = pickle.load(file)

        tensorflow.compat.v1.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, NO_OF_NEURONS)
        net = tflearn.fully_connected(net, NO_OF_NEURONS)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

        try:
            self.model.load("models/model.tflearn")
        except:
            print("Model not present, train the model first...")
            exit()

    def input_encoded(self, user_input, words):
        bag = [0 for i in range(len(words))]

        user_input = nltk.word_tokenize(user_input)
        user_input = [stemmer.stem(w.lower()) for w in user_input]

        for word in user_input:
            if word in words:
                bag[words.index(word)] = 1
        
        return numpy.array(bag)

    def chat(self, user_input):        
        result = self.model.predict([self.input_encoded(user_input, self.words)])[0]
        result_index = numpy.argmax(result)


        if result[result_index] >= 0.7:
            tag = self.labels[result_index]

            with open(intent_file) as file:
                data = json.load(file) 

            for t in data["intents"]:
                if t["tag"] == tag:
                    responses = t["responses"]
                    break
            
            output = random.choice(responses)
            return output
            # print("Bot: ", output)
            # print("percent: ", result[result_index])

        else:
            return "I didn't understand that. Please ask another question."
            # print("I didn't understand that. Please ask another question.")
            # print("percent: ", result[result_index])



@app.route('/')
def home():
    # return render_template('chat.html')
    return render_template('index-template.html')

@app.route('/get_response', methods=['POST'])
def respond():
    user_message = request.json['message']
    bot_response = obj.chat(user_message)

    return jsonify({'response': bot_response})


if __name__=="__main__":
    obj = chatbot()
    # print(obj.chat("what can i get in food?"))
    os.system('cls')
    app.run(debug=True)