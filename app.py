from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #  configure sqlalchemy and db
from datetime import datetime

app = Flask(__name__)

# COnfuguring  DB and sqlalchemy with db-sqlite

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
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



# routes 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)