from flask import Flask, render_template
from get_plane_states import get_states

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def index():
        title = 'Состояния самолетов мира'
        list_states = get_states()
        return render_template('index.html',page_title = title,list_states = list_states)

    return app