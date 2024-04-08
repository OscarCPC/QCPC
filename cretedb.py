import sqlite3
import os
import json
import requests

path = os.getcwd()
path_to_db = os.path.join(path, 'db', 'qcpc.db')

# Conectar a la base de datos (creará el archivo si no existe)
conn = sqlite3.connect(path_to_db)

# Crear un cursor
c = conn.cursor()

# Crear la tabla de juegos si no existe
c.execute('''CREATE TABLE IF NOT EXISTS juegos (
             id INTEGER PRIMARY KEY,
             game_title TEXT,
             release_date DATE,
             platform INTEGER,
             region_id INTEGER,
             country_id INTEGER,
             developer_id INTEGER,
             image_path TEXT,
             FOREIGN KEY(developer_id) REFERENCES developers(id)
             )''')

# Crear la tabla de desarrolladores si no existe
c.execute('''CREATE TABLE IF NOT EXISTS developers (
             id INTEGER PRIMARY KEY,
             name TEXT
             )''')

# Guardar los cambios
conn.commit()

# Descargar el JSON de desarrolladores desde la URL
url = "https://api.thegamesdb.net/v1/Developers?apikey=apikey"
response = requests.get(url)

if response.status_code == 200:
    developers_data = response.json()["data"]["developers"]
    
    # Insertar los desarrolladores en la tabla de desarrolladores
    for dev_id, dev_info in developers_data.items():
        c.execute('INSERT INTO developers (id, name) VALUES (?, ?)', (dev_info['id'], dev_info['name']))

    # Guardar los cambios
    conn.commit()
    print("Los datos de desarrolladores se han insertado correctamente en la base de datos.")
else:
    print("Error al obtener los datos de desarrolladores:", response.status_code)

# Cerrar la conexión
conn.close()
