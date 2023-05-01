from flask import *
from app.blueprint import user_blueprint
import json
from functools import wraps
import requests
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config['JSON_SORT_KEYS']=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000, debug = True)