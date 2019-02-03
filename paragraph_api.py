from flask import request
from flask_restful import Resource
import sqlite3


class Paragraph(Resource):
    def get(self):
        """
        Accepts a get request.
        :return: entire paragraph present in the database
        """
        # TODO (1) when a get request is performed, return the existing paragraph to the caller
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            c.execute('SELECT * FROM paragraph')
            para = c.fetchall()
            print(para[0][0])
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()
                return para[0][0]

    def post(self):
        """
        Accepts the modified paragraph in a post request. Updates the paragraph in the database.
        :return: updated paragraph
        """
        if request.form['paragraph']:
            paragraph = request.form['paragraph']

        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()

            c.execute('UPDATE paragraph SET para="' + paragraph + '";')
            print(paragraph)
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()

        return paragraph
