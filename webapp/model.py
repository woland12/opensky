from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trace(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    callsign = db.Column(db.Text,nullable=False)
    longitude = db.Column(db.Float,nullable=False)
    latitude = db.Column(db.Float,nullable=False)
    on_ground = db.Column(db.Boolean,nullable=False)
    datetime = db.Column(db.DateTime,nullable=True)


    def __repr__(self):
            return '<Trace {} {}>'.format(self.callsign, self.on_ground)