from flask import Flask, request
from flask_restful import Resource, Api
from deeppavlov import build_model, configs
from flask_cors import CORS
from substitute_data import InsertData, UpdateData, ReadData, DeleteData
from paragraph_api import Paragraph
import sqlite3
import re
from keras.models import load_model
import string
# Load stop words
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)
api = Api(app)

model = None
model_small_talk = None
paragraph = None
values = dict()
word_to_index, index_to_word, word_to_vec_map = None


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
        question = request.form['question']
        print(question)
        answer = model([paragraph], [question])[0][0]
        print(answer)



        if answer == '' or answer == None:
            # small talk model
            X_test = sentences_to_indices(np.array(test_sentence), word_to_index, maxLen)
            pred = model_small_talk.predict(X_test)
            pred_index = np.argmax(pred, axis=1)

            if pred_index in [0, 1, 2]:
                pass
            else:
                answer = "Sorry, I couldn't understand" 
        else:
            keys = re.findall('##[^\s.]*', answer)
            if keys:
                print(keys)
                for k in keys:
                    answer = re.sub(k, values[k[2:]], answer)
        print(answer)
        return answer


def load_all_model():
    # load the model into memory
    global model
    global model_small_talk
    global word_to_index, index_to_word, word_to_vec_map
    model = build_model(configs.squad.squad, download=False)
    model_small_talk = load_model('./model/small_talk/trained_lstm_128_128_dropout_4_3.h5')
    word_to_index, index_to_word, word_to_vec_map = read_glove_vecs('./model/glove/glove.6B.50d.txt')


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
