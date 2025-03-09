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

        # Layout principal
        self.mainLayout = QGridLayout(self)

        # Frame principal
        self.mainFrame = QFrame(self)
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)

        # Grid layout para el frame principal
        self.gridLayout = QGridLayout(self.mainFrame)

        # Crear y añadir los widgets al grid
        current_row = 0

        # Título del juego
        self.game_title_label = QLabel("Título del juego:", self.mainFrame)
        self.game_title_input = QLineEdit(self.mainFrame)
        self.gridLayout.addWidget(self.game_title_label, current_row, 0)
        self.gridLayout.addWidget(self.game_title_input, current_row, 1, 1, 2)

        # Fecha de lanzamiento
        current_row += 1
        self.release_date_label = QLabel("Fecha de lanzamiento:", self.mainFrame)
        self.release_date_input = QDateEdit(self.mainFrame)
        self.release_date_input.setDisplayFormat("yyyy")
        self.gridLayout.addWidget(self.release_date_label, current_row, 0)
        self.gridLayout.addWidget(self.release_date_input, current_row, 1)

        # Plataforma
        current_row += 1
        self.platform_label = QLabel("Plataforma:", self.mainFrame)
        self.platform_input = QLineEdit(self.mainFrame)
        self.gridLayout.addWidget(self.platform_label, current_row, 0)
        self.gridLayout.addWidget(self.platform_input, current_row, 1, 1, 2)

        # Región
        current_row += 1
        self.region_id_label = QLabel("ID de región:", self.mainFrame)
        self.region_id_input = QLineEdit(self.mainFrame)
        self.gridLayout.addWidget(self.region_id_label, current_row, 0)
        self.gridLayout.addWidget(self.region_id_input, current_row, 1, 1, 2)

        # País
        current_row += 1
        self.country_id_label = QLabel("ID de país:", self.mainFrame)
        self.country_id_input = QLineEdit(self.mainFrame)
        self.gridLayout.addWidget(self.country_id_label, current_row, 0)
        self.gridLayout.addWidget(self.country_id_input, current_row, 1, 1, 2)

        # Desarrollador
        # Desarrollador
        current_row += 1
        self.developer_id_label = QLabel("Desarrollador:", self.mainFrame)
        self.developer_id_input = QComboBox(self.mainFrame)
        self.developer_id_input.setFixedSize(
            int(self.width() / 2), 40
        )  # Tamaño fijo proporcional
        view = self.developer_id_input.view()
        view.setMinimumHeight(100)  # Altura mínima del desplegable
        view.setMaximumHeight(300)  # Altura máxima del desplegable

        self.gridLayout.addWidget(self.developer_id_label, current_row, 0)
        self.gridLayout.addWidget(self.developer_id_input, current_row, 1, 1, 2)
        # Portada frontal
        current_row += 1
        self.front_boxart_label = QLabel("Portada (frontal):", self.mainFrame)
        self.front_boxart_input = QLineEdit(self.mainFrame)
        self.front_boxart_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.front_boxart_button.clicked.connect(self.select_front_boxart_file)
        self.gridLayout.addWidget(self.front_boxart_label, current_row, 0)
        self.gridLayout.addWidget(self.front_boxart_input, current_row, 1)
        self.gridLayout.addWidget(self.front_boxart_button, current_row, 2)

        # Portada trasera
        current_row += 1
        self.back_boxart_label = QLabel("Portada (trasera):", self.mainFrame)
        self.back_boxart_input = QLineEdit(self.mainFrame)
        self.back_boxart_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.back_boxart_button.clicked.connect(self.select_back_boxart_file)
        self.gridLayout.addWidget(self.back_boxart_label, current_row, 0)
        self.gridLayout.addWidget(self.back_boxart_input, current_row, 1)
        self.gridLayout.addWidget(self.back_boxart_button, current_row, 2)

        # Capturas de pantalla
        current_row += 1
        self.screenshot_label = QLabel("Captura de pantalla:", self.mainFrame)
        self.screenshot_input = QLineEdit(self.mainFrame)
        self.screenshot_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.screenshot_button.clicked.connect(self.select_screenshot_file)
        self.gridLayout.addWidget(self.screenshot_label, current_row, 0)
        self.gridLayout.addWidget(self.screenshot_input, current_row, 1)
        self.gridLayout.addWidget(self.screenshot_button, current_row, 2)

        # URL
        current_row += 1
        self.url_label = QLabel("URL:", self.mainFrame)
        self.url_input = QLineEdit(self.mainFrame)
        self.gridLayout.addWidget(self.url_label, current_row, 0)
        self.gridLayout.addWidget(self.url_input, current_row, 1, 1, 2)

        # Comentarios
        current_row += 1
        self.comments_label = QLabel("Comentarios:", self.mainFrame)
        self.comments_input = QTextEdit(self.mainFrame)
        self.gridLayout.addWidget(self.comments_label, current_row, 0)
        self.gridLayout.addWidget(self.comments_input, current_row, 1, 1, 2)

        # Botones
        current_row += 1
        self.save_button = QPushButton("Guardar", self.mainFrame)
        self.cancel_button = QPushButton("Cancelar", self.mainFrame)
        self.gridLayout.addWidget(self.save_button, current_row, 1)
        self.gridLayout.addWidget(self.cancel_button, current_row, 2)

        # Añadir el frame principal al layout principal
        self.mainLayout.addWidget(self.mainFrame)

        # Configurar el espaciado y márgenes
        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)

        # Configurar traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        self.populate_developer_combobox()

    def populate_developer_combobox(self):
        for developer in self.get_developers():
            self.developer_id_input.addItem(developer[1], developer[0])

    def retranslateUi(self):
        self.setWindowTitle("Formulario de Edición/Adición")

    def setup_connections(self):
        # Aquí debes conectar los botones a las funciones correspondientes
        self.save_button.clicked.connect(self.save_record)
        self.cancel_button.clicked.connect(self.close)  # Cerrar el formulario

    def get_developers(self):
        try:
            conn = sqlite3.connect(self.path_to_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM developers")
            developers = cursor.fetchall()
            return developers
        except Exception as e:
            print("Error al obtener los desarrolladores")
            print(e)
        finally:
            conn.close()

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
        if item_data.get("platform") == 4914:
            self.platform_input.setText(str("Amstrad CPC"))
        else:
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
        platform = 4914
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
                    SET game_title = ?, release_date = ?, platform = , region_id = ?, country_id = ?, developer_id = ?, front_boxart_path = ?, back_boxart_path = ?, screenshot_path = ?, url = ?, comentarios = ?
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
