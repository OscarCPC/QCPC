from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import requests
import sqlite3
from .common import *



class qcpc_search(QWidget):
    path = os.getcwd()
    
    
    #BDD
    path_to_db = os.path.join(path,'db','qcpc.db')
    
    #Descargas    
    path_to_download = os.path.join(path,'files', 'downloads')    
    boxart_path = os.path.join(path_to_download, 'boxart')        
    screenshot_path = os.path.join(path_to_download, 'screenshot')
        
    #Guardar descargas
    path_to_image = os.path.join(path,'files', 'images')
    boxart_path_images = os.path.join(path_to_image, 'boxart')    
    screenshot_path_images = os.path.join(path_to_image, 'screenshot')    
    

    
    

    def setupUi(self):

        self.resize(1100, 950)
        
        self.setMinimumSize(QSize(1100, 950))
        self.formLayout_2 = QFormLayout(self)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.qcpc_frame_container = QFrame(self)
        self.qcpc_frame_container.setObjectName(u"qcpc_frame_container")
        
        
        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.qcpc_input_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_input_frame.setObjectName(u"qcpc_input_frame")
        
        
        self.qcpc_input_frame.setLayoutDirection(Qt.RightToLeft)
        self.qcpc_input_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_input_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_input_layout = QFormLayout(self.qcpc_input_frame)
        self.qcpc_input_layout.setObjectName(u"qcpc_input_layout")
        self.qcpc_input_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.qcpc_input_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.qcpc_input_layout.setLabelAlignment(Qt.AlignCenter)
        self.qcpc_input_label = QLabel(self.qcpc_input_frame)
        self.qcpc_input_label.setObjectName(u"qcpc_input_label")
        
        self.qcpc_input_label.setMinimumSize(QSize(250, 0))
        self.qcpc_input_label.setMaximumSize(QSize(16777215, 16777211))
        self.qcpc_input_label.setAlignment(Qt.AlignCenter)

        self.qcpc_input_layout.setWidget(0, QFormLayout.FieldRole, self.qcpc_input_label)

        self.qcpc_input_text = QPlainTextEdit(self.qcpc_input_frame)
        self.qcpc_input_text.setObjectName(u"qcpc_input_text")
        self.qcpc_input_text.setMinimumSize(QSize(275, 30))
        self.qcpc_input_text.setMaximumSize(QSize(16777215, 30))
        self.qcpc_input_text.installEventFilter(self)

        self.qcpc_input_layout.setWidget(1, QFormLayout.FieldRole, self.qcpc_input_text)

        self.qcpc_input_output_text = QTextEdit(self.qcpc_input_frame)
        self.qcpc_input_output_text.setObjectName(u"qcpc_input_output_text")
        self.qcpc_input_output_text.setReadOnly(True)
        

        self.qcpc_input_layout.setWidget(5, QFormLayout.FieldRole, self.qcpc_input_output_text)

        self.qcpc_inner_input_layout = QHBoxLayout()
        self.qcpc_inner_input_layout.setObjectName(u"qcpc_inner_input_layout")
        self.qcpc_input_frame_save = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_save.setObjectName(u"qcpc_input_frame_save")
        self.qcpc_input_frame_save.setMinimumSize(QSize(275, 0))
        self.qcpc_input_frame_save.setLayoutDirection(Qt.RightToLeft)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_save)

        self.qcpc_input_frame_delete = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_delete.setObjectName(u"qcpc_input_frame_delete")

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_delete)

        self.qcpc_input_search = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_search.setObjectName(u"qcpc_input_search")
        self.qcpc_input_search.setMinimumSize(QSize(80, 30))
        self.qcpc_input_search.setMaximumSize(QSize(80, 30))
        self.qcpc_input_search.setLayoutDirection(Qt.LeftToRight)
        # Establecer el botón como el botón predeterminado para que se active con Enter
        self.qcpc_input_search.setDefault(True)
        # Establecer el acceso directo a Enter
        self.qcpc_input_search.setShortcut(Qt.Key_Return)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_search)


        self.qcpc_input_layout.setLayout(4, QFormLayout.SpanningRole, self.qcpc_inner_input_layout)



        self.qcpc_result_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_result_frame.setObjectName(u"qcpc_result_frame")
        
        
        self.qcpc_result_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_result_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.qcpc_result_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.qcpc_result_table = QListWidget(self.qcpc_result_frame)
        self.qcpc_result_table.setObjectName(u"qcpc_result_table")

        self.verticalLayout.addWidget(self.qcpc_result_table)

        self.qcpc_result_label = QLabel(self.qcpc_result_frame)
        self.qcpc_result_label.setObjectName(u"qcpc_result_label")
        self.qcpc_result_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.qcpc_result_label)


        self.gridLayout_2.addWidget(self.qcpc_result_frame, 1, 0, 1, 1)


        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.qcpc_frame_container)

        self.qcpc_image_frame = QFrame(self)
        self.qcpc_image_frame.setObjectName(u"qcpc_image_frame")
        
        
        self.qcpc_image_frame.setMinimumSize(QSize(600, 900))
        self.qcpc_image_frame.setMaximumSize(QSize(16777215, 16777215))
        
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.qcpc_image_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName(u"qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(QSize(600, 900))
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)
                
        #self.qcpc_image_frame.setStyleSheet(u"background-color: rgba(170, 0, 0,0);")
        
        #self.gridLayout_2.addWidget(self.qcpc_input_frame, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.qcpc_input_frame, 0, 0, 1, 1)  # Colocar en la primera columna y primera fila
        self.gridLayout_2.addWidget(self.qcpc_image_frame, 0, 1, 2, 1)  # Colocar en la segunda columna y primera fila, ocupando 2 filas de altura
        self.gridLayout_2.addWidget(self.qcpc_result_frame, 1, 0, 1, 1)  # Colocar en la primera columna y segunda fila
        
            
        #self.horizontalLayout.addWidget(self.qcpc_image_label)
        self.retranslateUi(self)
        self.test_path()
        self.setup_connections()

        QMetaObject.connectSlotsByName(self)
    # setupUi   

    def retranslateUi(self, qcpc_search):
        qcpc_search.setWindowTitle(QCoreApplication.translate("qcpc_search", u"Form", None))
        self.qcpc_result_label.setText(QCoreApplication.translate("qcpc_search", u"Resultados", None))        
        self.qcpc_input_label.setText(QCoreApplication.translate("qcpc_search", u"Titulo a buscar", None))
        self.qcpc_input_frame_save.setText(QCoreApplication.translate("qcpc_search", u"Guardar Selecci\u00f3n", None))
        self.qcpc_input_frame_delete.setText(QCoreApplication.translate("qcpc_search", u"Borrar", None))
        self.qcpc_input_search.setText(QCoreApplication.translate("qcpc_search", u"Buscar", None))
    # retranslateUi
    
    def setup_connections(self):
        self.qcpc_input_search.clicked.connect(self.get_game)        
        self.qcpc_result_table.itemClicked.connect(self.show_game_image)
        self.qcpc_input_frame_delete.clicked.connect(lambda: self.qcpc_input_text.clear())
        self.qcpc_input_frame_save.clicked.connect(self.guardar_seleccion)
        
    def eventFilter(self, source, event):
        if source is self.qcpc_input_text and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.qcpc_input_search.click()  # Simular clic en el botón
            elif event.key() == Qt.Key_Escape:  # Si se presiona Escape, limpiar el texto
                self.qcpc_input_text.clear()
        else:
            # Llamar a la implementación original del evento para mantener el comportamiento predeterminado
            return super().eventFilter(source, event)

        return False

    def test_path(self):
        paths = [self.path_to_download, self.boxart_path, self.screenshot_path, self.path_to_image, self.boxart_path_images, self.screenshot_path_images]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        

            
    def get_api_key(self):
        path = os.getcwd()        
        path_to_json = os.path.join(path,'frames','config','config.json')
        with open(path_to_json, "r") as archivo_config:
            data = json.load(archivo_config)
            key = data["api_key"]
        return key
    
    def get_game(self):
        url_base = "https://api.thegamesdb.net/v1/Games/ByGameName"
        api_key = self.get_api_key()

        params = {
            'apikey': api_key,
            'name': self.qcpc_input_text.toPlainText().strip(),
            'filter[platform]': '4914' 
        }

        request = requests.get(url_base, params=params)

        
        if request.status_code == 200:
            data = request.json()            
            self.qcpc_result_table.clear()  # Clear existing items
            if "data" in data and "games" in data["data"] and data["data"]["games"]:
                for game in data["data"]["games"]:
                    game_id = game["id"]
                    game_title = game["game_title"]
                    release_date = game["release_date"][:4]  # Extraer solo el año
                    platform = game["platform"]
                    region_id = game["region_id"]
                    country_id = game["country_id"]
                    developer_id = developer_id = game["developers"][0] if game["developers"] else None  # Tomar el primer valor de la lista de desarrolladores si existe

                    developer_name = self.get_developer_name(developer_id)

                    # Crear un diccionario con los datos del juego
                    game_data = {
                    "game_id": game_id,
                    "game_title": game_title,
                    "release_date": release_date,
                    "platform": platform,
                    "region_id": region_id,
                    "country_id": country_id,
                    "developer_id": developer_id,
                    "developers": developer_name
                    }



                    item = QListWidgetItem(f"{game_title} - {release_date} -  Desarrollador: {developer_name}")
                    item.setData(Qt.UserRole, game_data)                
                    self.qcpc_result_table.addItem(item)
            else:
            # Show message if no results were found
                self.qcpc_result_table.addItem("No se han encontrado resultados")

        else:
            show_results(self.qcpc_input_output_text,"Error en la petición REST:", request.status_code)
            
    def get_developer_name(self, developer_id):
        # Conectar a la base de datos
        if developer_id is None:
            return "Desconocido"        
        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()

        # Buscar el nombre del desarrollador por su ID en la tabla de desarrolladores
        c.execute('SELECT name FROM developers WHERE id = ?', (developer_id,))
        developer_name = c.fetchone()

        # Cerrar la conexión
        conn.close()

        # Si se encontró el nombre del desarrollador, devolverlo, de lo contrario, devolver "Desconocido"
        if developer_name:
            return developer_name[0]
        else:
            return "Desconocido"
            
    def show_game_image(self, item):
    # Obtener el game_id del item
        game_data = item.data(Qt.UserRole)   
        game_id = game_data["game_id"]     
    # Obtener la imagen del juego y mostrarla en qcpc_image_label
        self.get_game_image(game_id)

    def get_game_image(self, game_id):
        # Determine image paths
        boxart_path = os.path.join(self.path, 'files', 'downloads', 'boxart')
        boxart_path_front = os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_front_boxart.jpg")
        boxart_path_back = os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_back_boxart.jpg")
        screenshot_path_check = os.path.join(self.path, 'files', 'downloads', 'screenshot', f"{game_id}")
        screenshot_path = os.path.join(self.path, 'files', 'downloads', 'screenshot')

        # Check if boxart already exists
        if os.path.exists(boxart_path_front) and os.path.exists(boxart_path_back):
            self.show_image(boxart_path_front)
            show_results(self.qcpc_input_output_text, f"Boxart ya existen.")
            return

        # Check if boxart and screenshot already exist
        if os.path.exists(boxart_path_front) and os.path.exists(boxart_path_back) and os.path.exists(screenshot_path_check):
            show_results(self.qcpc_input_output_text, f"Boxart y pantallazo ya existen.")
            return

        # Make API request for image
        url = f"https://api.thegamesdb.net/v1/Games/Images?apikey={self.get_api_key()}&games_id={game_id}"
        request = requests.get(url)

        # Process image data
        if request.status_code == 200:
            data = request.json()
            if data["data"]["count"] > 0:
                images = data["data"]["images"][str(game_id)]

                for image in images:
                    image_type = image["type"]
                    filename = image["filename"]  # Obtener el nombre de archivo original

                    # Determine image path
                    if image_type == "boxart":
                        image_side = image.get("side", "")
                        if image_side in ["front", "back"]:
                            image_path = os.path.join(boxart_path, f"{game_id}_{image_side}_boxart.jpg")
                            image_url = f"{data['data']['base_url']['thumb']}boxart/{image_side}/{filename}"
                            self.download_image(image_url, image_path, game_id, image_type,filename)
                    elif image_type == "screenshot":
                        image_path = os.path.join(screenshot_path, f"{game_id}_screenshot.jpg")
                        image_url = f"{data['data']['base_url']['thumb']}screenshots/{filename}"
                        self.download_image(image_url, image_path, game_id, image_type,filename)
                    else:
                        continue  # Skip other types of images

                    # Download image
                    image_url = f"{data['data']['base_url']['thumb']}{filename}"
                    self.download_image(image_url, image_path, game_id, image_type, filename)  # Pasar el nombre de archivo
            else:
                show_results(self.qcpc_input_output_text, f"No hay imagenes disponibles.")
        else:
            show_results(self.qcpc_input_output_text, f"Error en la petición REST: {request.status_code}")

    def download_image(self, image_url, image_path, game_id, image_type, filename):
        # Determine file extension from the filename
        #file_extension = filename.split(".")[-1]
        # Construct the full path including the original filename
        #image_path_with_name = os.path.join(image_path, f"{game_id}_{image_type}.{file_extension}")

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            self.show_image(image_path)
            show_results(self.qcpc_input_output_text,f"Imagen guardada para el ID del juego {game_id} ({image_type}) en {image_path}")
        else:
            show_results(self.qcpc_input_output_text,f"Fallo al descargar la imagen {image_type} para el ID del juego {game_id}")


    def show_image(self, image_path):
        original_pixmap = QPixmap(image_path)
        scaled_width = int(original_pixmap.width() * 1.5)
        scaled_height = int(original_pixmap.height() * 1.5)
        scaled_pixmap = original_pixmap.scaled(scaled_width, scaled_height)
        self.qcpc_image_label.setPixmap(scaled_pixmap)
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)
        
    
    def guardar_seleccion(self):
        # Obtener el elemento seleccionado en la tabla de resultados
        selected_item = self.qcpc_result_table.currentItem()

        # Verificar si hay un juego seleccionado
        if selected_item is None:
            show_results(self.qcpc_input_output_text, "No hay ningún juego seleccionado.")
            return

        # Obtener los datos del juego seleccionado
        game_data = selected_item.data(Qt.UserRole)
        
        # Obtener el ID del desarrollador del juego
        developer_id = game_data.get("developer_id")
        
        # Verificar si el juego tiene un desarrollador asociado
        if developer_id is None:
            # Asignar el ID 10861 al desarrollador si no tiene uno asociado
            developer_id = 10861
        game_id = game_data['game_id']
        # Definir las rutas de las imágenes
        front_boxart_path = None
        back_boxart_path = None
        screenshot_path = None
        
        if os.path.exists(os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_front_boxart.jpg")):
            front_boxart_path = os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_front_boxart.jpg")
        if os.path.exists(os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_back_boxart.jpg")):
            back_boxart_path = os.path.join(self.path, 'files', 'downloads', 'boxart', f"{game_id}_back_boxart.jpg")
        if os.path.exists(os.path.join(self.path, 'files', 'downloads', 'screenshot', f"{game_id}_screenshot.jpg")):
            screenshot_path = os.path.join(self.path, 'files', 'downloads', 'screenshot', f"{game_id}_screenshot.jpg")

        # Conectar a la base de datos
        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()
        
        # Verificar si el game_id ya existe en la tabla juegos
        c.execute('''SELECT id FROM juegos WHERE id = ?''', (game_id,))
        existing_game = c.fetchone()

        # Si ya existe un registro con el mismo game_id, mostrar un mensaje y salir de la función
        if existing_game:
            show_results(self.qcpc_input_output_text, f"El juego con ID {game_id} ya está en la base de datos.")
            conn.close()
            return


        # Insertar los datos en la tabla de juegos
        
        if front_boxart_path:
            new_front_boxart_path = os.path.join(self.path, 'files', 'images', 'boxart', f"{game_id}_front_boxart.jpg")
            shutil.move(front_boxart_path, new_front_boxart_path)
        else:
            new_front_boxart_path = 'null'
        if back_boxart_path:
            new_back_boxart_path = os.path.join(self.path, 'files', 'images', 'boxart', f"{game_id}_back_boxart.jpg")
            shutil.move(back_boxart_path, new_back_boxart_path)
        else:
            new_back_boxart_path = 'null'
        if screenshot_path:
            new_screenshot_path = os.path.join(self.path, 'files', 'images', 'screenshot', f"{game_id}")
            shutil.move(screenshot_path, new_screenshot_path)
        else:
            new_screenshot_path = 'null'
            
        c.execute('''INSERT INTO juegos 
            (id, game_title, release_date, platform, region_id, country_id, developer_id, front_boxart_path, back_boxart_path, screenshot_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (game_id, game_data["game_title"], game_data["release_date"], game_data["platform"],
            game_data["region_id"], game_data["country_id"], developer_id, new_front_boxart_path, new_back_boxart_path, new_screenshot_path))
        
        
        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Mostrar mensaje de éxito
        show_results(self.qcpc_input_output_text, "Selección guardada correctamente en la base de datos.")
