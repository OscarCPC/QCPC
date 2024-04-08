import requests

# Función para buscar juegos por nombre utilizando la API de TheGamesDB
def buscar_juegos(nombre_juego, api_key, plataforma='Amstrad'):
    # URL base de la API de TheGamesDB
    url_base = "https://api.thegamesdb.net/v1/Games/ByGameName"

    # Parámetros de la solicitud
    params = {
        'apikey': api_key,
        'name': nombre_juego,
        'fields': plataforma
    }

    # Realizar la solicitud GET a la API
    respuesta = requests.get(url_base, params=params)

    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        # Decodificar la respuesta JSON
        datos = respuesta.json()

        # Verificar si se encontraron juegos
        if 'data' in datos and 'games' in datos['data'] and datos['data']['games']:
            juegos = datos['data']['games']

            # Mostrar información de cada juego
            for juego in juegos:
                print("**Título:**", juego['game_title'])
                print("**Plataforma:**", plataforma)
                print("**Fecha de lanzamiento:**", juego['release_date'])
                print("---------------------")
        else:
            print("No se encontraron juegos que coincidan con el nombre '{}' para la plataforma '{}'.".format(nombre_juego, plataforma))
    else:
        print("Error al realizar la solicitud a la API de TheGamesDB. Código de estado:", respuesta.status_code)


# Definir la API key
api_key = "8b398662ea67cda0114a51d5b343cc52d085ce00565eec054b8c3c167e818724"

# Búsqueda de un juego
nombre_juego = "Renegade"
buscar_juegos(nombre_juego, api_key)
