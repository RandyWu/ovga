# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class Course(db.Model, UserMixin):
    __tablename__ = 'Course'

    CourseID = db.Column(db.Integer, primary_key=True)
    VenueID = db.Column(db.ForeignKey('Venues.VenueId'), nullable=False, index=True)
    Num_Holes = db.Column(db.Integer)
    CourseName = db.Column(db.String(256))

class Division(db.Model, UserMixin):
    __tablename__ = 'Division'

    DivisionID = db.Column(db.Integer, primary_key=True)
    Division = db.Column(db.String(256), nullable=False)
    EventID = db.Column(db.ForeignKey('Events.EventId'))

    Players = db.relationship('Player', secondary='PlayersDivision', backref='divisions')

class Event(db.Model, UserMixin):
    __tablename__ = 'Events'

    EventId = db.Column(db.Integer, primary_key=True)
    Venue_Id = db.Column(db.ForeignKey('Venues.VenueId'), nullable=False, index=True)
    Name = db.Column(db.String(256))
    Address = db.Column(db.String(256))
    Date = db.Column(db.Date)
    CourseID = db.Column(db.ForeignKey('Course.CourseID'), nullable=False, index=True)

    Venue = db.relationship('Venue', primaryjoin='Event.Venue_Id == Venue.VenueId', backref='events')

class Hole(db.Model, UserMixin):
    __tablename__= 'Hole'

    HoleID = db.Column(db.Integer, primary_key=True, nullable=False)
    CourseID = db.Column(db.ForeignKey('Course.CourseID'), nullable=False, index=True)
    Hole_Num = db.Column(db.Integer, nullable=False)
    Par = db.Column(db.Integer, nullable=False)

class Intersectional(db.Model, UserMixin):
    __tablename__ = 'Intersectionals'

    IntersectionalId = db.Column(db.Integer, primary_key=True)
    Event_Id = db.Column(db.ForeignKey('Events.EventId'), nullable=False, index=True)
    GroupName = db.Column(db.String(256), nullable=False)
    ScheduleDate = db.Column(db.DateTime)

    Event = db.relationship('Event', primaryjoin='Intersectional.Event_Id == Event.EventId', backref='intersectionals')

class Match(db.Model, UserMixin):
    __tablename__ = 'Match'

    MatchID = db.Column(db.Integer, primary_key=True, nullable=False)
    VenueID = db.Column(db.ForeignKey('Venues.VenueId'), nullable=False, index=True)
    CourseID = db.Column(db.ForeignKey('Course.CourseID'), nullable=False, index=True)

class PlayerDivision(db.Model, UserMixin):
    __tablename__ = 'PlayersDivision'

    Player_Id = db.Column(db.ForeignKey('Players.PlayerId'), nullable=False, index=True)
    Division_Id = db.Column(db.ForeignKey('Division.DivisionID'), nullable=False, index=True)
    Event_Id = db.Column(db.ForeignKey('Events.EventId'), index=True)    
    ID = db.Column(db.Integer, primary_key=True, nullable=False)

t_PlayersTeams = db.Table(
    'PlayersTeams',
    db.Column('Player_Id', db.ForeignKey('Players.PlayerId'), nullable=False, index=True),
    db.Column('Team_Id', db.ForeignKey('Teams.TeamId'), nullable=False, index=True)
)

class Score(db.Model, UserMixin):
    __tablename__ = 'Scores'

    ScoreId = db.Column(db.Integer, primary_key=True)
    PlayerID = db.Column(db.ForeignKey('Players.PlayerId'), nullable=False, index=True)
    EventID = db.Column(db.ForeignKey('Events.EventId'), nullable=False, index=True)
    CourseID = db.Column(db.ForeignKey('Course.CourseID'), nullable=False, index=True)
    HoleID = db.Column(db.ForeignKey('Hole.HoleID'), nullable=False)
    MatchID = db.Column(db.ForeignKey('Match.MatchID'), nullable=False)
    Strokes = db.Column(db.Integer, nullable=False)
    TeamScore = db.Column(db.Integer)

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

