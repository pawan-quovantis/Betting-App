from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from bcrypt import hashpw, gensalt
from server import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), unique=False)
    join_date = db.Column(db.DateTime)

    def my_dict(self):
        return {"id": self.id, "first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "join_date": self.join_date}


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    home_ground = db.Column(db.String(25))

    def my_dict(self):
        return {"id": self.id, "team_name": self.team_name, "home_ground": self.home_ground}


class Fixtures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer, db.ForeignKey(Teams.id))
    away_team_id = db.Column(db.Integer, db.ForeignKey(Teams.id))
    result = db.Column(db.Integer)
    home_team = db.relationship(Teams, foreign_keys=[home_team_id])
    away_team = db.relationship(Teams, foreign_keys=[away_team_id])

    def my_dict(self):
        return {"id": self.id, "match_date": self.match_date, "home_team_id": self.home_team_id,
                "away_team_id": self.away_team_id, "result": self.result}


class Bets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    fixture_id = db.Column(db.Integer, db.ForeignKey(Fixtures.id))
    team_id = db.Column(db.Integer, db.ForeignKey(Teams.id))
    amount = db.Column(db.Integer)
    user = db.relationship(Users, backref=db.backref('bets', uselist=True, cascade='delete,all'))
    fixture = db.relationship(Fixtures, backref=db.backref('bets', uselist=True, cascade='delete,all'))
    team = db.relationship(Teams, backref=db.backref('bets', uselist=True, cascade='delete,all'))

    def my_dict(self):
        return {"id": self.id, "user_id": self.user_id, "fixture_id": self.fixture_id,
                "team_id": self.team_id, "amount": self.amount}

    def __repr__(self):
        return str()


class UserBettingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    fixture_id = db.Column(db.Integer, db.ForeignKey(Fixtures.id))
    user = db.relationship(Users, backref=db.backref('user_betting_history', uselist=True, cascade='delete,all'))
    fixture = db.relationship(Fixtures, backref=db.backref('user_betting_history', uselist=True, cascade='delete,all'))

    def my_dict(self):
        return {"id": self.id, "user_id": self.user_id, "fixture_id": self.fixture_id, "score": self.score}


