#Establecer la variable de entorno FLASK_APPpara ser application.py.
#En Windows, el comando es en su lugar set
#*****FLASK_APP=application.py.****
#Es posible que desee establecer opcionalmente
#la variable de entorno ****FLASK_DEBUGa 1, ***que activará el depurador de
#Frasco y que se recargue automáticamente su aplicación web cada vez
#que guarde un cambio en un archivo.
#Establezca la variable de entorno DATABASE_URLpara que sea el URI de su
#base de datos, que debería poder ver en la página de credenciales en
#Heroku.
#***Ejecutar flask runpara iniciar su aplicación Flask.****
#Si navega a la URL proporcionada por flask, ¡debería ver el texto "Project
#----1: TODO"!




import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#"Project 1: TODO"

@app.route("/")
def index():
    return render_template("Register.html")
