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
        return None

    def post(self):
        """
        Accepts the modified paragraph in a post request. Updates the paragraph in the database.
        :return:
        """
        # TODO (2) when a paragraph is submitted in a post request, update the existing paragraph in the database
        return None
