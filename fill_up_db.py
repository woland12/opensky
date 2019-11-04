from sqlalchemy import create_engine
from get_plane_states import get_states
from time import sleep
from datetime import datetime,timedelta
from webapp import config

def main():

    while True:
        try:
            list_states = get_states()
            add_states_to_db(list_states)
            sleep(900)
        except KeyboardInterrupt:
            break

def add_states_to_db(list_states):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI_LOCAL)
    connection = engine.connect()
    
    now = datetime.now()

    # Очистим старые записи, возраст которых более 1 дня
    delta = timedelta(days=1)
    yesterday = now - delta
    connection.execute("DELETE from trace where datetime<%(yesterday)s;",{'yesterday':yesterday})

    trans = connection.begin()
    for state_vector in list_states:
        if (state_vector.on_ground==True
            and state_vector.callsign is not None
            and not state_vector.callsign.strip() == ''):
            # Здесь будем искать записи в БД по этому самолету более ранние и удалять их.
            # Означает, что самолет на земле и в его траектории нет больше смысла
            connection.execute("DELETE from trace where callsign=%(callsign)s and datetime<%(now)s;",{'callsign':state_vector.callsign,'now':now})
        elif (state_vector.on_ground == False
            and state_vector.callsign is not None
            and not state_vector.callsign.strip() == ''
            and state_vector.longitude is not None
            and state_vector.latitude is not None):
            connection.execute("INSERT INTO trace (callsign,longitude,latitude,on_ground,datetime) VALUES((%s),(%s),(%s),(%s),(%s))",
                                    (state_vector.callsign,state_vector.longitude,state_vector.latitude,state_vector.on_ground,now,))
    trans.commit()
    connection.close()

main()