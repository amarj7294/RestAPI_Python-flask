from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3 as sqlite
import sys
import json
from flask.ext.jsonpify import jsonify
import logging
import requests 

app = Flask(__name__)
api = Api(app)

class Movies(Resource):
	def get(self):
		try:
			conn = None
			conn = sqlite.connect(r'C:\Users\C5260086\Desktop\Project\Movies\MyMovies.db')
			cur = conn.cursor()
			url = request.path
			data={}
			if ('/getByName' in url):
				arg=request.args["name"]
				data={}
				qry = "SELECT CATEGORY,MOVIE_NAME from MOVIE_CATEGORY where MOVIE_NAME='{}'".format(str(arg))
				cur.execute(qry)
				data = {arg: [{"CATEGORY": i[0], "MOVIE_NAME":i[1]} for i in cur.fetchall()]}


			if ('/getByCategory' in url):
				arg=request.args["category"]
				data={}
				qry = "SELECT CATEGORY,MOVIE_NAME from MOVIE_CATEGORY where CATEGORY='{}'".format(str(arg))
				cur.execute(qry)
				data = {arg: [{"CATEGORY": i[0], "MOVIE_NAME":i[1]} for i in cur.fetchall()]}
				
			


			elif('/Allmovies' in url):
				qrydist = 'SELECT DISTINCT(CATEGORY) FROM MOVIE_CATEGORY'
				cur.execute(qrydist)
		    	dist = [i[0] for i in cur.fetchall()]
		    	qryMovie = 'SELECT CATEGORY,MOVIE_NAME from MOVIE_CATEGORY'
		    	cur.execute(qryMovie)
		    	movies = [i for i in cur.fetchall()]
		    	for d in dist:
		    		arrMovies=[]
		    		data[d]=arrMovies
		    		for movie in movies:
						if(movie[0]==d):
							arrMovies.append(movie[1]) 

			
					
		except Exception as e:
		    data = {"Error": str(e)}
		finally:
			if conn:
				conn.close()
		return data


	
	def post(self):
		try:
			post = {}
			data = request.get_json()
			conn = None
			arg=None
			conn = sqlite.connect(r'C:\Users\C5260086\Desktop\Project\Movies\MyMovies.db')
			cur = conn.cursor()
			name=data["name"]
			category=data["category"]
			qry="INSERT INTO MOVIES_NAMES (ID,MOVIE_NAME)VALUES ((SELECT MAX(ID) + 1 FROM MOVIES_NAMES),'{}')".format(name)
			qry2="INSERT INTO MOVIE_CATEGORY (CATEGORY,MOVIE_NAME)VALUES ('{}','{}')".format(category,name)
			cur.execute(qry)
			cur.execute(qry2)
			conn.commit()
			conn.close()
			post = {"success": data}				
		except Exception as e:
			post = {"Error": str(e),
					"data":data}
			
		return post,201


	def delete(self):
		try:
			conn = None
			conn = sqlite.connect(r'C:\Users\C5260086\Desktop\Project\Movies\MyMovies.db')
			cur = conn.cursor()
			data={}
			
			arg=request.args["name"]
			data={}
			qry = "DELETE from MOVIE_CATEGORY where MOVIE_NAME='{}'".format(str(arg))
			cur.execute(qry)
			qry2 = "DELETE from MOVIES_NAMES where MOVIE_NAME='{}'".format(str(arg))
			cur.execute(qry2)
			conn.commit()
			conn.close()
			data = {"success": "movie deleted",
					"name" : arg}
			
					
		except Exception as e:
		    data = {"Error": str(e)}
		
		return data





api.add_resource(Movies,'/add','/Allmovies', '/getByName' , '/getByCategory', '/delete')





if __name__ == '__main__':
    app.run(debug=True)