from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#stores what the cat will wear for a given range of temperatures
class CatWear(db.Model):
    __tablename__ = 'catwear'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    image = db.Column(db.String, nullable = False)
    t_max = db.Column(db.Integer, nullable = True)
    t_min = db.Column(db.Integer, nullable = True)

#    def __init__(self, **kwargs):
#        self.code = kwargs.get('code')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image
        }

#stores what background elements will be present for a given weather condition
class Background(db.Model):
    __tablename__ = 'background'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    image = db.Column(db.String, nullable = False)
    wx_condition = db.Column(db.String, nullable = False)

#    def __init__(self, **kwargs):
#        self.code = kwargs.get('code')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image
        }

#stores a CONUS sector, at which URL to find data for that sector, and the *.flt
#file(s) associated with the sector
#Note 1.0: CONUS sectors are a static geographic partion, the data is downloaded
#for a specific sector
#Note 2.0: *.flt files store the condensed weather forecast data efficiently. They
#are a file type used by the degrib program that will be integrated later
class Sector(db.Model):
    __tablename__ = 'sector'
    id = db.Column(db.Integer, primary_key = True)
    sectorname = db.Column(db.String, nullable = False)
    grib_route = db.Column(db.String, nullable = False)
    flt_file = db.relationship('ForecastData', cascade = 'delete')

#stores the different factors needed for a complete forecast and stores the URL
#extension for that type of data
class ForecastType(db.Model):
    __tablename__ = 'forecasttypes'
    id = db.Column(db.Integer, primary_key = True)
    datatype = db.Column(db.String, nullable = False)
    grib_route = db.Column(db.String, nullable = False)

#stores the most recent *.flt and the index file for each sector, this part is
#going to change a bit. This table will be updated automatically as new forecasts
#are released, probably with the a bash script and the cron module
class ForecastData(db.Model):
    __tablename__ = 'forecastwx'
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False)
    index_file = db.Column(db.String, nullable = False)
    sectorid = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable = False)
    sector = db.relationship('Sector')
    #flt files?

    def __init__(self, **kwargs):
        self.fltdb = kwargs.get('fltdb')
        self.sector = kwargs.get('sector')
