#para usted en este proyecto hay un archivo
#llamado books.csv,
#escriba un programa
#que lleve los libros e impórtelos a su base de datos PostgreSQL. Primero
#deberá decidir qué tablas crear, qué columnas deben tener esas tablas y
#cómo deben relacionarse entre sí. Ejecute este programa
#ejecutando python3 import.pypara importar los libros a su base de datos,
#y envíe este programa con el resto del código de su proyecto.


import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for id_book,isbn_book,title_book,author_book,year_book in reader:
        db.execute("INSERT INTO books (id_book,isbn_book,title_book,author_book,year_book) VALUES (:isbn, :title, :author, :year)",
                    {"isbn_book": isbn, "title_book": title, "author_book": author, "year_book: year"})
        print(f"Added books from {id_book} to {year_book}")
    db.commit()

if __name__ == "__main__":
    main()
