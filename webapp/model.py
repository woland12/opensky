import config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()

class Trace():
    callsign = db.Column(db.Text,nullable=False)
    longitude = db.Column(db.Float,nullable=False)
    latitude = db.Column(db.Float,unique=True,nullable=False)
    on_ground = db.Column(db.Boolean,nullable=False)
    datetime = db.Column(db.DateTime,nullable=True)

    def add_to_trace(list_states):
        connect_db = psycopg2.connect(dbname=config.NAME_DB, user=config.USER_DB, 
                            password=config.PASSWORD_DB, host=config.HOSTNAME_DB)
        cursor = connect_db.cursor()
        now = datetime.now()
        for state_vector in list_states:
            if (state_vector.on_ground==True
                and state_vector.callsign is not None
                and not state_vector.callsign.strip() == ''):
                # Здесь будем искать записи в БД по этому самолету более ранние и удалять их.
                # Означает, что самолет на земле и в его траектории нет больше смысла
                cursor.execute("DELETE from trace where callsign=%(callsign)s and datetime<%(now)s;",{'callsign':state_vector.callsign,'now':now})
                
            elif (state_vector.on_ground == False
                and state_vector.callsign is not None
                and not state_vector.callsign.strip() == ''
                and state_vector.longitude is not None
                and state_vector.latitude is not None):

                cursor.execute("INSERT INTO trace (callsign,longitude,latitude,on_ground,datetime) VALUES((%s),(%s),(%s),(%s),(%s))",
                                    (state_vector.callsign,state_vector.longitude,state_vector.latitude,state_vector.on_ground,now,))

        connect_db.commit()
        connect_db.close()

    def __repr__(self):
            return '<Trace {} {}>'.format(self.title, self.url)