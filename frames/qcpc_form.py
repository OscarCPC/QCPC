from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import shutil
import sqlite3
import pandas as pd
from .common import *


class qcpc_form(QWidget):
    # BDD
    config = load_config()
    path = os.getcwd()

    # BDD
    path_to_db = os.path.join(path, "db", "qcpc.db")

    # Descargas
    path_to_download = os.path.join(path, config["paths"]["path_to_download"])
    boxart_path = os.path.join(path, config["paths"]["boxart_path"])
    screenshot_path = os.path.join(path, config["paths"]["screenshot_path"])

    # Guardar descargas
    path_to_image = os.path.join(path, config["paths"]["path_to_image"])
    boxart_path_images = os.path.join(path, config["paths"]["boxart_path_images"])
    screenshot_path_images = os.path.join(
        path, config["paths"]["screenshot_path_images"]
    )

    closed = pyqtSignal()

    is_editing = False
    record_id = None

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
        self.release_date_input.setDisplayFormat("yyyy")

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
        self.front_boxart_button = QPushButton("Seleccionar archivo", self.formFrame)
        self.front_boxart_button.clicked.connect(self.select_front_boxart_file)

        self.back_boxart_label = QLabel("Portada (trasera):", self.formFrame)
        self.back_boxart_input = QLineEdit(self.formFrame)
        self.back_boxart_button = QPushButton("Seleccionar archivo", self.formFrame)
        self.back_boxart_button.clicked.connect(self.select_back_boxart_file)

        self.screenshot_label = QLabel("Captura de pantalla:", self.formFrame)
        self.screenshot_input = QLineEdit(self.formFrame)
        self.screenshot_button = QPushButton("Seleccionar archivo", self.formFrame)
        self.screenshot_button.clicked.connect(self.select_screenshot_file)

        self.url_label = QLabel("URL:", self.formFrame)
        self.url_input = QLineEdit(self.formFrame)

        self.comments_label = QLabel("Comentarios:", self.formFrame)
        self.comments_input = QTextEdit(self.formFrame)

        # Añadir los campos al formulario
        self.formLayout.addRow(self.game_title_label, self.game_title_input)
        self.formLayout.addRow(self.release_date_label, self.release_date_input)
        self.formLayout.addRow(self.platform_label, self.platform_input)
        self.formLayout.addRow(self.region_id_label, self.region_id_input)
        self.formLayout.addRow(self.country_id_label, self.country_id_input)
        self.formLayout.addRow(self.developer_id_label, self.developer_id_input)
        self.formLayout.addRow(self.front_boxart_label, self.front_boxart_input)
        self.formLayout.addRow(QLabel(""), self.front_boxart_button)
        self.formLayout.addRow(self.back_boxart_label, self.back_boxart_input)
        self.formLayout.addRow(QLabel(""), self.back_boxart_button)
        self.formLayout.addRow(self.screenshot_label, self.screenshot_input)
        self.formLayout.addRow(QLabel(""), self.screenshot_button)
        self.formLayout.addRow(self.url_label, self.url_input)
        self.formLayout.addRow(self.comments_label, self.comments_input)

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

    def load_data(self, item_data):
        self.is_editing = True
        self.record_id = item_data.get(
            "id"
        )  # Suponiendo que cada registro tiene un ID único

        self.game_title_input.setText(str(item_data.get("game_title", "")))

        release_date = item_data.get("release_date")
        if release_date:
            self.release_date_input.setDate(QDate(int(release_date), 1, 1))
        else:
            self.release_date_input.setDate(QDate.currentDate())

        self.platform_input.setText(str(item_data.get("platform", "")))
        self.region_id_input.setText(str(item_data.get("region_id", "")))
        self.country_id_input.setText(str(item_data.get("country_id", "")))
        self.developer_id_input.setText(str(item_data.get("developer_id", "")))
        self.front_boxart_input.setText(str(item_data.get("front_boxart_path", "")))
        self.back_boxart_input.setText(str(item_data.get("back_boxart_path", "")))
        self.screenshot_input.setText(str(item_data.get("screenshot_path", "")))
        self.url_input.setText(str(item_data.get("url", "")))
        self.comments_input.setPlainText(str(item_data.get("comentarios", "")))

    def save_record(self):
        game_title = self.game_title_input.text()
        release_date = self.release_date_input.date().year()
        platform = self.platform_input.text()
        region_id = self.region_id_input.text()
        country_id = self.country_id_input.text()
        developer_id = self.developer_id_input.text()
        front_boxart_path = self.front_boxart_input.text()
        back_boxart_path = self.back_boxart_input.text()
        screenshot_path = self.screenshot_input.text()
        url = self.url_input.text()
        comentarios = self.comments_input.toPlainText()

        conn = sqlite3.connect(self.path_to_db)
        cursor = conn.cursor()
        print("Conexión establecida")
        print(self.is_editing)
        try:
            if self.is_editing:
                # Actualizar registro existente
                cursor.execute(
                    """
                    UPDATE juegos
                    SET game_title = ?, release_date = ?, platform = ?, region_id = ?, country_id = ?, developer_id = ?, front_boxart_path = ?, back_boxart_path = ?, screenshot_path = ?, url = ?, comentarios = ?
                    WHERE id = ?
                """,
                    (
                        game_title,
                        release_date,
                        platform,
                        region_id,
                        country_id,
                        developer_id,
                        front_boxart_path,
                        back_boxart_path,
                        screenshot_path,
                        url,
                        comentarios,
                        self.record_id,
                    ),
                )
            else:
                # Insertar nuevo registro
                cursor.execute(
                    """
                    INSERT INTO juegos (game_title, release_date, platform, region_id, country_id, developer_id, front_boxart_path, back_boxart_path, screenshot_path, url, comentarios)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        game_title,
                        release_date,
                        platform,
                        region_id,
                        country_id,
                        developer_id,
                        front_boxart_path,
                        back_boxart_path,
                        screenshot_path,
                        url,
                        comentarios,
                    ),
                )
        except Exception as e:
            print("Error al guardar el registro")
            print(e)
        finally:
            conn.commit()
            conn.close()

        self.close()

    def select_front_boxart_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de portada frontal",
            "",
            "Images (*.png *.xpm *.jpg);;All Files (*)",
            options=options,
        )
        if file_path:
            # Definir la ruta de destino
            new_file_path = os.path.join(
                self.path, "files", "images", "boxart", os.path.basename(file_path)
            )
            # Copiar el archivo a la ruta de destino
            shutil.copy(file_path, new_file_path)
            # Actualizar el campo de texto con la ruta relativa del archivo
            relative_path = os.path.relpath(new_file_path, self.path)
            self.front_boxart_input.setText(relative_path)

    def select_back_boxart_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de portada trasera",
            "",
            "Images (*.png *.xpm *.jpg);;All Files (*)",
            options=options,
        )
        if file_path:
            # Definir la ruta de destino
            new_file_path = os.path.join(
                self.path, "files", "images", "boxart", os.path.basename(file_path)
            )
            # Copiar el archivo a la ruta de destino
            shutil.copy(file_path, new_file_path)
            # Actualizar el campo de texto con la ruta relativa del archivo
            relative_path = os.path.relpath(new_file_path, self.path)
            self.back_boxart_input.setText(relative_path)

    def select_screenshot_file(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos de captura de pantalla",
            "",
            "Images (*.png *.xpm *.jpg);;All Files (*)",
            options=options,
        )
        if files:
            relative_paths = []
            for file_path in files:
                # Definir la ruta de destino
                new_file_path = os.path.join(
                    self.path,
                    "files",
                    "images",
                    "screenshot",
                    os.path.basename(file_path),
                )
                # Copiar el archivo a la ruta de destino
                shutil.copy(file_path, new_file_path)
                # Obtener la ruta relativa del archivo
                relative_path = os.path.relpath(new_file_path, self.path)
                relative_paths.append(relative_path)
            # Actualizar el campo de texto con las rutas relativas de los archivos seleccionados
            self.screenshot_input.setText(";".join(relative_paths))

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
