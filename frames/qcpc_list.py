from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import sqlite3
from .common import *


class qcpc_list(QWidget):
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
        self.formLayout_2.setObjectName("formLayout_2")
        
        # Contenedor principal
        self.qcpc_frame_container = QFrame(self)
        self.qcpc_frame_container.setObjectName("qcpc_frame_container")
        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)
        
        # Layout principal
        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # Frame de la lista de atributos (Widget 1)
        self.qcpc_attribute_list_frame = QListWidget(self.qcpc_frame_container)
        self.qcpc_attribute_list_frame.setObjectName("qcpc_attribute_list_frame")
        self.qcpc_attribute_list_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_attribute_list_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_attributes = QVBoxLayout(self.qcpc_attribute_list_frame)
        self.verticalLayout_attributes.setObjectName("verticalLayout_attributes")
        self.qcpc_attribute_list = QListWidget(self.qcpc_attribute_list_frame)
        self.qcpc_attribute_list.setObjectName("qcpc_attribute_list")
        self.verticalLayout_attributes.addWidget(self.qcpc_attribute_list)

        # Añadir el frame de la lista de atributos al layout principal
        self.gridLayout_2.addWidget(self.qcpc_attribute_list_frame, 0, 0, 2, 1)  # 2 filas de altura

        # Frame de la imagen (Widget 2)
        self.qcpc_image_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_image_frame.setObjectName("qcpc_image_frame")
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_image_layout = QVBoxLayout(self.qcpc_image_frame)
        self.qcpc_image_layout.setObjectName("qcpc_image_layout")
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName("qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(QSize(300, 450))  # Ocupa la mitad de la altura del primer widget
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)
        self.qcpc_image_layout.addWidget(self.qcpc_image_label)

        # Añadir el frame de la imagen al layout principal
        self.gridLayout_2.addWidget(self.qcpc_image_frame, 0, 1, 1, 1)

        # Frame del texto (Widget 3)
        self.qcpc_text_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_text_frame.setObjectName("qcpc_text_frame")
        self.qcpc_text_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_text_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_text_layout = QVBoxLayout(self.qcpc_text_frame)
        self.qcpc_text_layout.setObjectName("qcpc_text_layout")
        self.qcpc_text_label = QTextEdit(self.qcpc_text_frame)
        self.qcpc_text_label.setObjectName("qcpc_text_label")
        self.qcpc_text_label.setReadOnly(True)
        self.qcpc_text_layout.addWidget(self.qcpc_text_label)

        # Añadir el frame del texto al layout principal
        self.gridLayout_2.addWidget(self.qcpc_text_frame, 1, 1, 1, 1)

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.qcpc_frame_container)

        # Traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)
        
        self.show_all_games()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("qcpc_search", "Form", None))
        self.qcpc_attribute_list.setWindowTitle(QCoreApplication.translate("qcpc_search", "Atributos", None))
        self.qcpc_image_label.setText(QCoreApplication.translate("qcpc_search", "Imagen", None))
        self.qcpc_text_label.setPlaceholderText(QCoreApplication.translate("qcpc_search", "Resultados", None))

    def setup_connections(self):
        pass  # Aquí puedes definir las conexiones necesarias
    
    def show_all_games(self):
        try:
            conn = sqlite3.connect(self.path_to_db)
            conn.row_factory = sqlite3.Row  # Habilitar el acceso a las columnas por nombre
            c = conn.cursor()

            result = c.execute('SELECT * FROM juegos')
            rows = result.fetchall()

            # Convertir a JSON
            rows_as_dict = [dict(row) for row in rows]

            # Convertir a JSON y luego deserializar para iterar sobre él
            json_result = json.dumps(rows_as_dict)
            data = json.loads(json_result)
            
            for item_data in data:
                item = QListWidgetItem(f"{item_data['game_title']}")
                item.setData(Qt.UserRole, item_data)
                self.qcpc_attribute_list.addItem(item)
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            conn.close()
        