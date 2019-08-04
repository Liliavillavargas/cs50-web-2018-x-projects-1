import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#connect with database Adminer CS50 Heroku.
engine = create_engine('postgres://nxugbrmngapkdm:c9498cebaf192f3c5b124b422049a712c69759046a0f8bad9849b3409e26d646@ec2-107-20-155-148.compute-1.amazonaws.com:5432/d9q2pp1sgjekv')
db = scoped_session(sessionmaker(bind=engine))


def main():
    #open books.csv database for upload
    f= open("books.csv", "r")

    #Read database with delimiter " , " - field (isbn, title, author and year)
    reader = csv.reader(f, delimiter=',')
    next(reader)
    #Insert into database Books in Adminer CS50
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
               {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()
        #Print for screen and control errors.
        print(f"Added book with ISBN: {isbn} Title: {title}  Author: {author}  Year: {year}")

if __name__ == '__main__':
    main()
