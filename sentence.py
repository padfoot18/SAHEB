from flask import Flask, render_template, request
from flask_restful import Resource, Api
import sqlite3


app = Flask(__name__)
api = Api(app)


class Read(Resource):
    def post(self):
        """read data from table"""
        try:
            connection=sqlite3.connect('chat.db')
            c=connection.cursor()
            c.execute('SELECT * FROM paragraph')
            para=c.fetchall()
            print(para)
            connection.commit()
        except sqlite3.IntegrityError:
            return {"error"}
        except Exception as exception:
            print(exception)
        finally:
            if connection:
               connection.close()
               return para


class Insert(Resource):
    def post(self):
        if request.form['key'] and request.form['value'] and request.form['sentence']:
            key=request.form['key']
            value=request.form['value']
            sentence=request.form['sentence']

        try:
            connection=sqlite3.connect('chat.db')
            c=connection.cursor()
            c.execute('SELECT * FROM paragraph')
            para=c.fetchall()

            para=para+sentence
            c.execute("INSERT INTO data VALUES('"+key+"','"+value+"')")
            c.execute("UPDATE paragraph SET para="+para+"")
            print(para)
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
               connection.close()

        return para


api.add_resource(Read,'/api/v2/read/')
api.add_resource(Insert,'/api/v2/insert/')

if __name__ == '__main__':
    app.run(debug=True)
