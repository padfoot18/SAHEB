from flask import Flask, request
from flask_restful import Resource, Api
from deeppavlov import build_model, configs
from flask_cors import CORS
from substitute_data import InsertData, UpdateData, ReadData, DeleteData
from paragraph_api import Paragraph
import sqlite3
import re
from keras.models import load_model
from helper import *
import numpy as np
import tensorflow as tf
from nltk.corpus import stopwords
from string import punctuation

app = Flask(__name__)
CORS(app)
api = Api(app)

model = None
model_basic_response = None
paragraph = None
values = dict()
word_to_index = None
index_to_word = None
word_to_vec_map = None

g1 = tf.Graph()
g2 = tf.Graph()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@app.route('/hello/')
def hello_world():
    return 'Hello, World!'


@app.before_first_request
def init_stuff():
    """
    Initialize the data and the model before first request is processed.
    :return: None
    """
    load_data()
    load_all_model()


class ChatBot(Resource):
    def post(self):
        threshold = 45000
        minimum_match = 1

        question = request.form['question']
        question = question.strip()
        question = question
        if question[-1] != "?":
            question += '?'
        print(question)

        print(question)

        answer = None
        answer_main = None

        with g2.as_default():
            answer = model([paragraph], [question])
            print(answer)
            answer_main = answer[0][0]





        keys = re.findall('zxyw[^\s.]*', answer_main)
        if keys:
            print(keys)
            for k in keys:
                answer_main = re.sub(k, values[k[4:]], answer_main)
        print(answer_main)

        if answer[2][0] < threshold:
            question_list = removeStopWords(question)
            answer_list = removeStopWords(answer_main)
            print(question_list, answer_list)
            count = 0
            for i in question_list:
                for j in answer_list:
                    if i == j:
                        count += 1
            if count >= minimum_match:
                return answer_main
            else:





                return "Sorry i didn't get that!"
        else:
            return answer_main
















        with g2.as_default():
            answer = model([paragraph], [question])
            print(answer)
            answer = answer[0][0]

        maxLen = 10
        if answer == '' or answer is None:

            with g1.as_default():
                # basic response model
                X_test = sentences_to_indices(np.array([question]), word_to_index, maxLen)
                pred = model_basic_response.predict(X_test)
                pred_index = int(np.argmax(pred, axis=1)[0])

                basic_reply = ['Hi there, how can I help?', 'See you later, thanks for visiting', 'Happy to help!']

                if pred_index in [0, 1, 2]:
                    answer = basic_reply[pred_index]
                else:
                    answer = "Looks like your question is out of my scope. I am still learning but I am now only able to answer question related to Admission process"
        else:
            keys = re.findall('zxyw[^\s.]*', answer)
            if keys:
                print(keys)
                for k in keys:
                    answer = re.sub(k, values[k[4:]], answer)
        print(answer)
        return answer


def removeStopWords(words):
    customStopWords = set(stopwords.words('english') + list(punctuation))
    return [word for word in word_tokenize(words) if word not in customStopWords]


def load_all_model():
    # load the model into memory
    global model
    global model_basic_response
    global word_to_index, index_to_word, word_to_vec_map
    global g1
    global g2

    with g1.as_default():
        # basic response model
        model_basic_response = load_model('./model/basic_response_model/trained_lstm_128_128_dropout_4_3.h5')

    with g2.as_default():
        # paragraph model
        model = build_model(configs.squad.squad, download=False)

    # glove embedding
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('./model/glove/glove.6B.50d.h5')


def load_data():
    # DONE (3) load the paragraph and all the key-value pairs into the global variables
    global paragraph
    global values
    para_sql = "select * from paragraph;"
    values_sql = "select * from blank_data;"
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(para_sql)
        paragraph = cursor.fetchall()[0][0]
        cursor.execute(values_sql)
        values_list = cursor.fetchall()

        for i in values_list:
            values.update({i[0]: i[1]})
        print(paragraph)
        print(values)

    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


api.add_resource(ChatBot, '/chat/')
api.add_resource(InsertData, '/values/insert/')
api.add_resource(UpdateData, '/values/update/')
api.add_resource(DeleteData, '/values/delete/')
api.add_resource(ReadData, '/values/read/')
api.add_resource(Paragraph, '/para/')

if __name__ == '__main__':
    # load_data()
    # load_all_model()
    app.run(host='127.0.0.1', port=8888, debug=True)
