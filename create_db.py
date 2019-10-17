import psycopg2

def main()
    connect_db = psycopg2.connect(dbname=config.NAME_DB, user=config.USER_DB, 
                        password=config.PASSWORD_DB, host=config.HOSTNAME_DB)

    cursor = connect_db.cursor()
    cursor.execute('''CREATE TABLE  if not exists trace  
            (callsign TEXT NOT NULL,
            longitude FLOAT NOT NULL,
            latitude FLOAT NOT NULL,
            on_ground  BOOL NOT NULL,
            datetime timestamp);''')

    connect_db.commit()
    connect_db.close()

main()