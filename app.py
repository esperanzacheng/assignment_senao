from flask import Flask, jsonify
from app.blueprint import user_blueprint
from flask_cors import CORS

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config['JSON_SORT_KEYS']=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.register_blueprint(user_blueprint)
CORS(app)

@app.errorhandler(404)
def resource_not_found(e):
    return (jsonify(success = False, reason=str(e)), 404)

@app.errorhandler(405)
def method_not_allowed(e):
    return (jsonify(success = False, reason=str(e)), 405)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)