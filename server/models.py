from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String,nullable=False)
    