from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import sqlite3
import pandas as pd
from .common import *


class qcpc_form(QWidget):
    
    def setupUi(self):
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

        # Crear el layout principal
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Frame de formulario para los datos del juego
        self.formFrame = QFrame(self)
        self.formFrame.setObjectName("formFrame")
        self.formFrame.setFrameShape(QFrame.StyledPanel)
        self.formFrame.setFrameShadow(QFrame.Raised)
        self.formLayout = QFormLayout(self.formFrame)

        # Crear campos del formulario
        self.game_title_label = QLabel("Título del juego:", self.formFrame)
        self.game_title_input = QLineEdit(self.formFrame)

        self.release_date_label = QLabel("Fecha de lanzamiento:", self.formFrame)
        self.release_date_input = QDateEdit(self.formFrame)

        self.platform_label = QLabel("Plataforma:", self.formFrame)
        self.platform_input = QLineEdit(self.formFrame)

        self.region_id_label = QLabel("ID de región:", self.formFrame)
        self.region_id_input = QLineEdit(self.formFrame)

        self.country_id_label = QLabel("ID de país:", self.formFrame)
        self.country_id_input = QLineEdit(self.formFrame)

        self.developer_id_label = QLabel("ID del desarrollador:", self.formFrame)
        self.developer_id_input = QLineEdit(self.formFrame)

        self.front_boxart_label = QLabel("Portada (frontal):", self.formFrame)
        self.front_boxart_input = QLineEdit(self.formFrame)

        self.back_boxart_label = QLabel("Portada (trasera):", self.formFrame)
        self.back_boxart_input = QLineEdit(self.formFrame)

        self.screenshot_label = QLabel("Captura de pantalla:", self.formFrame)
        self.screenshot_input = QLineEdit(self.formFrame)

        self.url_label = QLabel("URL:", self.formFrame)
        self.url_input = QLineEdit(self.formFrame)

        # Añadir los campos al formulario
        self.formLayout.addRow(self.game_title_label, self.game_title_input)
        self.formLayout.addRow(self.release_date_label, self.release_date_input)
        self.formLayout.addRow(self.platform_label, self.platform_input)
        self.formLayout.addRow(self.region_id_label, self.region_id_input)
        self.formLayout.addRow(self.country_id_label, self.country_id_input)
        self.formLayout.addRow(self.developer_id_label, self.developer_id_input)
        self.formLayout.addRow(self.front_boxart_label, self.front_boxart_input)
        self.formLayout.addRow(self.back_boxart_label, self.back_boxart_input)
        self.formLayout.addRow(self.screenshot_label, self.screenshot_input)
        self.formLayout.addRow(self.url_label, self.url_input)

        # Botones
        self.save_button = QPushButton("Guardar", self)
        self.cancel_button = QPushButton("Cancelar", self)

        # Añadir botones al layout
        self.gridLayout.addWidget(self.formFrame, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.save_button, 1, 0)
        self.gridLayout.addWidget(self.cancel_button, 1, 1)

        # Configurar el tamaño de los botones
        self.save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Configurar traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()

    def retranslateUi(self):
        self.setWindowTitle("Formulario de Edición/Adición")
    
    def setup_connections(self):
        # Aquí debes conectar los botones a las funciones correspondientes
        self.save_button.clicked.connect(self.save_record)
        self.cancel_button.clicked.connect(self.close)  # Cerrar el formulario

    def save_record(self):
        # Aquí implementas la lógica para guardar los datos
        print("Datos guardados")  # Placeholder, reemplázalo con la lógica de guardado


