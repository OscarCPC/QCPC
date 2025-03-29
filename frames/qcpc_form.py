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

    def __init__(self, parent=None):
        super(qcpc_form, self).__init__(parent)
        self.setupUi()

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

        # Sección: Título del juego
        title_layout = QHBoxLayout()
        self.game_title_label = QLabel("Título del juego:", self.mainFrame)
        self.game_title_input = QLineEdit(self.mainFrame)
        title_layout.addWidget(self.game_title_label)
        title_layout.addWidget(self.game_title_input)
        self.gridLayout.addLayout(title_layout, current_row, 0, 1, 2)

        # Sección: Fecha de lanzamiento
        current_row += 1
        release_date_layout = QHBoxLayout()
        self.release_date_label = QLabel("Fecha de lanzamiento:", self.mainFrame)
        self.release_date_input = QDateEdit(self.mainFrame)
        self.release_date_input.setDisplayFormat("yyyy")
        release_date_layout.addWidget(self.release_date_label)
        release_date_layout.addWidget(self.release_date_input)
        self.gridLayout.addLayout(release_date_layout, current_row, 0, 1, 2)

        # Sección: Plataforma
        current_row += 1
        platform_layout = QHBoxLayout()
        self.platform_label = QLabel("Plataforma:", self.mainFrame)
        self.platform_input = QLineEdit(self.mainFrame)
        platform_layout.addWidget(self.platform_label)
        platform_layout.addWidget(self.platform_input)
        self.gridLayout.addLayout(platform_layout, current_row, 0, 1, 2)

        # Sección: Región
        current_row += 1
        region_layout = QHBoxLayout()
        self.region_id_label = QLabel("ID de región:", self.mainFrame)
        self.region_id_input = QLineEdit(self.mainFrame)
        region_layout.addWidget(self.region_id_label)
        region_layout.addWidget(self.region_id_input)
        self.gridLayout.addLayout(region_layout, current_row, 0, 1, 2)

        # Sección: País
        current_row += 1
        country_layout = QHBoxLayout()
        self.country_id_label = QLabel("ID de país:", self.mainFrame)
        self.country_id_input = QLineEdit(self.mainFrame)
        country_layout.addWidget(self.country_id_label)
        country_layout.addWidget(self.country_id_input)
        self.gridLayout.addLayout(country_layout, current_row, 0, 1, 2)

        # Sección: Desarrollador
        current_row += 1
        developer_layout = QHBoxLayout()
        self.developer_id_label = QLabel("Desarrollador:", self.mainFrame)
        self.developer_id_input = QComboBox(self.mainFrame)
        self.developer_id_input.setFixedHeight(40)
        self.developer_id_input.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.developer_id_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        developer_layout.addWidget(self.developer_id_label)
        developer_layout.addWidget(self.developer_id_input)
        self.gridLayout.addLayout(developer_layout, current_row, 0, 1, 2)

        # Sección: Portada frontal
        current_row += 1
        front_boxart_layout = QHBoxLayout()
        self.front_boxart_label = QLabel("Portada (frontal):", self.mainFrame)
        self.front_boxart_input = QLineEdit(self.mainFrame)
        self.front_boxart_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.front_boxart_button.clicked.connect(self.select_front_boxart_file)
        front_boxart_layout.addWidget(self.front_boxart_label)
        front_boxart_layout.addWidget(self.front_boxart_input)
        front_boxart_layout.addWidget(self.front_boxart_button)
        self.gridLayout.addLayout(front_boxart_layout, current_row, 0, 1, 2)

        # Sección: Portada trasera
        current_row += 1
        back_boxart_layout = QHBoxLayout()
        self.back_boxart_label = QLabel("Portada (trasera):", self.mainFrame)
        self.back_boxart_input = QLineEdit(self.mainFrame)
        self.back_boxart_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.back_boxart_button.clicked.connect(self.select_back_boxart_file)
        back_boxart_layout.addWidget(self.back_boxart_label)
        back_boxart_layout.addWidget(self.back_boxart_input)
        back_boxart_layout.addWidget(self.back_boxart_button)
        self.gridLayout.addLayout(back_boxart_layout, current_row, 0, 1, 2)

        # Sección: Capturas de pantalla
        current_row += 1
        screenshot_layout = QHBoxLayout()
        self.screenshot_label = QLabel("Captura de pantalla:", self.mainFrame)
        self.screenshot_input = QLineEdit(self.mainFrame)
        self.screenshot_button = QPushButton("Seleccionar archivo", self.mainFrame)
        self.screenshot_button.clicked.connect(self.select_screenshot_file)
        screenshot_layout.addWidget(self.screenshot_label)
        screenshot_layout.addWidget(self.screenshot_input)
        screenshot_layout.addWidget(self.screenshot_button)
        self.gridLayout.addLayout(screenshot_layout, current_row, 0, 1, 2)

        # Sección: URL
        current_row += 1
        url_layout = QHBoxLayout()
        self.url_label = QLabel("URL:", self.mainFrame)
        self.url_input = QLineEdit(self.mainFrame)
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)
        self.gridLayout.addLayout(url_layout, current_row, 0, 1, 2)

        # Sección: Comentarios
        current_row += 1
        comments_layout = QVBoxLayout()
        self.comments_label = QLabel("Comentarios:", self.mainFrame)
        self.comments_input = QTextEdit(self.mainFrame)
        comments_layout.addWidget(self.comments_label)
        comments_layout.addWidget(self.comments_input)
        self.gridLayout.addLayout(comments_layout, current_row, 0, 1, 2)

        # Sección: Botones
        current_row += 1
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar", self.mainFrame)
        self.cancel_button = QPushButton("Cancelar", self.mainFrame)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        self.gridLayout.addLayout(buttons_layout, current_row, 0, 1, 2)

        # Añadir el frame principal al layout principal
        self.mainLayout.addWidget(self.mainFrame)

        # Configurar el espaciado y márgenes
        self.gridLayout.setSpacing(15)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)

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
        # Cargar los datos en los campos del formulario
        self.game_title_input.setText(item_data.get("game_title", ""))

        # Asegurarnos de que release_date sea una cadena en el formato "yyyy-MM-dd"
        release_date = item_data.get("release_date", "2000-01-01")
        if isinstance(release_date, int):  # Si es un entero, convertirlo a cadena
            release_date = f"{release_date}-01-01"
        self.release_date_input.setDate(QDate.fromString(release_date, "yyyy-MM-dd"))

        # Convertir valores numéricos a cadenas antes de usar setText
        self.platform_input.setText(str(item_data.get("platform", "")))
        self.region_id_input.setText(str(item_data.get("region_id", "")))
        self.country_id_input.setText(str(item_data.get("country_id", "")))

        # Usar setCurrentText para seleccionar el desarrollador en el QComboBox
        developer_name = item_data.get("developer_id", "")
        index = self.developer_id_input.findText(str(developer_name))
        if index != -1:
            self.developer_id_input.setCurrentIndex(index)
        else:
            self.developer_id_input.setCurrentIndex(
                0
            )  # Seleccionar el primer elemento si no se encuentra

        self.front_boxart_input.setText(item_data.get("front_boxart_path", ""))
        self.back_boxart_input.setText(item_data.get("back_boxart_path", ""))
        self.screenshot_input.setText(item_data.get("screenshot_path", ""))
        self.url_input.setText(item_data.get("url", ""))
        self.comments_input.setPlainText(item_data.get("comentarios", ""))

    def save_record(self):
        game_title = self.game_title_input.text()
        release_date = self.release_date_input.date().year()
        platform = 4914
        region_id = self.region_id_input.text() or None
        country_id = self.country_id_input.text() or None
        developer_id = self.developer_id_input.currentData()
        front_boxart_path = self.front_boxart_input.text()
        back_boxart_path = self.back_boxart_input.text()
        screenshot_paths = self.screenshot_input.text().split(";")
        url = self.url_input.text()
        comentarios = self.comments_input.toPlainText()

        print(f"game_title: {game_title}")
        print(f"release_date: {release_date}")
        print(f"platform: {platform}")
        print(f"region_id: {region_id}")
        print(f"country_id: {country_id}")
        print(f"developer_id: {developer_id}")
        print(f"front_boxart_path: {front_boxart_path}")
        print(f"back_boxart_path: {back_boxart_path}")
        print(f"screenshot_paths: {screenshot_paths}")
        print(f"url: {url}")
        print(f"comentarios: {comentarios}")

        conn = sqlite3.connect(self.path_to_db)
        cursor = conn.cursor()
        print("Conexión establecida")
        print(f"is_editing: {self.is_editing}")
        try:
            if self.is_editing:
                # Actualizar registro existente
                cursor.execute(
                    """
                    UPDATE juegos
                    SET game_title = ?, release_date = ?, platform = ?, region_id = ?, country_id = ?, developer_id = ?, front_boxart_path = ?, back_boxart_path = ?, url = ?, comentarios = ?
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
                        url,
                        comentarios,
                        self.record_id,
                    ),
                )
                print("Registro actualizado")

                # Actualizar capturas de pantalla existentes
                cursor.execute(
                    "DELETE FROM screenshots WHERE game_id = ?", (self.record_id,)
                )
                for path in screenshot_paths:
                    cursor.execute(
                        "INSERT INTO screenshots (game_id, screenshot_path) VALUES (?, ?)",
                        (self.record_id, path),
                    )
                print("Capturas de pantalla actualizadas")
            else:
                # Insertar nuevo registro
                cursor.execute(
                    """
                    INSERT INTO juegos (game_title, release_date, platform, region_id, country_id, developer_id, front_boxart_path, back_boxart_path, url, comentarios)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        url,
                        comentarios,
                    ),
                )
                self.record_id = cursor.lastrowid
                print("Nuevo registro insertado")

                # Insertar nuevas capturas de pantalla
                for path in screenshot_paths:
                    cursor.execute(
                        "INSERT INTO screenshots (game_id, screenshot_path) VALUES (?, ?)",
                        (self.record_id, path),
                    )
                print("Nuevas capturas de pantalla insertadas")

        except Exception as e:
            print("Error al guardar el registro")
            print(e)
        finally:
            conn.commit()
            conn.close()
            print("Conexión cerrada")

        self.close()
        print("Formulario cerrado")

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
