from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PAGES.db'

db = SQLAlchemy(app)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))


class Hablo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


db.create_all()

for i in range(1, 201):
    thread = Thread(title="Thread " + str(i))
    db.session.add(thread)
db.session.commit()
hablo = Thread.query.count()
print (hablo)

"""if __name__ == '__main__':
    app.run(debug=True)
"""
