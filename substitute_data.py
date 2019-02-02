from flask import request
from flask_restful import Resource
import sqlite3
from sqlite3 import IntegrityError


class InsertData(Resource):
    def post(self):
        """
        Accepts new key, value pair and inserts it in the database
        :return: entire table in form of list of lists
        """
        table_data = []
        formatted_data = []
        if request.form['key'] and request.form['value']:
            key = request.form['key']
            value = request.form['value']
        
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            c.execute("INSERT INTO blank_data VALUES('"+key+"','"+value+"')")
            c.execute('SELECT * FROM blank_data')
            table_data = c.fetchall()
            for items in table_data:
                formatted_data.append({'key':items[0], 'value':items[1]})
            print(formatted_data)
            connection.commit()
        except IntegrityError:
            return {"exception": "Key already exists"}
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()
        
        return formatted_data
    
    
class UpdateData(Resource):
    def post(self):
        """
        Accepts key, value pair and updates it in the database
        :return: entire table in form of list of lists
        """
        table_data = []
        formatted_data = []
        if request.form['key'] and request.form['value']:    
            key = request.form['key']
            value = request.form['value']
        
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            c.execute("UPDATE blank_data SET value="+value+" WHERE key='"+key+"'")
            c.execute('SELECT * FROM blank_data')
            table_data = c.fetchall()
            for items in table_data:
                formatted_data.append({'key':items[0], 'value':items[1]})
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()
 
        return formatted_data


class DeleteData(Resource):
    def post(self):
        """
        Accepts key and deletes it in the database
        :return: entire table in form of list of lists
        """
        table_data = []
        formatted_data = []
        if request.form['key']:
            key = request.form['key']
        
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            c.execute("DELETE FROM blank_data WHERE key='"+key+"'")
            c.execute('SELECT * FROM blank_data')
            table_data = c.fetchall()
            for items in table_data:
                formatted_data.append({'key':items[0], 'value':items[1]})
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()

        return formatted_data


class ReadData(Resource):
    def post(self):
        """
        :return: entire table in form of list of lists
        """
        table_data = []
        formatted_data = []
        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            c.execute('SELECT * FROM blank_data')
            table_data = c.fetchall()
            for items in table_data:
                formatted_data.append({'key':items[0], 'value':items[1]})
            connection.commit()
        except Exception as exception:
            print(exception)
        finally:
            if connection:
                connection.close()
        
        return formatted_data
