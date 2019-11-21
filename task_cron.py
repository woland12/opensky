#!/home/woland/opensky/env/bin/python3

from fill_up_db import add_states_to_db
from get_plane_states import get_states


def main():
    list_states = get_states()
    add_states_to_db(list_states)

if __name__=='__main__':
   main()
