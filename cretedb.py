import sqlite3
import os
import json
import requests

path = os.getcwd()
path_to_db = os.path.join(path, 'db', 'qcpc.db')

# Eliminar la base de datos si existe
if os.path.exists(path_to_db):
    os.remove(path_to_db)

# Conectar a la base de datos (creará el archivo nuevamente)
conn = sqlite3.connect(path_to_db)

# Crear un cursor
c = conn.cursor()

# Eliminar la tabla de juegos si existe
c.execute('''DROP TABLE IF EXISTS juegos''')

# Eliminar la tabla de desarrolladores si existe
c.execute('''DROP TABLE IF EXISTS developers''')

# Crear la tabla de juegos
c.execute('''CREATE TABLE juegos (
             id INTEGER PRIMARY KEY,
             game_title TEXT,
             release_date DATE,
             platform INTEGER,
             region_id INTEGER,
             country_id INTEGER,
             developer_id INTEGER,             
             front_boxart_path TEXT,
             back_boxart_path TEXT,
             screenshot_path TEXT,
             url VARCHAR(255),
             FOREIGN KEY(developer_id) REFERENCES developers(id)
             )''')

# Crear la tabla de desarrolladores
c.execute('''CREATE TABLE developers (
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
