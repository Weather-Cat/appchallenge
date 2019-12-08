from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
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
    ft_max = db.Column(db.Integer, nullable = True)
    ft_min = db.Column(db.Integer, nullable = True)
    ct_max = db.Column(db.Integer, nullable = True)
    ct_min = db.Column(db.Integer, nullable = True)

    def __init__(self, **kwargs):
        self.imagename = kwargs.get('imagename')
        self.ft_max = kwargs.get('ft_max')
        self.ft_min = kwargs.get('ft_min')
        self.ct_max = kwargs.get('ct_max')
        self.ct_min = kwargs.get('ct_min')

    def serialize(self):
        return {
            'id': self.id,
            'image_name': self.imagename
        }
