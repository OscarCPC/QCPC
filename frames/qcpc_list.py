from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import datetime
from openpyxl import Workbook
import json
import os
import sqlite3
import pandas as pd
from .common import *
from .qcpc_form import qcpc_form


class qcpc_list(QWidget):
    path = os.getcwd()

    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        self.qcpc_attribute_list.setSelectionMode(QListWidget.SingleSelection)

        # Añadir el frame de la lista de atributos al layout principal
        self.gridLayout_2.addWidget(
            self.qcpc_attribute_list_frame, 0, 0, 2, 1
        )  # 2 filas de altura

        # Frame de la imagen (Widget 2)
        self.qcpc_image_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_image_frame.setObjectName("qcpc_image_frame")
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_image_layout = QVBoxLayout(self.qcpc_image_frame)
        self.qcpc_image_layout.setObjectName("qcpc_image_layout")
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName("qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(
            QSize(300, 450)
        )  # Ocupa la mitad de la altura del primer widget
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
        # self.qcpc_text_label = QTextEdit(self.qcpc_text_frame)
        self.qcpc_text_label = QTextBrowser(self.qcpc_text_frame)
        self.qcpc_text_label.setObjectName("qcpc_text_label")
        # self.qcpc_text_label.setOpenExternalLinks(True)
        self.qcpc_text_label.setReadOnly(True)
        self.qcpc_text_layout.addWidget(self.qcpc_text_label)

        # Frame de los botones (Nuevo Widget)
        self.qcpc_button_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_button_frame.setObjectName("qcpc_button_frame")
        self.qcpc_button_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_button_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_button_layout = QHBoxLayout(self.qcpc_button_frame)
        self.qcpc_button_layout.setObjectName("qcpc_button_layout")

        # Crear y añadir los botones al layout de los botones
        self.qcpc_button_1 = QPushButton(self.qcpc_button_frame)
        self.qcpc_button_1.setObjectName("qcpc_button_1")
        self.qcpc_button_1.setText("Actualizar Listado")
        self.qcpc_button_layout.addWidget(self.qcpc_button_1)

        self.qcpc_button_2 = QPushButton(self.qcpc_button_frame)
        self.qcpc_button_2.setObjectName("qcpc_button_2")
        self.qcpc_button_2.setText("Excel")
        self.qcpc_button_layout.addWidget(self.qcpc_button_2)

        self.qcpc_button_3 = QPushButton(self.qcpc_button_frame)
        self.qcpc_button_3.setObjectName("qcpc_button_3")
        self.qcpc_button_3.setText("Mostrar Archivos")
        self.qcpc_button_layout.addWidget(self.qcpc_button_3)

        self.qcpc_button_4 = QPushButton(self.qcpc_button_frame)
        self.qcpc_button_4.setObjectName("qcpc_button_4")
        self.qcpc_button_4.setText("Editar")
        self.qcpc_button_layout.addWidget(self.qcpc_button_4)

        # Añadir el frame de los botones al layout principal
        self.gridLayout_2.addWidget(
            self.qcpc_button_frame, 2, 0, 1, 2
        )  # Nueva fila que ocupa ambas columnas

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(
            0, QFormLayout.SpanningRole, self.qcpc_frame_container
        )

        # Añadir el frame del texto al layout principal
        self.gridLayout_2.addWidget(self.qcpc_text_frame, 1, 1, 1, 1)

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(
            0, QFormLayout.SpanningRole, self.qcpc_frame_container
        )

        # Traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)

        self.show_all_games()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("qcpc_search", "Form", None))
        self.qcpc_attribute_list.setWindowTitle(
            QCoreApplication.translate("qcpc_search", "Atributos", None)
        )
        self.qcpc_image_label.setText(
            QCoreApplication.translate("qcpc_search", "Imagen", None)
        )
        self.qcpc_text_label.setPlaceholderText(
            QCoreApplication.translate("qcpc_search", "Resultados", None)
        )

    def setup_connections(self):
        # Añadir conexiones de los botones aquí
        self.qcpc_button_1.clicked.connect(self.refresh_list)
        self.qcpc_button_2.clicked.connect(self.create_excel)
        self.qcpc_button_3.clicked.connect(self.open_files)
        self.qcpc_button_4.clicked.connect(self.edit_current_item)
        self.qcpc_text_label.anchorClicked.connect(
            self.open_link
        )  # Conectar la señal una vez

        # Conectar la señal itemClicked a la función handle_item_click
        self.qcpc_attribute_list.itemClicked.connect(self.get_game_info)
        self.qcpc_attribute_list.currentItemChanged.connect(
            self.handle_current_item_change
        )

        # Conectar la señal itemDoubleClicked a la función edit_current_item
        self.qcpc_attribute_list.itemDoubleClicked.connect(self.edit_current_item)

    def handle_current_item_change(self, current, previous):
        if current:
            self.get_game_info(current)

    # Métodos de los botones

    def create_excel(self):
        excel_path = os.path.join(
            self.path, "files", f"{self.current_date}_juegos.xlsx"
        )
        try:
            conn = sqlite3.connect(self.path_to_db)

            df = pd.read_sql_query(
                """ SELECT j.game_title,j.release_date,d.name,j.url,j.comentarios FROM  juegos j INNER JOIN developers d 
                                ON j.developer_id = d.id
                                ORDER BY j.game_title ASC
                                """,
                conn,
            )
            df.to_excel(excel_path, sheet_name="Juegos", index=False)

            clean_excel(excel_path)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            conn.close()

    def edit_current_item(self):
        current_item = self.qcpc_attribute_list.currentItem()
        if current_item:
            item_data = {
                "id": current_item.data(Qt.UserRole).get(
                    "id"
                ),  # Suponiendo que cada registro tiene un ID único
                "game_title": current_item.text(),  # Ajusta según la estructura de tu QListWidget
                "release_date": current_item.data(Qt.UserRole).get(
                    "release_date", "2000-01-01"
                ),
                "platform": current_item.data(Qt.UserRole).get("platform", ""),
                "region_id": current_item.data(Qt.UserRole).get("region_id", ""),
                "country_id": current_item.data(Qt.UserRole).get("country_id", ""),
                "developer_id": current_item.data(Qt.UserRole).get("developer_id", ""),
                "front_boxart_path": current_item.data(Qt.UserRole).get(
                    "front_boxart_path", ""
                ),
                "back_boxart_path": current_item.data(Qt.UserRole).get(
                    "back_boxart_path", ""
                ),
                "screenshot_path": current_item.data(Qt.UserRole).get(
                    "screenshot_path", ""
                ),
                "url": current_item.data(Qt.UserRole).get("url", ""),
                "comentarios": current_item.data(Qt.UserRole).get("comentarios", ""),
            }
            self.open_edit_form(item_data)
        else:
            print("No item selected")

    def open_edit_form(self, item_data):
        self.edit_form = qcpc_form()
        self.edit_form.setupUi()
        self.edit_form.load_data(item_data)
        self.edit_form.closed.connect(
            self.refresh_list
        )  # Conectar la señal closed a refresh_list
        self.edit_form.show()

    def open_files(self):
        open_file_folder(os.path.join(self.path, "files"))

    def show_all_games(self):
        try:
            conn = sqlite3.connect(self.path_to_db)
            conn.row_factory = (
                sqlite3.Row
            )  # Habilitar el acceso a las columnas por nombre
            c = conn.cursor()

            result = c.execute(
                """SELECT 
                    j.id,
                    j.game_title,
                    j.release_date,
                    j.platform,
                    j.region_id,
                    j.country_id,
                    j.developer_id,
                    j.front_boxart_path,
                    j.back_boxart_path,
                    d.name AS developer_name,
                    GROUP_CONCAT(s.screenshot_path) AS screenshot_paths
                FROM 
                    juegos j
                INNER JOIN 
                    developers d ON j.developer_id = d.id
                LEFT JOIN 
                    screenshots s ON j.id = s.game_id
                GROUP BY 
                    j.id
                ORDER BY 
                    j.game_title ASC"""
            )
            rows = result.fetchall()

            # Convertir a JSON
            rows_as_dict = [dict(row) for row in rows]

            # Convertir a JSON y luego deserializar para iterar sobre él
            json_result = json.dumps(rows_as_dict)
            data = json.loads(json_result)

            for item_data in data:
                title = QListWidgetItem(f"{item_data['game_title']}")
                title.setData(Qt.UserRole, item_data)
                self.qcpc_attribute_list.addItem(title)

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            conn.close()

    def get_game_info(self, item):
        # Obtener los datos del elemento clicado
        item_data = item.data(Qt.UserRole)

        # Obtener las rutas de las imágenes
        image_paths = [
            item_data.get("front_boxart_path", ""),
            item_data.get("back_boxart_path", ""),
        ]

        # Obtener las rutas de las capturas de pantalla y agregarlas a la lista de rutas de imágenes
        screenshot_paths = item_data.get("screenshot_paths", "")
        if screenshot_paths:
            image_paths.extend(screenshot_paths.split(","))

        # Filtrar rutas vacías
        self.image_paths = [path for path in image_paths if path and path != "null"]

        # Imprimir las rutas de las imágenes para depuración
        for i in self.image_paths:
            print(i)

        if self.image_paths:
            # Iniciar el slideshow solo si no está ya en curso
            if not hasattr(self, "timer") or not self.timer.isActive():
                self.start_slideshow()
        else:
            print("No image paths found for this item")

        # Mostrar la información del juego en el widget de texto
        game_info = f"""
        <style>
        body {{
            color: #0F0;
        }}
        a {{
            color: #0FF;
        }}
        b {{
            color: yellow;
        }}
        </style>
        <b>Title:</b> {item_data.get('game_title')}<br>
        <b>Release Date:</b> {item_data.get('release_date')}<br>
        <b>Developer:</b> {item_data.get('developer_name')}<br>
        """

        web_url = item_data.get("url")
        comentarios = item_data.get("comentarios")

        if web_url:
            game_info += f'<b>Web:</b> <a href="{web_url}">{web_url}</a>'
        if comentarios:
            game_info += f"<br><b>Comentarios:</b> {comentarios}"

        self.qcpc_text_label.setHtml(game_info)

    def refresh_list(self):
        self.qcpc_attribute_list.clear()
        self.show_all_games()

    def open_link(self, url: QUrl):
        QDesktopServices.openUrl(url)

    def start_slideshow(self):
        self.current_image_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)
        QTimer.singleShot(
            1000, self.show_next_image
        )  # Mostrar la primera imagen después de 1 segundo
        self.timer.start(5000)  # Cambiar de imagen cada 5 segundos

    def show_next_image(self):
        if self.image_paths:
            image_path = self.image_paths[self.current_image_index]
            pixmap = QPixmap(image_path)
            self.qcpc_image_label.setPixmap(pixmap)

            # Actualizar el índice para la siguiente imagen
            self.current_image_index = (self.current_image_index + 1) % len(
                self.image_paths
            )
