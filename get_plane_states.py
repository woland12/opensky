from opensky_api import OpenSkyApi
import config

# Функция получает лист со словарями, в каждом словаре есть атрибуты
# смотри https://opensky-network.org/apidoc/python.html      
def get_states():

    api = OpenSkyApi(config.LOGIN_OPENSKY_API,config.PASSWORD_OPENSKY_API)
    plane_states = api.get_states()
    list_states = plane_states.states
    return list_states
