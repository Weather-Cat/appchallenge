from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    #lasttime = db.Column(db.)
    #last_t_max = db.Column(db.Integer, nullable = True)
    #last_t_min = db.Column(db.Integer, nullable = True)
    #last_forecast
    #locations = db.relationship()

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')

    def serialize(self):
        return {'id': self.id, 'username': self.username}

#stores what the cat will wear for a given range of temperatures
class CatWear(db.Model):
    __tablename__ = 'catwear'
    id = db.Column(db.Integer, primary_key = True)
    imagename = db.Column(db.String, nullable = False)
    t_max = db.Column(db.Integer, nullable = True)
    t_min = db.Column(db.Integer, nullable = True)

    def __init__(self, **kwargs):
        self.imagename = kwargs.get('imagename')
        self.t_max = kwargs.get('t_max')
        self.t_min = kwargs.get('t_min')

    def serialize(self):
        return {
            'id': self.id,
            'image_name': self.imagename
        }


# class Forecast(db.Model):
#     __tablename__ = 'forecast'
#     id = db.Column(db.Integer, primary_key = True)
#     time = db.Column(db.Float, nullable = False)
#     max_t0 = db.Column(db.Integer, nullable = False)
#     min_t0 = db.Column(db.Integer, nullable = False)
#     max_t1 = db.Column(db.Integer, nullable = False)
#     min_t1 = db.Column(db.Integer, nullable = False)
#     max_t2 = db.Column(db.Integer, nullable = False)
#     min_t2 = db.Column(db.Integer, nullable = False)
#     max_t3 = db.Column(db.Integer, nullable = False)
#     min_t3 = db.Column(db.Integer, nullable = False)
#
#     def __init__(self, **kwargs):
#         self.time = datetime.now(timezone.utc)
