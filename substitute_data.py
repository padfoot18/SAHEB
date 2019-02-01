from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3


class SubstituteData(Resource):
    def post(self):
        college_fee = request.form['college_fee']
        print(college_fee)
        application_fee = request.form['application_fee']
        print(application_fee)
        hostel_fee = request.form['hostel_fee']
        print(hostel_fee)

        try:
            connection = sqlite3.connect('test.db')
            c = connection.cursor()
            # c.execute('CREATE TABLE blank_data (application_fee text, college_fee text, hostel_fee text)')
            c.execute('INSERT INTO blank_data VALUES('+application_fee+','+college_fee+','+hostel_fee+')')
            connection.commit()
        except Exception as exception:
            print(e)
        finally:
            if connection:
                connection.close()
        
        return True



