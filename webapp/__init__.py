from flask import Flask, render_template, request
from get_plane_states import get_states
from webapp.model import Trace
   
def create_app():
    app = Flask(__name__)
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

        return render_template('index.html',
                                page_title = title,
                                list_states = list_states,
                                number_of_page = number_of_page,
                                list_of_entries=list_of_entries,
                                len_list_of_entries=len_list_of_entries)
    return app
