from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import requests
import sqlite3
from .common import *


class qcpc_search(QWidget):
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

    def __init__(self, parent=None):
        super(qcpc_search, self).__init__(parent)
        self.setupUi()

    def setupUi(self):

        self.resize(1100, 950)

        self.setMinimumSize(QSize(1100, 950))
        self.formLayout_2 = QFormLayout(self)
        self.formLayout_2.setObjectName("formLayout_2")
        self.qcpc_frame_container = QFrame(self)
        self.qcpc_frame_container.setObjectName("qcpc_frame_container")

        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.qcpc_input_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_input_frame.setObjectName("qcpc_input_frame")

        self.qcpc_input_frame.setLayoutDirection(Qt.RightToLeft)
        self.qcpc_input_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_input_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_input_layout = QFormLayout(self.qcpc_input_frame)
        self.qcpc_input_layout.setObjectName("qcpc_input_layout")
        self.qcpc_input_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.qcpc_input_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.qcpc_input_layout.setLabelAlignment(Qt.AlignCenter)
        self.qcpc_input_label = QLabel(self.qcpc_input_frame)
        self.qcpc_input_label.setObjectName("qcpc_input_label")

        self.qcpc_input_label.setMinimumSize(QSize(250, 0))
        self.qcpc_input_label.setMaximumSize(QSize(16777215, 16777211))
        self.qcpc_input_label.setAlignment(Qt.AlignCenter)

        self.qcpc_input_layout.setWidget(
            0, QFormLayout.FieldRole, self.qcpc_input_label
        )

        self.qcpc_input_text = QPlainTextEdit(self.qcpc_input_frame)
        self.qcpc_input_text.setObjectName("qcpc_input_text")
        self.qcpc_input_text.setMinimumSize(QSize(275, 30))
        self.qcpc_input_text.setMaximumSize(QSize(16777215, 30))
        self.qcpc_input_text.installEventFilter(self)

        self.qcpc_input_layout.setWidget(1, QFormLayout.FieldRole, self.qcpc_input_text)

        self.qcpc_input_output_text = QTextEdit(self.qcpc_input_frame)
        self.qcpc_input_output_text.setObjectName("qcpc_input_output_text")
        self.qcpc_input_output_text.setReadOnly(True)

        # Agregar el formulario editable al layout

        self.qcpc_input_layout.setWidget(
            5, QFormLayout.FieldRole, self.qcpc_input_output_text
        )

        self.qcpc_inner_input_layout = QHBoxLayout()
        self.qcpc_inner_input_layout.setObjectName("qcpc_inner_input_layout")
        self.qcpc_input_frame_save = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_save.setObjectName("qcpc_input_frame_save")
        self.qcpc_input_frame_save.setMinimumSize(QSize(80, 30))
        self.qcpc_input_frame_save.setLayoutDirection(Qt.RightToLeft)

        self.qcpc_input_frame_edit = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_edit.setObjectName("qcpc_info_frame_edit")
        self.qcpc_input_frame_edit.setMinimumSize(QSize(80, 30))
        self.qcpc_input_frame_edit.setLayoutDirection(Qt.RightToLeft)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_save)
        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_edit)

        self.qcpc_input_frame_delete = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_delete.setObjectName("qcpc_input_frame_delete")

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_delete)

        self.qcpc_input_search = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_search.setObjectName("qcpc_input_search")
        self.qcpc_input_search.setMinimumSize(QSize(80, 30))
        self.qcpc_input_search.setMaximumSize(QSize(80, 30))
        self.qcpc_input_search.setLayoutDirection(Qt.LeftToRight)
        # Establecer el botón como el botón predeterminado para que se active con Enter
        self.qcpc_input_search.setDefault(True)
        # Establecer el acceso directo a Enter
        self.qcpc_input_search.setShortcut(Qt.Key_Return)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_search)

        self.qcpc_input_layout.setLayout(
            4, QFormLayout.SpanningRole, self.qcpc_inner_input_layout
        )

        self.qcpc_result_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_result_frame.setObjectName("qcpc_result_frame")

        self.qcpc_result_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_result_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.qcpc_result_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qcpc_result_table = QListWidget(self.qcpc_result_frame)
        self.qcpc_result_table.setObjectName("qcpc_result_table")

        self.verticalLayout.addWidget(self.qcpc_result_table)

        self.qcpc_result_label = QLabel(self.qcpc_result_frame)
        self.qcpc_result_label.setObjectName("qcpc_result_label")
        self.qcpc_result_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.qcpc_result_label)

        self.gridLayout_2.addWidget(self.qcpc_result_frame, 1, 0, 1, 1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.qcpc_frame_container)

        self.qcpc_image_frame = QFrame(self)
        self.qcpc_image_frame.setObjectName("qcpc_image_frame")

        self.qcpc_image_frame.setMinimumSize(QSize(600, 900))
        self.qcpc_image_frame.setMaximumSize(QSize(16777215, 16777215))

        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.qcpc_image_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName("qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(QSize(600, 900))
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)

        # self.qcpc_image_frame.setStyleSheet(u"background-color: rgba(170, 0, 0,0);")

        # self.horizontalLayout.addWidget(self.qcpc_image_label)
        self.set_grid_layout()
        self.retranslateUi(self)
        self.test_path()
        self.setup_connections()

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def set_grid_layout(self):
        # self.gridLayout_2.addWidget(self.qcpc_input_frame, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(
            self.qcpc_input_frame, 0, 0, 1, 1
        )  # Colocar en la primera columna y primera fila
        self.gridLayout_2.addWidget(
            self.qcpc_image_frame, 0, 1, 2, 1
        )  # Colocar en la segunda columna y primera fila, ocupando 2 filas de altura
        self.gridLayout_2.addWidget(
            self.qcpc_result_frame, 1, 0, 1, 1
        )  # Colocar en la primera columna y segunda fila

    def create_editable_form(self):
        # Aquí es donde se definirá el formulario editable
        self.qcpc_form_editable_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_form_editable_frame.setObjectName("qcpc_form_editable_frame")
        self.qcpc_form_editable_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_form_editable_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_form_editable_layout = QFormLayout(self.qcpc_form_editable_frame)
        self.qcpc_form_editable_layout.setObjectName("qcpc_form_editable_layout")
        self.gridLayout_2.addWidget(
            self.qcpc_form_editable_frame, 1, 1, 1, 1
        )  # Segunda columna, segunda fila
        self.gridLayout_2.addWidget(
            self.qcpc_image_frame, 0, 1, 1, 1
        )  # Segunda columna, primera fila, ocupa una fila

        selected_item = self.qcpc_result_table.currentItem()

        if selected_item is None:
            show_results(
                self.qcpc_input_output_text, "No hay ningún juego seleccionado."
            )
            return

        game_data = selected_item.data(Qt.UserRole)
        game_id = str(game_data["game_id"])
        # Añadir campos al formulario
        self.qcpc_form_editable_layout.addRow(
            "ID del Juego:", QLabel(str(game_data["game_id"]))
        )
        self.game_title_input = QLineEdit(str(game_data["game_title"]))
        self.qcpc_form_editable_layout.addRow("Título:", self.game_title_input)
        self.release_date_input = QLineEdit(str(game_data["release_date"]))
        self.qcpc_form_editable_layout.addRow(
            "Fecha de lanzamiento:", self.release_date_input
        )
        self.platform_input = QLineEdit(str(game_data["platform"]))
        self.qcpc_form_editable_layout.addRow("Plataforma:", self.platform_input)
        self.developer_input = QLineEdit(str(game_data["developers"]))
        self.qcpc_form_editable_layout.addRow("Desarrollador:", self.developer_input)

        self.qcpc_image_frame.setMinimumSize(QSize(600, 450))
        self.qcpc_image_frame.setMaximumSize(QSize(16777215, 16777215))
        self.qcpc_image_label.setMinimumSize(QSize(600, 450))
        self.qcpc_image_label.setMaximumSize(QSize(16777215, 16777215))

        # Forzar actualización del layout y el QLabel
        self.qcpc_image_frame.adjustSize()  # Asegurarse de que el frame redimensione sus hijos
        self.qcpc_image_label.adjustSize()  # Asegurar que el QLabel ajuste su tamaño
        self.qcpc_image_label.update()  # Forzar actualización visual del QLabel
        self.qcpc_image_frame.update()  # Forzar actualización visual

        QTimer.singleShot(0, lambda: self.update_image(game_id))

    def update_image(self, game_id):
        # Obtener el tamaño actualizado del QLabel
        label_width = self.qcpc_image_label.width()
        label_height = self.qcpc_image_label.height()

        front_boxart_path = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
        )

        if os.path.exists(front_boxart_path):
            self.show_image(front_boxart_path, label_width, label_height)

    def clear_editable_form(self):
        # Verificar si el formulario editable ya existe
        if hasattr(self, "qcpc_form_editable_frame") and self.qcpc_form_editable_frame:
            # Remover el widget del layout
            self.gridLayout_2.removeWidget(self.qcpc_form_editable_frame)

            # Eliminar todos los widgets dentro del formulario editable
            for i in reversed(range(self.qcpc_form_editable_layout.count())):
                widget = self.qcpc_form_editable_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Eliminar el marco del formulario editable
            self.qcpc_form_editable_frame.deleteLater()
            self.qcpc_form_editable_frame = None

    def add_action_buttons(self):
        # Crear botones y añadirlos al QTextEdit
        self.save_button = QPushButton("Guardar")
        self.select_button = QPushButton("Seleccionar")
        self.edit_button = QPushButton("Editar")

        # Añadir botones al QTextEdit
        cursor = self.qcpc_input_output_text.textCursor()
        cursor.movePosition(cursor.End)

        self.qcpc_input_output_text.setTextCursor(cursor)
        self.qcpc_input_output_text.insertPlainText("\n\n")

        self.qcpc_input_output_text.append("Seleccione una acción:")
        self.qcpc_input_output_text.append(" ")

        self.qcpc_input_output_text.setAlignment(Qt.AlignCenter)

        self.qcpc_input_output_text.setAlignment(Qt.AlignLeft)

        self.qcpc_input_output_text.insertWidget(cursor, self.select_button)
        self.qcpc_input_output_text.insertWidget(cursor, self.edit_button)
        self.qcpc_input_output_text.insertWidget(cursor, self.save_button)

        # Conectar los botones a sus respectivas funciones
        self.select_button.clicked.connect(self.select_data)
        self.edit_button.clicked.connect(self.edit_data)
        self.save_button.clicked.connect(self.save_data)

    def retranslateUi(self, qcpc_search):
        qcpc_search.setWindowTitle(
            QCoreApplication.translate("qcpc_search", "Form", None)
        )
        self.qcpc_result_label.setText(
            QCoreApplication.translate("qcpc_search", "Resultados", None)
        )
        self.qcpc_input_label.setText(
            QCoreApplication.translate("qcpc_search", "Titulo a buscar", None)
        )
        self.qcpc_input_frame_save.setText(
            QCoreApplication.translate("qcpc_search", "Guardar Selecci\u00f3n", None)
        )
        self.qcpc_input_frame_delete.setText(
            QCoreApplication.translate("qcpc_search", "Borrar", None)
        )
        self.qcpc_input_frame_edit.setText(
            QCoreApplication.translate("qcpc_search", "Editar", None)
        )
        self.qcpc_input_search.setText(
            QCoreApplication.translate("qcpc_search", "Buscar", None)
        )

    # retranslateUi

    def setup_connections(self):
        self.qcpc_input_search.clicked.connect(self.get_game)
        self.qcpc_result_table.itemClicked.connect(self.show_game_image)
        self.qcpc_input_frame_delete.clicked.connect(
            lambda: self.qcpc_input_text.clear()
        )
        self.qcpc_input_frame_save.clicked.connect(self.guardar_seleccion)
        self.qcpc_input_frame_edit.clicked.connect(self.create_editable_form)

    def eventFilter(self, source, event):
        if source is self.qcpc_input_text and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.qcpc_input_search.click()  # Simular clic en el botón
            elif (
                event.key() == Qt.Key_Escape
            ):  # Si se presiona Escape, limpiar el texto
                self.qcpc_input_text.clear()
        else:
            # Llamar a la implementación original del evento para mantener el comportamiento predeterminado
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
        self.clear_editable_form()
        self.set_grid_layout()
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
            self.qcpc_result_table.clear()  # Clear existing items
            if "data" in data and "games" in data["data"] and data["data"]["games"]:
                for game in data["data"]["games"]:
                    game_id = game["id"]
                    game_title = game["game_title"]
                    release_date = game["release_date"][:4]  # Extraer solo el año
                    platform = game["platform"]
                    region_id = game["region_id"]
                    country_id = game["country_id"]
                    developer_id = developer_id = (
                        game["developers"][0] if game["developers"] else None
                    )  # Tomar el primer valor de la lista de desarrolladores si existe

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
                        "developers": developer_name,
                    }

                    item = QListWidgetItem(
                        f"{game_title} - {release_date} -  Desarrollador: {developer_name}"
                    )
                    item.setData(Qt.UserRole, game_data)
                    self.qcpc_result_table.addItem(item)
            else:
                # Show message if no results were found
                self.qcpc_result_table.addItem("No se han encontrado resultados")

        else:
            show_results(
                self.qcpc_input_output_text,
                "Error en la petición REST:",
                request.status_code,
            )

    def get_developer_name(self, developer_id):
        # Conectar a la base de datos
        if developer_id is None:
            return "Desconocido"
        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()

        # Buscar el nombre del desarrollador por su ID en la tabla de desarrolladores
        c.execute("SELECT name FROM developers WHERE id = ?", (developer_id,))
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
        # Definir las rutas de las imágenes
        boxart_path_front = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
        )
        boxart_path_back = os.path.join(
            self.path, "files", "downloads", "boxart", f"{game_id}_back_boxart.jpg"
        )
        screenshot_dir = os.path.join(
            self.path, "files", "downloads", "screenshot", f"{game_id}"
        )

        # Crear la carpeta de capturas de pantalla si no existe
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Comprobar si el boxart ya existe y mostrarlo si es el caso
        if os.path.exists(boxart_path_front) and os.path.exists(boxart_path_back):
            self.show_image(boxart_path_front)
            show_results(self.qcpc_input_output_text, f"El boxart ya existe.")
            return

        # Comprobar si el boxart y la captura de pantalla ya existen
        if (
            os.path.exists(boxart_path_front)
            and os.path.exists(boxart_path_back)
            and os.path.exists(screenshot_dir)
        ):
            show_results(
                self.qcpc_input_output_text,
                f"El boxart y la captura de pantalla ya existen.",
            )
            return

        # Realizar la solicitud a la API para obtener las imágenes
        url = f"https://api.thegamesdb.net/v1/Games/Images?apikey={self.get_api_key()}&games_id={game_id}"
        request = requests.get(url)

        if request.status_code == 200:
            data = request.json()

            # Verificar que haya imágenes disponibles
            if data["data"]["count"] > 0:
                images = data["data"]["images"].get(str(game_id), [])
                base_url_thumb = data["data"]["base_url"]["thumb"]

                # Procesar las imágenes recibidas
                for image in images:
                    image_type = image.get("type")
                    filename = image.get("filename")

                    if not image_type or not filename:
                        continue  # Si faltan datos, pasar a la siguiente imagen

                    # Procesar las imágenes de tipo 'boxart'
                    if image_type == "boxart":
                        image_side = image.get("side", "")
                        if image_side == "front":
                            image_path = boxart_path_front
                        elif image_side == "back":
                            image_path = boxart_path_back
                        else:
                            continue  # Si no es ni 'front' ni 'back', continuar con la siguiente imagen

                        # Descargar la imagen si no existe, de lo contrario, mostrarla
                        if not os.path.exists(image_path):
                            image_url = f"{base_url_thumb}{filename}"
                            self.download_image(
                                image_url, image_path, game_id, image_type, filename
                            )
                        else:
                            self.show_image(image_path)

                    # Procesar las capturas de pantalla (aquí se puede agregar más lógica si fuera necesario)
                    elif image_type == "screenshot":
                        screenshot_path = os.path.join(screenshot_dir, filename)
                        if not os.path.exists(screenshot_path):
                            image_url = f"{base_url_thumb}{filename}"
                            self.download_image(
                                image_url,
                                screenshot_path,
                                game_id,
                                image_type,
                                filename,
                            )

            else:
                show_results(
                    self.qcpc_input_output_text, "No hay imágenes disponibles."
                )
        else:
            show_results(
                self.qcpc_input_output_text,
                f"Error en la petición REST: {request.status_code}",
            )

    def download_image(self, image_url, image_path, game_id, image_type, filename):
        # Crear la carpeta de destino si no existe
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, "wb") as f:
                f.write(response.content)
            self.show_image(image_path)
            show_results(
                self.qcpc_input_output_text,
                f"Imagen guardada para el ID del juego {game_id} ({image_type}) en {image_path}",
            )
        else:
            show_results(
                self.qcpc_input_output_text,
                f"Fallo al descargar la imagen {image_type} para el ID del juego {game_id}",
            )

    def show_image(self, image_path, label_width=None, label_height=None):
        # Cargar la imagen en un QPixmap
        pixmap = QPixmap(image_path)

        # Obtener el tamaño del QLabel donde se mostrará la imagen si no se proporciona
        if label_height is None and label_width is None:
            label_width = self.qcpc_image_label.width()
            label_height = self.qcpc_image_label.height()

        # Escalar la imagen al tamaño del QLabel, manteniendo la proporción
        scaled_pixmap = pixmap.scaled(
            label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # Mostrar la imagen escalada
        self.qcpc_image_label.setPixmap(scaled_pixmap)
        self.qcpc_image_label.setAlignment(
            Qt.AlignCenter
        )  # Centrar la imagen en el QLabel

        # Forzar la actualización del QLabel para asegurar que la imagen se dibuje correctamente
        self.qcpc_image_label.update()

    def guardar_seleccion(self):
        # Obtener el elemento seleccionado en la tabla de resultados
        selected_item = self.qcpc_result_table.currentItem()

        # Verificar si hay un juego seleccionado
        if selected_item is None:
            show_results(
                self.qcpc_input_output_text, "No hay ningún juego seleccionado."
            )
            return

        # Obtener los datos del juego seleccionado
        game_data = selected_item.data(Qt.UserRole)

        # Obtener el ID del desarrollador del juego
        developer_id = game_data.get("developer_id")

        # Verificar si el juego tiene un desarrollador asociado
        if developer_id is None:
            # Asignar el ID 10861 al desarrollador si no tiene uno asociado
            developer_id = 10861
        game_id = game_data["game_id"]

        # Definir las rutas de las imágenes
        front_boxart_path = None
        back_boxart_path = None
        screenshot_paths = []

        # Verificar si existen las imágenes de portada frontal y trasera
        if os.path.exists(
            os.path.join(
                self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
            )
        ):
            front_boxart_path = os.path.join(
                self.path, "files", "downloads", "boxart", f"{game_id}_front_boxart.jpg"
            )
        if os.path.exists(
            os.path.join(
                self.path, "files", "downloads", "boxart", f"{game_id}_back_boxart.jpg"
            )
        ):
            back_boxart_path = os.path.join(
                self.path, "files", "downloads", "boxart", f"{game_id}_back_boxart.jpg"
            )

        # Verificar si existen capturas de pantalla y agregarlas a la lista
        screenshot_dir = os.path.join(
            self.path, "files", "downloads", "screenshot", f"{game_id}", "screenshots"
        )
        if os.path.exists(screenshot_dir):
            for file_name in os.listdir(screenshot_dir):
                screenshot_paths.append(os.path.join(screenshot_dir, file_name))

        # Conectar a la base de datos
        conn = sqlite3.connect(self.path_to_db)
        c = conn.cursor()

        # Verificar si el game_id ya existe en la tabla juegos
        c.execute("""SELECT id FROM juegos WHERE id = ?""", (game_id,))
        existing_game = c.fetchone()

        # Si ya existe un registro con el mismo game_id, mostrar un mensaje y salir de la función
        if existing_game:
            show_results(
                self.qcpc_input_output_text,
                f"El juego con ID {game_id} ya está en la base de datos.",
            )
            conn.close()
            return

        # Mover las imágenes de portada a la carpeta de imágenes y obtener las rutas relativas
        if front_boxart_path:
            new_front_boxart_path = os.path.join(
                self.path, "files", "images", "boxart", f"{game_id}_front_boxart.jpg"
            )
            shutil.move(front_boxart_path, new_front_boxart_path)
            relative_front_boxart_path = os.path.relpath(
                new_front_boxart_path, self.path
            )
        else:
            relative_front_boxart_path = "null"
        if back_boxart_path:
            new_back_boxart_path = os.path.join(
                self.path, "files", "images", "boxart", f"{game_id}_back_boxart.jpg"
            )
            shutil.move(back_boxart_path, new_back_boxart_path)
            relative_back_boxart_path = os.path.relpath(new_back_boxart_path, self.path)
        else:
            relative_back_boxart_path = "null"

        # Insertar los datos del juego en la tabla juegos
        c.execute(
            """INSERT INTO juegos 
            (id, game_title, release_date, platform, region_id, country_id, developer_id, front_boxart_path, back_boxart_path) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                game_id,
                game_data["game_title"],
                game_data["release_date"],
                game_data["platform"],
                game_data["region_id"],
                game_data["country_id"],
                developer_id,
                relative_front_boxart_path,
                relative_back_boxart_path,
            ),
        )

        # Mover las capturas de pantalla a la carpeta de imágenes y obtener las rutas relativas
        for screenshot_path in screenshot_paths:
            new_screenshot_path = os.path.join(
                self.path,
                "files",
                "images",
                "screenshot",
                os.path.basename(screenshot_path),
            )
            shutil.move(screenshot_path, new_screenshot_path)
            relative_screenshot_path = os.path.relpath(new_screenshot_path, self.path)
            c.execute(
                """INSERT INTO screenshots (game_id, screenshot_path) VALUES (?, ?)""",
                (game_id, relative_screenshot_path),
            )

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Mostrar mensaje de éxito
        show_results(
            self.qcpc_input_output_text,
            "Selección guardada correctamente en la base de datos.",
        )
