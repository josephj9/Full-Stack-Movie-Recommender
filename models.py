from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

#Add the columns plus the clean title
class Movie(Base):
    __tablename__ = 'movies'
    id = Column( Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    clean_title = Column(String, nullable=True)


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False)
    movieid= Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

import re

engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session() 

# loop through the csv files and add to the database
print("Loading movies.csv...")
movies_df = pd.read_csv('movies.csv')
for index, row in movies_df.iterrows():
    existing_movie = session.query(Movie).filter_by(title=row['title'], genre=row['genres']).first()
    if not existing_movie:
        movie = Movie(title=row['title'], genre=row['genres'], clean_title=re.sub("[^a-zA-Z0-9 ]", "", row['title']))
        session.add(movie)
print("Movies loaded.")

print("Loading ratings.csv...")
ratings_df = pd.read_csv('filtered_ratings.csv')
for index, row in ratings_df.iterrows():
    existing_rating = session.query(Rating).filter_by(userid=row['userId'], movieid=row['movieId']).first()
    if not existing_rating:
        rating = Rating(userid=row['userId'], movieid=row['movieId'], rating=row['rating'])
        session.add(rating)
print("Ratings loaded.")

session.commit()
session.close()

