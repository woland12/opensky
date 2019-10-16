import config
from datetime import datetime
import psycopg2

connect_db = psycopg2.connect(dbname=config.NAME_DB, user=config.USER_DB, 
                        password=config.PASSWORD_DB, host=config.HOSTNAME_DB)

class Trace():
    cursor = connect_db.cursor()
    cursor.execute('''CREATE TABLE  if not exists trace  
            (callsign TEXT NOT NULL,
            longitude FLOAT NOT NULL,
            latitude FLOAT NOT NULL,
            on_ground  BOOL NOT NULL,
            datetime timestamp);''')

    connect_db.commit()

    def add_to_trace(list_states):
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