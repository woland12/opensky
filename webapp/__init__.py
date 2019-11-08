
from datetime import datetime
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps,Map
from get_plane_states import get_states

from sqlalchemy import create_engine
import config
from webapp.model import db
def create_app():
    app = Flask(__name__)
    app.config['GOOGLEMAPS_KEY'] = config.GOOGLEMAPS_KEY
    db.init_app(app)

    GoogleMaps(app)

    @app.route("/")
    def index():
             
        engine = create_engine(config.SQLALCHEMY_DATABASE_URI_LOCAL)
        connection = engine.connect()
        
        mymap = Map(
        identifier="view-side",
        lat=27.4419,
        lng=-112.1419,
        )

        markers =[]
        rows = connection.execute("SELECT latitude,longitude,callsign,datetime \
            FROM (SELECT   t.*, MAX(datetime) OVER (partition BY callsign) maxdatetime \
            FROM PUBLIC.trace AS t) AS tt \
            WHERE tt.datetime=tt.maxdatetime \
            ORDER BY callsign").fetchall()

        for row in rows:
            markers.append({
            'icon': 'http://maps.google.com/mapfiles/ms/icons/plane.png',
            'lat': row[0],
            'lng': row[1],
            'infobox': f"<b>{row[2]}</b>"
            })

        
        sndmap = Map(
            identifier="sndmap",
            lat=55.9000,
            lng=37.7800,
            markers=markers ,zoom = 3,
            style="height:720px;width:1100px;margin:0;"
            )

        return render_template('index.html',mymap=mymap,sndmap=sndmap)

    return app
