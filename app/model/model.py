# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()



class Division(db.Model, UserMixin):
    __tablename__ = 'Division'

    DivisionId = db.Column(db.Integer, primary_key=True)
    Division = db.Column(db.String(256), nullable=False)

    Players = db.relationship('Player', secondary='PlayersDivision', backref='divisions')



class Event(db.Model, UserMixin):
    __tablename__ = 'Events'

    EventId = db.Column(db.Integer, primary_key=True)
    Venue_Id = db.Column(db.ForeignKey('Venues.VenueId'), nullable=False, index=True)

    Venue = db.relationship('Venue', primaryjoin='Event.Venue_Id == Venue.VenueId', backref='events')



class Intersectional(db.Model, UserMixin):
    __tablename__ = 'Intersectionals'

    IntersectionalId = db.Column(db.Integer, primary_key=True)
    Event_Id = db.Column(db.ForeignKey('Events.EventId'), nullable=False, index=True)
    GroupName = db.Column(db.String(256), nullable=False)
    ScheduleDate = db.Column(db.DateTime)

    Event = db.relationship('Event', primaryjoin='Intersectional.Event_Id == Event.EventId', backref='intersectionals')



t_PlayersDivision = db.Table(
    'PlayersDivision',
    db.Column('Player_Id', db.ForeignKey('Players.PlayerId'), nullable=False, index=True),
    db.Column('Division_Id', db.ForeignKey('Division.DivisionId'), nullable=False, index=True)
)



t_PlayersTeams = db.Table(
    'PlayersTeams',
    db.Column('Player_Id', db.ForeignKey('Players.PlayerId'), nullable=False, index=True),
    db.Column('Team_Id', db.ForeignKey('Teams.TeamId'), nullable=False, index=True)
)



class Score(db.Model, UserMixin):
    __tablename__ = 'Scores'

    ScoreId = db.Column(db.Integer, primary_key=True)
    Player_Id = db.Column(db.ForeignKey('Players.PlayerId'), nullable=False, index=True)
    Event_Id = db.Column(db.ForeignKey('Events.EventId'), nullable=False, index=True)
    Hole1 = db.Column(db.Integer)
    Hole2 = db.Column(db.Integer)
    Hole3 = db.Column(db.Integer)
    Hole4 = db.Column(db.Integer)
    Hole5 = db.Column(db.Integer)
    Hole6 = db.Column(db.Integer)
    Hole7 = db.Column(db.Integer)
    Hole8 = db.Column(db.Integer)
    Hole9 = db.Column(db.Integer)
    Hole10 = db.Column(db.Integer)
    Hole11 = db.Column(db.Integer)
    Hole12 = db.Column(db.Integer)
    Hole13 = db.Column(db.Integer)
    Hole14 = db.Column(db.Integer)
    Hole15 = db.Column(db.Integer)
    Hole16 = db.Column(db.Integer)
    Hole17 = db.Column(db.Integer)
    Hole18 = db.Column(db.Integer)
    TeamScore = db.Column(db.Integer)

    Event = db.relationship('Event', primaryjoin='Score.Event_Id == Event.EventId', backref='scores')
    Player = db.relationship('Player', primaryjoin='Score.Player_Id == Player.PlayerId', backref='scores')



class Team(db.Model, UserMixin):
    __tablename__ = 'Teams'

    TeamId = db.Column(db.Integer, primary_key=True)
    Event_Id = db.Column(db.ForeignKey('Events.EventId'), nullable=False, index=True)
    Name = db.Column(db.String(256), nullable=False)
    CaptainId = db.Column(db.Integer, nullable=False)

    Event = db.relationship('Event', primaryjoin='Team.Event_Id == Event.EventId', backref='teams')



class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    UserId = db.Column(db.Integer, primary_key=True)
    Role = db.Column(db.String(30), nullable=False)


class Admin(User):
    __tablename__ = 'Admins'

    Admin_Id = db.Column(db.ForeignKey('Users.UserId'), primary_key=True)
    Password = db.Column(db.String(256), nullable=False)
    Email = db.Column(db.String(256), nullable=False)


class Player(User):
    __tablename__ = 'Players'

    PlayerId = db.Column(db.ForeignKey('Users.UserId'), primary_key=True)
    Name = db.Column(db.String(256), nullable=False)
    Password = db.Column(db.String(256), nullable=False)
    Gender = db.Column(db.String(32))
    Email = db.Column(db.String(128), nullable=False, unique=True)

    Teams = db.relationship('Team', secondary='PlayersTeams', backref='players')

    #   Override get_id()
    def get_id(self):
        return (self.PlayerId)

class Venue(db.Model, UserMixin):
    __tablename__ = 'Venues'

    VenueId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(256), nullable=False)
    Address = db.Column(db.String(256))
