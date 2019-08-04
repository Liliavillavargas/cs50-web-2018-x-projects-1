import requests
from flask import  redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Link database
engine = create_engine('postgres://nxugbrmngapkdm:c9498cebaf192f3c5b124b422049a712c69759046a0f8bad9849b3409e26d646@ec2-107-20-155-148.compute-1.amazonaws.com:5432/d9q2pp1sgjekv')

db = scoped_session(sessionmaker(bind=engine))


# Index Page
@app.route("/")
def index():
    return render_template("index.html")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        email = request.form.get("Email")

        # Check if user is registered
        if db.execute("SELECT id FROM users WHERE email= :email", {"email": email}).fetchone() is not None:
            return render_template ("login.html", work="Login",
                                   error_message="The user has already registered. Please Login.")

        #type name and password and encrypt password
        name=request.form.get("name")
        password = request.form.get("Password")
        db.execute("INSERT INTO users (email, name, password) VALUES (:email, :name, :password)",
                   {"email": email, "name":name,"password": generate_password_hash(password)})
        db.commit()
        return render_template("login.html", work="Login")

    return render_template("login.html", work="Register")


# Logout for the website
@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")



#Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Login with email and check if it already exist
    if request.method == "POST":

        email = request.form.get("Email")
        user = db.execute("SELECT id, password FROM users WHERE email= :email", {"email": email}).fetchone()

        # Redirect to Register if email not exist.
        if user is None:
            return render_template("login.html", error_message="Unregistered user.",
                                   work="Register")
        #if exist enter password and check  it
        password = request.form.get("Password")
        if not check_password_hash(user.password, password):
            return render_template("login.html", error_message= email + ".  Please try again. Password is wrong", work="Login")
        session["user_email"] = email
        session["user_id"] = user.id

    #if star session go to search and if not Login.
    if request.method == "GET" and "user_email" not in session:
        return render_template("login.html", work="Login")
    return render_template("search.html", user_email=email)


# Page search books
@app.route("/search", methods=["GET","POST"])
def search():
    # Confirm Log In.
    if "user_email" not in session:
        return render_template("login.html", work="Login")

    #Select for column and type searched column
    column = request.form.get("column")
    query = request.form.get("query")

    #Only are ISBN, TITLE AND AUTHOR to search.
    if column != "year":
        #Search and select by column
        table_result = db.execute("SELECT * FROM books WHERE UPPER(" + column + ") LIKE :query ORDER BY year DESC",
                               {"query": "%" + query.upper() + "%"}).fetchall()
    #field length
    if len(table_result):
        return render_template("table_result.html", table_result=table_result, user_email=session["user_email"])

        if not len(table_result):
            return render_template("table_result.html", table_result=table_result, message=message,
                               user_email=session["user_email"])
    #Error Message 404 No Found
    else:
        return render_template("error.html", error_message="File Not Found.")


# Result of the search
@app.route("/detail_books/<int:book_id>", methods=["GET", "POST"])
def detail_books(book_id):
    # Confirm Log In.
    if "user_email" not in session:
        return render_template("login.html", error_message="Please Login First", work="Login")


    book = db.execute("SELECT * FROM books WHERE id = :book_id", {"book_id": book_id}).fetchone()

    # Sending review of books
    if request.method == "POST" :

        user_id = session["user_id"]
        rating = request.form.get("rating")
        comment = request.form.get("comment")


        if db.execute("SELECT * FROM review WHERE user_id = :user_id AND book_id = :book_id",
                      {"user_id": user_id, "book_id": book_id}).fetchone() is None:
            db.execute(
                "INSERT INTO review (user_id, book_id, rating, comment) VALUES (:user_id, :book_id, :rating, :comment)",
                {"book_id": book.id, "user_id": user_id, "rating": rating, "comment": comment})
        else:
            return render_template("error.html", error_message="Sorry. You cannot add second review.")
        db.commit()


    # Return JSON since Goodreads API with my Key API

    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "DhulKg99GLTTnBKhSAWWw", "isbns": book.isbn}).json()["books"][0]

    #store information books for print on screen
    ratings_count = res["ratings_count"]
    average_rating = res["average_rating"]
    reviews = db.execute("SELECT * FROM review WHERE book_id = :book_id", {"book_id": book.id}).fetchall()
    users = []
    for review in reviews:
        email = db.execute("SELECT email FROM users WHERE id = :user_id", {"user_id": review.user_id}).fetchone().email
        users.append((email, review))

    return render_template("detail_books.html", book=book, users=users,
                           ratings_count=ratings_count, average_rating=average_rating, user_email=session["user_email"],)


# API Goodreads Query for ISBN
@app.route("/api/<ISBN>", methods=["GET"])
def api(ISBN):
    book = db.execute("SELECT * FROM books WHERE isbn = :ISBN", {"ISBN": ISBN}).fetchone()
    #Invlaid ISBN API
    if book is None:
        return render_template("error.html", error_message="Invalid ISBN. Not Found 404 ")

    reviews = db.execute("SELECT * FROM review WHERE book_id = :book_id", {"book_id": book.id}).fetchall()
    #Start variables
    rating=0;
    count=0;

    for review in reviews:
        count += 1
        rating += review.rating
    if count:
        average_rating = rating / count
    else:
        average_rating = 0

    #Answer JSON API
    return jsonify(  isbn=book.isbn, title=book.title, author=book.author, year=book.year, review_count=count,average_rating_score=average_rating)


if __name__ == "__main__":
    app.run(debug=True)
