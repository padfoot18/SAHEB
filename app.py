from flask import Flask, request
from flask_restful import Resource, Api
from deeppavlov import build_model, configs
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

model = None
paragraph = """The application process will remain open at 04th of July to 14th of August. 
               Application form for admission is available at the Somaiya website. Our hours are 9am-8pm every day. 
               The fee amount is INR 150000 and the hostel fees is INR 5000. The application fee is the 5000. 
               There are total 7 courses are available at the university."""


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class ChatBot(Resource):
    def post(self):
        question = request.form['question']
        print(question)
        answer = model([paragraph], [question])
        print(answer)
        return answer


def load_model():
    global model
    model = build_model(configs.squad.squad, download=False)


api.add_resource(HelloWorld, '/')
api.add_resource(ChatBot, '/chat/')


if __name__ == '__main__':
    load_model()
    app.run(host='127.0.0.1', port=8888, debug=True)
