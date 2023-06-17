from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #  configure sqlalchemy and db
from datetime import datetime

app = Flask(__name__)

# COnfuguring  DB and sqlalchemy with db-sqlite
# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db" #/// mean relative path and //// i.e. 4 slash used for absolute path
db = SQLAlchemy(app)

# basic understanding how routes works:
@app.route('/test')
def hello_world():
    return 'This is my first API call!'

@app.route('/about')
def about():
    return 'This is my about!'


@app.route("/contact")
def hello():
    return "<p>Hello, i am contact url</p>"

@app.route('/success/<int:score>')
def success(score):
    res=""
    # if score>=50:
    #     res="PASS"
    # else:
    #     res='FAIL'
    exp={'score':2,'res':3}
    # exp={'score':score,'res':res}
    return exp
   

@app.route('/post', methods=["POST"])
def testpost():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)


@app.route('/homeCheck')
def homeCheck() :
    page = "I am variable from python app.py"
    return render_template('index.html', name=page)

# above are just routing testing . And now below the real logic

#  creating model



if __name__ == "__main__":
    app.run(debug=True)