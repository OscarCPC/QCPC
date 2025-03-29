from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import requests
import sqlite3
import shutil  # Se necesita para mover archivos
from .common import *


class qcpc_search(QWidget):
    path = os.getcwd()

    # BDD
    path_to_db = os.path.join(path, "db", "qcpc.db")

    # Descargas
    path_to_download = os.path.join(path, "files", "downloads")
    boxart_path = os.path.join(path_to_download, "boxart")
    screenshot_path = os.path.join(path_to_download, "screenshot")

    # Guardar descargas
    path_to_image = os.path.join(path, "files", "images")
    boxart_path_images = os.path.join(path_to_image, "boxart")
    screenshot_path_images = os.path.join(path_to_image, "screenshot")

    def __init__(self, parent=..., flags=...):
        super().__init__(parent, flags)
        self.setupUi()

    def setupUi(self):
        self.resize(1100, 950)
        self.setMinimumSize(QSize(1100, 950))

        self.formLayout_2 = QFormLayout(self)
        self.qcpc_frame_container = QFrame(self)
        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)

        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.qcpc_input_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_input_frame.setLayoutDirection(Qt.RightToLeft)
        self.qcpc_input_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_input_frame.setFrameShadow(QFrame.Raised)

        self.qcpc_input_layout = QFormLayout(self.qcpc_input_frame)
        self.qcpc_input_label = QLabel(self.qcpc_input_frame)
        self.qcpc_input_label.setMinimumSize(QSize(250, 0))
        self.qcpc_input_label.setAlignment(Qt.AlignCenter)
        self.qcpc_input_label.setText("Título a buscar")

        self.qcpc_input_layout.setWidget(
            0, QFormLayout.FieldRole, self.qcpc_input_label
        )

        self.qcpc_input_text = QPlainTextEdit(self.qcpc_input_frame)
        self.qcpc_input_text.setMinimumSize(QSize(275, 30))
        self.qcpc_input_text.setMaximumSize(QSize(16777215, 30))
        self.qcpc_input_text.installEventFilter(self)
        self.qcpc_input_layout.setWidget(1, QFormLayout.FieldRole, self.qcpc_input_text)

        self.qcpc_input_search = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_search.setMinimumSize(QSize(80, 30))
        self.qcpc_input_search.setMaximumSize(QSize(80, 30))
        self.qcpc_input_search.setLayoutDirection(Qt.LeftToRight)
        self.qcpc_input_search.setText("Buscar")
        self.qcpc_input_search.setDefault(True)
        self.qcpc_input_search.setShortcut(Qt.Key_Return)
        self.qcpc_input_layout.setWidget(
            2, QFormLayout.FieldRole, self.qcpc_input_search
        )

        self.qcpc_form_editable = QFormLayout()  # Layout para el formulario editable
        self.qcpc_input_layout.setLayout(
            3, QFormLayout.SpanningRole, self.qcpc_form_editable
        )

        self.gridLayout_2.addWidget(self.qcpc_input_frame, 0, 0, 1, 1)

        self.qcpc_image_frame = QFrame(self)
        self.qcpc_image_frame.setMinimumSize(QSize(600, 900))
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.qcpc_image_frame)
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)

        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setMinimumSize(QSize(600, 900))
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.qcpc_image_label)
        self.gridLayout_2.addWidget(self.qcpc_image_frame, 0, 1, 2, 1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.qcpc_frame_container)

        self.qcpc_input_frame_save = QPushButton(self.qcpc_frame_container)
        self.qcpc_input_frame_save.setText("Guardar Selección")
        self.qcpc_input_layout.addWidget(self.qcpc_input_frame_save)

        self.qcpc_input_frame_delete = QPushButton(self.qcpc_frame_container)
        self.qcpc_input_frame_delete.setText("Borrar")
        self.qcpc_input_layout.addWidget(self.qcpc_input_frame_delete)

        self.retranslateUi(self)
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, qcpc_search):
        qcpc_search.setWindowTitle(
            QCoreApplication.translate("qcpc_search", "Form", None)
        )

    def create_editable_form(self, game_data):
        # Limpiar el formulario anterior
        for i in reversed(range(self.qcpc_form_editable.count())):
            widget = self.qcpc_form_editable.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Crear campos de entrada editables
        self.qcpc_form_editable.addRow(
            "ID del Juego:", QLabel(str(game_data["game_id"]))
        )

        self.game_title_input = QLineEdit(str(game_data["game_title"]))
        self.qcpc_form_editable.addRow("Título:", self.game_title_input)

        self.release_date_input = QLineEdit(str(game_data["release_date"]))
        self.qcpc_form_editable.addRow("Fecha de lanzamiento:", self.release_date_input)

        self.platform_input = QLineEdit(
            str(game_data["platform"])
        )  # Convertir a string
        self.qcpc_form_editable.addRow("Plataforma:", self.platform_input)

        self.developer_input = QLineEdit(str(game_data["developers"]))
        self.qcpc_form_editable.addRow("Desarrollador:", self.developer_input)

    def setup_connections(self):
        self.qcpc_input_search.clicked.connect(self.get_game)
        self.qcpc_input_frame_save.clicked.connect(self.guardar_seleccion)
        self.qcpc_input_frame_delete.clicked.connect(
            lambda: self.qcpc_input_text.clear()
        )

    def eventFilter(self, source, event):
        if source is self.qcpc_input_text and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.qcpc_input_search.click()  # Simular clic en el botón
            elif (
                event.key() == Qt.Key_Escape
            ):  # Si se presiona Escape, limpiar el texto
                self.qcpc_input_text.clear()
        else:
            return super().eventFilter(source, event)

        return False

    def test_path(self):
        paths = [
            self.path_to_download,
            self.boxart_path,
            self.screenshot_path,
            self.path_to_image,
            self.boxart_path_images,
            self.screenshot_path_images,
        ]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def get_api_key(self):
        path = os.getcwd()
        path_to_json = os.path.join(path, "frames", "config", "config.json")
        with open(path_to_json, "r") as archivo_config:
            data = json.load(archivo_config)
            key = data["api_key"]
        return key

    def get_game(self):
        url_base = "https://api.thegamesdb.net/v1/Games/ByGameName"
        api_key = self.get_api_key()

        params = {
            "apikey": api_key,
            "name": self.qcpc_input_text.toPlainText().strip(),
            "filter[platform]": "4914",
        }

        request = requests.get(url_base, params=params)

        if request.status_code == 200:
            data = request.json()
            if "data" in data and "games" in data["data"] and data["data"]["games"]:
                game = data["data"]["games"][
                    0
                ]  # Usar el primer resultado para la edición
                game_data = {
                    "game_id": game["id"],
                    "game_title": game["game_title"],
                    "release_date": game["release_date"][:4],
                    "platform": game["platform"],
                    "region_id": game["region_id"],
                    "country_id": game["country_id"],
                    "developer_id": (
                        game["developers"][0] if game["developers"] else None
                    ),
                    "developers": self.get_developer_name(
                        game["developers"][0] if game["developers"] else None
                    ),
                }

                self.create_editable_form(game_data)
            else:
                self.qcpc_input_output_text.setText("No se han encontrado resultados")
        else:
            self.qcpc_input_output_text.setText(
                f"Error en la petición REST: {request.status_code}"
            )

    def get_developer_name(self, developer_id):
        if developer_id is None:
            return "Desconocido"
        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()

        c.execute("SELECT name FROM developers WHERE id = ?", (developer_id,))
        developer_name = c.fetchone()

        conn.close()

        if developer_name:
            return developer_name[0]
        else:
            return "Desconocido"

    def show_game_image(self, item):
        game_data = item.data(Qt.UserRole)
        game_id = game_data["game_id"]
        self.get_game_image(game_id)

    def get_game_image(self, game_id):
        boxart_path = os.path.join(self.path, "files", "downloads", "boxart")
        boxart_path_front = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
        )
        boxart_path_back = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_back_boxart.jpg"
        )
        screenshot_path_check = os.path.join(
            self.path, "files", "downloads", "screenshot", f"{game_id}"
        )
        screenshot_path = os.path.join(self.path, "files", "downloads", "screenshot")

        if os.path.exists(boxart_path_front) and os.path.exists(boxart_path_back):
            self.show_image(boxart_path_front)
            self.qcpc_input_output_text.setText(f"Boxart ya existen.")
            return

        if (
            os.path.exists(boxart_path_front)
            and os.path.exists(boxart_path_back)
            and os.path.exists(screenshot_path_check)
        ):
            self.qcpc_input_output_text.setText(f"Boxart y pantallazo ya existen.")
            return

        url = f"https://api.thegamesdb.net/v1/Games/Images?apikey={self.get_api_key()}&games_id={game_id}"
        request = requests.get(url)

        if request.status_code == 200:
            data = request.json()
            if data["data"]["count"] > 0:
                images = data["data"]["images"][str(game_id)]

                for image in images:
                    image_type = image["type"]
                    filename = image["filename"]

                    if image_type == "boxart":
                        image_side = image.get("side", "")
                        if image_side in ["front", "back"]:
                            image_path = os.path.join(
                                boxart_path, f"{game_id}_{image_side}_boxart.jpg"
                            )
                            image_url = f"{data['data']['base_url']['thumb']}boxart/{image_side}/{filename}"
                            self.download_image(
                                image_url, image_path, game_id, image_type, filename
                            )
                    elif image_type == "screenshot":
                        image_path = os.path.join(
                            screenshot_path, f"{game_id}_screenshot.jpg"
                        )
                        image_url = (
                            f"{data['data']['base_url']['thumb']}screenshots/{filename}"
                        )
                        self.download_image(
                            image_url, image_path, game_id, image_type, filename
                        )
                    else:
                        continue

                    image_url = f"{data['data']['base_url']['thumb']}{filename}"
                    self.download_image(
                        image_url, image_path, game_id, image_type, filename
                    )
            else:
                self.qcpc_input_output_text.setText(f"No hay imágenes disponibles.")
        else:
            self.qcpc_input_output_text.setText(
                f"Error en la petición REST: {request.status_code}"
            )

    def download_image(self, image_url, image_path, game_id, image_type, filename):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, "wb") as f:
                f.write(response.content)
            self.show_image(image_path)
            self.qcpc_input_output_text.setText(
                f"Imagen guardada para el ID del juego {game_id} ({image_type}) en {image_path}"
            )
        else:
            self.qcpc_input_output_text.setText(
                f"Fallo al descargar la imagen {image_type} para el ID del juego {game_id}"
            )

    def show_image(self, image_path):
        original_pixmap = QPixmap(image_path)
        scaled_width = int(original_pixmap.width() * 1.5)
        scaled_height = int(original_pixmap.height() * 1.5)
        scaled_pixmap = original_pixmap.scaled(scaled_width, scaled_height)
        self.qcpc_image_label.setPixmap(scaled_pixmap)
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)

    def guardar_seleccion(self):
        game_data = {
            "game_id": self.qcpc_form_editable.itemAt(0, QFormLayout.FieldRole)
            .widget()
            .text(),
            "game_title": self.game_title_input.text(),
            "release_date": self.release_date_input.text(),
            "platform": self.platform_input.text(),
            "developers": self.developer_input.text(),
        }

        developer_id = game_data.get("developer_id", None)
        if developer_id is None:
            developer_id = 10861
        game_id = game_data["game_id"]

        front_boxart_path = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
        )
        back_boxart_path = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_back_boxart.jpg"
        )
        screenshot_path = os.path.join(
            self.path, "files", "downloads", "screenshot", f"{game_id}_screenshot.jpg"
        )

        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()

        c.execute("""SELECT id FROM juegos WHERE id = ?""", (game_id,))
        existing_game = c.fetchone()

        if existing_game:
            self.qcpc_input_output_text.setText(
                f"El juego con ID {game_id} ya está en la base de datos."
            )
            conn.close()
            return

        # Verificar si los archivos existen y asignar None si no existen
        if os.path.exists(front_boxart_path):
            new_front_boxart_path = os.path.join(
                self.path, "files", "images", "boxart", f"{game_id}_front_boxart.jpg"
            )
            shutil.move(front_boxart_path, new_front_boxart_path)
        else:
            new_front_boxart_path = None

        if os.path.exists(back_boxart_path):
            new_back_boxart_path = os.path.join(
                self.path, "files", "images", "boxart", f"{game_id}_back_boxart.jpg"
            )
            shutil.move(back_boxart_path, new_back_boxart_path)
        else:
            new_back_boxart_path = None

        if os.path.exists(screenshot_path):
            new_screenshot_path = os.path.join(
                self.path, "files", "images", "screenshot", f"{game_id}_screenshot.jpg"
            )
            shutil.move(screenshot_path, new_screenshot_path)
        else:
            new_screenshot_path = None

        # Insertar los datos en la base de datos
        c.execute(
            """INSERT INTO juegos 
            (id, game_title, release_date, platform, region_id, country_id, developer_id, front_boxart_path, back_boxart_path, screenshot_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                game_id,
                game_data["game_title"] or None,  # Usar None si el campo está vacío
                game_data["release_date"] or None,
                game_data["platform"] or None,
                game_data.get("region_id", None),
                game_data.get("country_id", None),
                developer_id,
                new_front_boxart_path,
                new_back_boxart_path,
                new_screenshot_path,
            ),
        )

        conn.commit()
        conn.close()

        self.qcpc_input_output_text.setText(
            "Selección guardada correctamente en la base de datos."
        )
