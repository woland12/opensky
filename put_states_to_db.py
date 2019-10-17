from datetime import date
from get_plane_states import get_states
from webapp.model import Trace
   
def main():
    list_states = get_states()
    #list_states = [{'callsign':'SD123','longitude':12.1580,'latitude':-52.3254,'on_ground':False}]
    Trace.add_to_trace(list_states)            

main()