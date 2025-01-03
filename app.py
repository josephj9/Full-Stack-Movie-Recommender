from flask import Flask, request, jsonify, render_template, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from recommender import search, collaborative_filtering
from models import Base, Movie, Rating, Session

app = Flask(__name__)

# Searching the movie
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/search', methods=["GET"])
def search_movie():
    title = request.args.get('title', '')
    genre = request.args.get('genre', None)
    
    with Session() as session:  
        result = search(session, title, genre)
    
    return jsonify(result.to_dict(orient="records"))


# Recommending the movie (Takes in a movie ID)
@app.route('/recommendations/<int:movieid>', methods=["GET"])
def recommendations(movieid):
    with Session() as session:
        result = collaborative_filtering(movieid, session) 
    return jsonify(result) 

if __name__ == "__main__":
    app.run(debug=True, port=5000)  

