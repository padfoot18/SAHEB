from flask import Flask, request
from flask_restful import Resource, Api
from deeppavlov import build_model, configs
from flask_cors import CORS
from substitute_data import InsertData, UpdateData, ReadData, DeleteData
from paragraph_api import Paragraph
import sqlite3
import re


app = Flask(__name__)
CORS(app)
api = Api(app)

model = None
paragraph = None
values = dict()

# paragraph = """The application process will remain open at 04th of July to 14th of August.
#                Application form for admission is available at the Somaiya website. Our hours are 9am-8pm every day.
#                The college fee amount is INR 150000 and the hostel fees is INR 5000. The application fee is the 5000.
#                There are total 7 courses are available at the university."""


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class ChatBot(Resource):
    def post(self):
        question = request.form['question']
        print(question)
        answer = model([paragraph], [question])[0][0]
        if re.match('##[^\s\.]*', answer):
            keys = re.findall('##[^\s\.]*', answer)
            print(keys)
            for k in keys:
                answer = re.sub(k, values[k[2:]], answer)
        print(answer)
        return answer


def load_model():
    # load the model into memory
    global model
    model = build_model(configs.squad.squad, download=False)


def load_data():
    # TODO (3) load the paragraph and all the key-value pairs into the global variables
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


api.add_resource(HelloWorld, '/')
api.add_resource(ChatBot, '/chat/')
api.add_resource(InsertData, '/values/insert/')
api.add_resource(UpdateData, '/values/update/')
api.add_resource(DeleteData, '/values/delete/')
api.add_resource(ReadData, '/values/read/')
api.add_resource(Paragraph, '/para/')


if __name__ == '__main__':
    load_data()
    load_model()
    app.run(host='127.0.0.1', port=8888, debug=True)
