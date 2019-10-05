from opensky_api import OpenSkyApi
import config

def get_states():

    #Функция получает лист со словарями, в каждом словаре есть следующие атрибуты
    #icao24 - ICAO24 address of the transmitter in hex string representation.
    # callsign - callsign of the vehicle. Can be None if no callsign has been received.
    # origin_country - inferred through the ICAO24 address
    # time_position - seconds since epoch of last position report. Can be None if there was no position report received by OpenSky within 15s before.
    # last_contact - seconds since epoch of last received message from this transponder
    # longitude - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
    # latitude - in ellipsoidal coordinates (WGS-84) and degrees. Can be None
    # geo_altitude - geometric altitude in meters. Can be None
    # on_ground - true if aircraft is on ground (sends ADS-B surface position reports).
    # velocity - over ground in m/s. Can be None if information not present
    # heading - in decimal degrees (0 is north). Can be None if information not present.
    # vertical_rate - in m/s, incline is positive, decline negative. Can be None if information not present.
    # sensors - serial numbers of sensors which received messages from the vehicle within the validity period of this state vector. Can be None if no filtering for sensor has been requested.
    # baro_altitude - barometric altitude in meters. Can be None
    # squawk - transponder code aka Squawk. Can be None
    # spi - special purpose indicator
    # position_source - origin of this state’s position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM

    api = OpenSkyApi(config.LOGIN_OPENSKY_API,config.PASSWORD_OPENSKY_API)
    states = api.get_states()
    list_states = states.states
    return list_states

if __name__ == "__main__":
    list_states = get_states()
    for state_vector in list_states:
        print(f'latitude is {state_vector.latitude},longitude is {state_vector.longitude}')