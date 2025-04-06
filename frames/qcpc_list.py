from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import datetime
from httpx import delete, get
from openpyxl import Workbook
import os
import sqlite3
import pandas as pd
from .common import *
from .qcpc_form import qcpc_form
import os


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

    def __init__(self, parent=None):
        super(qcpc_list, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.resize(1100, 950)
        self.setMinimumSize(QSize(1100, 950))
        self.formLayout_2 = QFormLayout(self)
        self.formLayout_2.setObjectName("formLayout_2")

        self.setup_main_container()
        self.setup_attribute_list_frame()
        self.setup_image_frame()
        self.setup_text_frame()
        self.setup_button_frame()

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(
            0, QFormLayout.SpanningRole, self.qcpc_frame_container
        )

        # Traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)

        self.show_all_games()

    def setup_main_container(self):
        """Setup main container frame and layout"""
        self.qcpc_frame_container = QFrame(self)
        self.qcpc_frame_container.setObjectName("qcpc_frame_container")
        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)

        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.gridLayout_2.setObjectName("gridLayout_2")

    def setup_attribute_list_frame(self):
        """Setup attribute list frame and layout"""
        self.qcpc_attribute_table_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_attribute_table_frame.setObjectName("qcpc_attribute_table_frame")
        self.qcpc_attribute_table_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_attribute_table_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_attributes = QVBoxLayout(self.qcpc_attribute_table_frame)
        self.verticalLayout_attributes.setObjectName("verticalLayout_attributes")

        # Cambiar QListWidget por QTableView
        self.qcpc_attribute_table = QTableView(self.qcpc_attribute_table_frame)
        self.qcpc_attribute_table.setObjectName("qcpc_attribute_table")
        self.qcpc_attribute_table.setSelectionBehavior(QTableView.SelectRows)
        self.qcpc_attribute_table.setSelectionMode(QTableView.SingleSelection)
        self.qcpc_attribute_table.setEditTriggers(QTableView.NoEditTriggers)
        self.qcpc_attribute_table.horizontalHeader().setStretchLastSection(True)
        self.qcpc_attribute_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.verticalLayout_attributes.addWidget(self.qcpc_attribute_table)

        # Añadir el frame de la tabla al layout principal
        self.gridLayout_2.addWidget(
            self.qcpc_attribute_table_frame, 0, 0, 2, 1
        )  # 2 filas de altura # 2 filas de altura

    def setup_image_frame(self):
        """Setup image frame and layout"""
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
        self.qcpc_image_label.setMaximumSize(
            QSize(600, 750)
        )  # Ocupa la mitad de la altura del primer widget

        self.qcpc_image_label.setAlignment(Qt.AlignCenter)
        self.qcpc_image_layout.addWidget(self.qcpc_image_label)

        # Añadir el frame de la imagen al layout principal
        self.gridLayout_2.addWidget(self.qcpc_image_frame, 0, 1, 1, 1)

    def setup_text_frame(self):
        """Setup text frame and layout"""
        self.qcpc_text_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_text_frame.setObjectName("qcpc_text_frame")
        self.qcpc_text_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_text_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_text_layout = QVBoxLayout(self.qcpc_text_frame)
        self.qcpc_text_layout.setObjectName("qcpc_text_layout")
        self.qcpc_text_label = QTextBrowser(self.qcpc_text_frame)
        self.qcpc_text_label.setObjectName("qcpc_text_label")
        self.qcpc_text_label.setReadOnly(True)
        self.qcpc_text_layout.addWidget(self.qcpc_text_label)

        # Añadir el frame del texto al layout principal
        self.gridLayout_2.addWidget(self.qcpc_text_frame, 1, 1, 1, 1)

    def setup_button_frame(self):
        """Setup button frame and layout"""
        self.qcpc_button_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_button_frame.setObjectName("qcpc_button_frame")
        self.qcpc_button_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_button_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_button_layout = QHBoxLayout(self.qcpc_button_frame)
        self.qcpc_button_layout.setObjectName("qcpc_button_layout")

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
        self.qcpc_button_3.setText("Eliminar Entrada")
        self.qcpc_button_layout.addWidget(self.qcpc_button_3)

        self.qcpc_button_4 = QPushButton(self.qcpc_button_frame)
        self.qcpc_button_4.setObjectName("qcpc_button_4")
        self.qcpc_button_4.setText("Editar")
        self.qcpc_button_layout.addWidget(self.qcpc_button_4)

        # Añadir el frame de los botones al layout principal
        self.gridLayout_2.addWidget(
            self.qcpc_button_frame, 2, 0, 1, 2
        )  # Nueva fila que ocupa ambas columnas

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("qcpc_search", "Form", None))
        self.qcpc_attribute_table.setWindowTitle(
            QCoreApplication.translate("qcpc_search", "Atributos", None)
        )
        self.qcpc_image_label.setText(
            QCoreApplication.translate("qcpc_search", "Imagen", None)
        )
        self.qcpc_text_label.setPlaceholderText(
            QCoreApplication.translate("qcpc_search", "Resultados", None)
        )

    def setup_connections(self):
        # Conectar otros botones
        self.qcpc_button_1.clicked.connect(self.refresh_list)
        self.qcpc_button_2.clicked.connect(self.create_excel)
        self.qcpc_button_3.clicked.connect(self.delete_currentIndex)
        self.qcpc_button_4.clicked.connect(self.edit_currentIndex)
        self.qcpc_text_label.anchorClicked.connect(self.open_link)

    def handle_selection_change(self, selected, deselected):
        # Verificar si hay una selección
        if selected.indexes():
            index = selected.indexes()[0]  # Obtener el índice de la fila seleccionada
            model = self.qcpc_attribute_table.model()
            item_data = model.item(index.row(), 0).data(
                Qt.UserRole
            )  # Obtener los datos
            self.get_game_info(item_data)  # Mostrar la información del juego

    def display_message(self, message, message_type="info"):
        """
        Muestra un mensaje formateado en qcpc_text_label.

        :param message: El mensaje a mostrar.
        :param message_type: El tipo de mensaje (info, success, warning, error).
        """
        # Estilos según el tipo de mensaje
        style_classes = {
            "info": "info-box",
            "success": "success-box",
            "warning": "warning-box",
            "error": "error-box",
        }
        style_class = style_classes.get(message_type, "info-box")

        # Generar el HTML con el mensaje
        html_message = f"""
        {get_html_styles()}
        <div class="{style_class}">
            {message}
        </div>
        {get_html_footer()}
        """

        # Mostrar el mensaje en qcpc_text_label
        self.qcpc_text_label.setHtml(html_message)

    # Métodos de los botones

    def delete_currentIndex(self):
        currentIndex = self.qcpc_attribute_table.currentIndex()
        if currentIndex.isValid():  # Verificar si el índice es válido
            # Obtener los datos asociados al índice
            item_data = (
                currentIndex.model().item(currentIndex.row(), 0).data(Qt.UserRole)
            )
            if item_data:
                # Eliminar el registro de la base de datos
                self.delete_game(item_data)
                # Actualizar la lista después de eliminar
                self.refresh_list()
                self.display_message(
                    f"El juego con ID {item_data.get('id')} ha sido eliminado correctamente.",
                    "success",
                )
            else:
                self.display_message(
                    "No se encontraron datos para el elemento seleccionado.", "warning"
                )
        else:
            self.display_message("No se seleccionó ningún elemento.", "error")

    def delete_game(self, item_data):
        try:
            conn = sqlite3.connect(self.path_to_db)
            cursor = conn.cursor()

            # Eliminar las capturas de pantalla asociadas al juego
            cursor.execute(
                "DELETE FROM screenshots WHERE game_id = ?", (item_data.get("id"),)
            )

            # Eliminar el juego de la base de datos
            cursor.execute("DELETE FROM juegos WHERE id = ?", (item_data.get("id"),))

            conn.commit()

            if conn.total_changes > 0:
                self.display_message(
                    f"El juego con ID {item_data.get('id')} ha sido eliminado correctamente.",
                    "success",
                )
                self.refresh_list()
            else:
                self.display_message(
                    f"No se realizaron cambios al intentar eliminar el juego con ID {item_data.get('id')}.",
                    "warning",
                )

        except sqlite3.Error as e:
            self.display_message(f"Error de base de datos: {e}", "error")
        except Exception as e:
            self.display_message(f"Error general: {e}", "error")
        finally:
            conn.close()

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

            self.open_files()
            self.display_message(
                "El archivo Excel se ha creado correctamente.", "success"
            )

        except sqlite3.Error as e:
            self.display_message(f"Error de base de datos: {e}", "error")
        except Exception as e:
            self.display_message(f"Error general: {e}", "error")
        finally:
            conn.close()

    def edit_currentIndex(self):
        currentIndex = self.qcpc_attribute_table.currentIndex()
        if currentIndex.isValid():  # Verificar si el índice es válido
            # Obtener los datos asociados al índice
            item_data = (
                currentIndex.model().item(currentIndex.row(), 0).data(Qt.UserRole)
            )

            if item_data:
                # Abrir el formulario de edición con los datos del elemento seleccionado
                self.open_edit_form(item_data)
            else:
                self.display_message("No data found for the selected item")
        else:
            self.display_message("No item selected")

    def open_edit_form(self, item_data):
        self.edit_form = open_edit_form(
            parent=self, item_data=item_data, on_close=self.refresh_list
        )

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
                """ SELECT 
                    j.id,
                    j.game_title,
                    j.release_date,
                    j.platform,
                    j.region_id,
                    j.country_id,
                    j.developer_id,
                    j.front_boxart_path,
                    j.back_boxart_path,
                    j.url,
                    j.comentarios,
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

            # Crear el modelo para la tabla
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(
                [
                    "Título",
                    "Desarrollador",
                ]
            )

            # Añadir filas al modelo
            for row in rows:
                items = [
                    QStandardItem(row["game_title"]),
                    QStandardItem(row["developer_name"]),
                ]
                # Asociar datos adicionales al primer elemento de la fila
                items[0].setData(dict(row), Qt.UserRole)
                model.appendRow(items)

            # Asignar el modelo a la tabla
            self.qcpc_attribute_table.setModel(model)

            # Configurar el modelo de selección después de asignar el modelo
            selection_model = self.qcpc_attribute_table.selectionModel()
            if selection_model:
                selection_model.selectionChanged.connect(self.handle_selection_change)

        except sqlite3.Error as e:
            self.display_message(f"Database error: {e}")
        except Exception as e:
            self.display_message(f"General error: {e}")
        finally:
            conn.close()

    def get_game_info(self, item_data):
        # Reiniciar el índice de la imagen actual
        self.current_image_index = 0

        # Obtener las rutas de las imágenes
        image_paths = []

        # Verificar y agregar front_boxart_path si existe
        front_boxart_path = item_data.get("front_boxart_path", "")
        if front_boxart_path and os.path.exists(front_boxart_path):
            image_paths.append(front_boxart_path)

        # Verificar y agregar back_boxart_path si existe
        back_boxart_path = item_data.get("back_boxart_path", "")
        if back_boxart_path and os.path.exists(back_boxart_path):
            image_paths.append(back_boxart_path)

        # Obtener las rutas de las capturas de pantalla y agregarlas a la lista de rutas de imágenes
        screenshot_paths = item_data.get("screenshot_paths", "")
        if screenshot_paths:
            for path in screenshot_paths.split(","):
                if path and os.path.exists(
                    path
                ):  # Verificar que la ruta no esté vacía y que el archivo exista
                    image_paths.append(path)

        # Filtrar rutas vacías o inexistentes
        self.image_paths = image_paths

        if self.image_paths:
            # Iniciar el slideshow solo si no está ya en curso
            if not hasattr(self, "timer") or not self.timer.isActive():
                self.start_slideshow()
        else:
            self.display_message("No image paths found for this item", "warning")
            self.qcpc_image_label.clear()  # Limpiar la etiqueta de imagen si no hay imágenes

        # Mostrar la información del juego en el widget de texto
        game_info = get_html_styles()
        game_info += f"""
        <div class="summary-container">
        <table class="info-box">
        <tr>
        <td class="summary-label">Title:</td><td class='summary-section'>{item_data.get('game_title')}</td>
        </tr>
        <tr>
        <td class="summary-label">Release Date:</td><td class='summary-section'> {item_data.get('release_date')}</td>
        </tr>
        <tr>
        <td class="summary-label">Developer:</td><td class='summary-section'> {item_data.get('developer_name')}</td>        
        </tr>
        """
        web_url = item_data.get("url")
        comentarios = item_data.get("comentarios")

        if web_url:
            game_info += f'<tr><td class="summary-label">Web:</td><td class="summary-section"><a href="{web_url}">{web_url}</a></td></tr>'
        if comentarios:
            game_info += f'<tr><td class="summary-label"><b>Comentarios:</b></td><td class="summary-section">{comentarios}</td></tr>'
        game_info += "</table></div>" + get_html_footer()

        self.qcpc_text_label.setHtml(game_info)

    def refresh_list(self):
        model = self.qcpc_attribute_table.model()
        if model:
            model.removeRows(0, model.rowCount())  # Eliminar todas las filas del modelo
        self.show_all_games()  # Volver a cargar los datos

    def open_link(self, url: QUrl):
        QDesktopServices.openUrl(url)

    def start_slideshow(self):
        if self.image_paths:
            self.display_message(
                f"Starting slideshow with images: {self.image_paths}", "info"
            )
            self.current_image_index = 0
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.show_next_image)
            QTimer.singleShot(
                1000, self.show_next_image
            )  # Mostrar la primera imagen después de 1 segundo
            self.timer.start(3000)  # Cambiar de imagen cada 3 segundos
        else:
            self.display_message("No images available for slideshow", "warning")

    def show_next_image(self):
        if self.image_paths and 0 <= self.current_image_index < len(self.image_paths):
            image_path = self.image_paths[self.current_image_index]

            try:
                # Convertir la ruta a absoluta
                absolute_image_path = os.path.abspath(image_path)

                # Verificar si la imagen existe
                if not os.path.exists(absolute_image_path):
                    raise FileNotFoundError(f"Image not found: {absolute_image_path}")

                # Crear una imagen limpia sin metadatos
                image = QImage(absolute_image_path)
                if image.isNull():
                    raise ValueError(f"Failed to load image: {absolute_image_path}")

                # Crear una nueva imagen sin metadatos
                clean_image = QImage(
                    image.width(), image.height(), QImage.Format_ARGB32
                )
                clean_image.fill(Qt.transparent)

                # Pintar la imagen original en la nueva
                painter = QPainter(clean_image)
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setRenderHint(QPainter.SmoothPixmapTransform)
                painter.drawImage(0, 0, image)
                painter.end()

                # Convertir a QPixmap y escalar
                pixmap = QPixmap.fromImage(clean_image)
                scaled_pixmap = pixmap.scaled(
                    600, 750, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )

                # Mostrar la imagen procesada
                self.qcpc_image_label.setPixmap(scaled_pixmap)

            except Exception as e:
                self.display_message(str(e), "error")

            # Actualizar el índice para la siguiente imagen
            self.current_image_index = (self.current_image_index + 1) % len(
                self.image_paths
            )
        else:
            self.display_message("No valid image paths to display", "warning")
            self.qcpc_image_label.clear()
