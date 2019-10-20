from datetime import datetime
from flask import Flask, render_template, request
from get_plane_states import get_states
from webapp.model import Trace,db
   
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    @app.route("/")
    def index():
        list_states = get_states()
        return my_render_template(list_states=list_states)

    @app.route('/my-route')
    def my_route():
        page = request.args.get('page', default = 1, type = int)
        list_states = get_states()
        num_of_lines_page = 20
        number_of_page = min(page,len(list_states)//num_of_lines_page)
        return my_render_template(number_of_page = number_of_page,list_states=list_states)

    def my_render_template(list_states,number_of_page = 1,num_of_lines_page = 20):
        title = 'Состояния самолетов мира'
        num_start = (number_of_page-1)*num_of_lines_page
        num_finish = number_of_page*num_of_lines_page-1
        list_of_entries = range(num_start,num_finish)
        len_list_of_entries = len(list_states)//num_of_lines_page
        
        # Добавляем записи в базу данных
        add_states_to_db(list_states)

        return render_template('index.html',
                                page_title = title,
                                list_states = list_states,
                                number_of_page = number_of_page,
                                list_of_entries=list_of_entries,
                                len_list_of_entries=len_list_of_entries)
    
    def add_states_to_db(list_states):
        for state_vector in list_states:
            if (state_vector.on_ground==True
                and state_vector.callsign is not None
                and not state_vector.callsign.strip() == ''):
                # Здесь будем искать записи в БД по этому самолету более ранние и удалять их.
                # Означает, что самолет на земле и в его траектории нет больше смысла
                old_traces=Trace.query.filter_by(callsign=state_vector.callsign).filter(Trace.datetime < datetime.now()).all()
                for old_trace in old_traces:
                    db.session.delete(old_trace)
            elif (state_vector.on_ground == False
                and state_vector.callsign is not None
                and not state_vector.callsign.strip() == ''
                and state_vector.longitude is not None
                and state_vector.latitude is not None):
                new_trace = Trace(callsign=state_vector.callsign,
                                    longitude=state_vector.longitude,
                                    latitude=state_vector.latitude,
                                    on_ground=state_vector.on_ground,
                                    datetime = datetime.now()
                                    )
                db.session.add(new_trace)
        db.session.commit()
    return app
