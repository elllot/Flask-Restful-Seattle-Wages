from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import flask_restful.representations.json

engine = create_engine('sqlite:///myDB.db')

app = Flask(__name__)
api = Api(app)

app_settings = app.config['RESTFUL_JSON'] = {'indent':4}

class Departments_Meta(Resource):
	def get(self):
		conn = engine.connect()
		query = conn.execute("select distinct Department from seattle_salaries")
		return {'departments': [i[0] for i in query.cursor.fetchall()]}

class Departmental_Salary(Resource):
	def get(self, department):
		conn = engine.connect()
		query_string = "select * from seattle_salaries where Department='{0}'".format(department)
		query = conn.execute(query_string)
		return {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}

api.add_resource(Departmental_Salary, '/dept/<string:department>')
api.add_resource(Departments_Meta, '/departments')

if __name__ == '__main__':
	app.run()