from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
app = Flask(__name__)
CORS(app)

app.secret_key = "This is a very very secret key!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:LoulouOona12@localhost:5432/typeracer'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String)
    score = db.relationship("Score", backref="user", lazy=True)

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    words_per_minute = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    excerpt_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Excerpt(db.Model):
    __tablename__ = "excerpts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

db.create_all()

@app.route('/')
def root():
    return jsonify(['Hello', 'World'])

@app.route('/scores', methods=["GET", "POST"])
def create_score():
    if request.method == 'POST':
        data = request.get_json()
      
        scores = Score(user_id=1, time=data["time"], words_per_minute=data["wpm"], errors=data["errorCount"], excerpt_id=1)
        db.session.add(scores)
        db.session.commit()
        response = {"userID":scores.user_id,
                    "time": scores.time,
                    "words_per_minute": scores.words_per_minute,
                    "errors": scores.errors
                    }
        print(response)
    else:
        scores = Score.query.all()
        response = {"data":[{"user_id": i.user_id,
                            "time":i.time,
                            "words_per_minute":i.words_per_minute,
                            "errors":i.errors,
                            "excerpt_id":i.excerpt_id
                             } for i in scores]}
    return jsonify(response)

if __name__ == "__main__":
  app.run(debug=True, ssl_context='adhoc')