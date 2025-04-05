from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore
import json
import os
import shutil
import sqlite3
import pandas as pd
import qtawesome as qta
from .common import *


class qcpc_form(QWidget):
    # Configuración y rutas
    config = load_config()
    path = os.getcwd()
    path_to_db = os.path.join(path, "db", "qcpc.db")
    path_to_download = os.path.join(path, config["paths"]["path_to_download"])
    boxart_path = os.path.join(path, config["paths"]["boxart_path"])
    screenshot_path = os.path.join(path, config["paths"]["screenshot_path"])
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
        self.setup_animations()

    def create_label_with_icon(self, icon, text):
        """Crea una etiqueta con icono y texto integrados"""
        # Crear el layout principal
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        # Contenedor principal
        container = QWidget()
        container.setStyleSheet(
            f"""
            QWidget {{
                background-color: #202020;
                border-radius: 4px;
            }}
        """
        )

        # Contenedor para icono
        icon_container = QWidget()
        icon_container.setFixedWidth(50)  # Ancho fijo para el icono
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(5, 0, 5, 0)

        # Label para el icono
        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(20, 20))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)

        # Label para el texto
        text_label = QLabel(text)
        text_label.setStyleSheet(
            f"""
            color: {self.phosphor_green};            
            font-size: 12px;
            padding-right: 10px;
        """
        )

        # Añadir los elementos al layout principal
        layout.addWidget(icon_container)
        layout.addWidget(text_label)

        # Establecer el layout en el contenedor principal
        container.setLayout(layout)

        return container

    def setup_styles(self):
        """Configura los estilos de la aplicación"""
        self.phosphor_green = "#3AFF9E"
        self.dark_bg = "#1A1A1A"

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.dark_bg};
                color: {self.phosphor_green};                
                font-size: 12px;
            }}
            QFrame {{
                border: 2px solid {self.phosphor_green};
                border-radius: 4px;
                background-color: #202020;
            }}
            QPushButton {{
                background-color: #2A2A2A;
                border: 2px solid {self.phosphor_green};
                border-radius: 4px;
                color: {self.phosphor_green};
                padding: 8px;
                min-height: 30px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.phosphor_green};
                color: {self.dark_bg};
            }}
            QLineEdit, QTextEdit, QDateEdit, QComboBox {{
                background-color: #2A2A2A;
                border: 2px solid {self.phosphor_green};
                border-radius: 4px;
                color: {self.phosphor_green};
                padding: 5px;
                min-height: 25px;
            }}
            QLabel {{
                color: {self.phosphor_green};
                font-weight: bold;
                padding: 2px 5px;
            }}
            QTextBrowser {{
                background-color: #202020;
                border: 2px solid {self.phosphor_green};
                color: {self.phosphor_green};
                font-family: 'amstrad_cpc464';
                padding: 10px;
            }}
        """
        )

    def create_form_row(self, icon_name, label_text, widget, button=None):
        """Crea una fila del formulario con la etiqueta integrada"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear etiqueta con icono integrado
        icon = qta.icon(f"fa5s.{icon_name}", color=self.phosphor_green)
        label = self.create_label_with_icon(icon, label_text)

        # Configurar el widget de entrada
        widget.setMinimumWidth(300)  # Ancho mínimo para el campo de entrada

        # Añadir elementos al layout
        layout.addWidget(label)
        layout.addWidget(widget, 1)  # El 1 hace que el widget se expanda

        if button:
            button.setIcon(qta.icon("fa5s.folder-open", color=self.phosphor_green))
            button.setText(" Seleccionar")
            layout.addWidget(button)

        layout.addStretch()  # Añadir espacio flexible al final

        return layout

    def setup_form_fields(self):
        """Configura los campos del formulario"""
        current_row = 0

        # Título del juego
        self.game_title_input = QLineEdit(self.mainFrame)
        self.gridLayout.addLayout(
            self.create_form_row("gamepad", " Título", self.game_title_input),
            current_row,
            0,
            1,
            2,
        )

        # Año de lanzamiento
        current_row += 1
        self.release_date_input = QDateEdit(self.mainFrame)
        self.release_date_input.setDisplayFormat("yyyy")
        self.gridLayout.addLayout(
            self.create_form_row("calendar", " Año", self.release_date_input),
            current_row,
            0,
            1,
            2,
        )

        # Plataforma
        current_row += 1
        self.platform_input = QLineEdit(self.mainFrame)
        self.gridLayout.addLayout(
            self.create_form_row("desktop", " Plataforma", self.platform_input),
            current_row,
            0,
            1,
            2,
        )

        # Desarrollador
        current_row += 1
        self.developer_id_input = QComboBox(self.mainFrame)
        self.developer_id_input.setFixedHeight(40)
        self.developer_id_input.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.developer_id_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.gridLayout.addLayout(
            self.create_form_row("code", " Desarrollador", self.developer_id_input),
            current_row,
            0,
            1,
            2,
        )

        # Imágenes
        current_row += 1
        self.front_boxart_input = QLineEdit(self.mainFrame)
        self.front_boxart_button = QPushButton(self.mainFrame)
        self.front_boxart_button.clicked.connect(self.select_front_boxart_file)
        self.gridLayout.addLayout(
            self.create_form_row(
                "image",
                " Portada frontal",
                self.front_boxart_input,
                self.front_boxart_button,
            ),
            current_row,
            0,
            1,
            2,
        )

        current_row += 1
        self.back_boxart_input = QLineEdit(self.mainFrame)
        self.back_boxart_button = QPushButton(self.mainFrame)
        self.back_boxart_button.clicked.connect(self.select_back_boxart_file)
        self.gridLayout.addLayout(
            self.create_form_row(
                "image",
                " Portada trasera",
                self.back_boxart_input,
                self.back_boxart_button,
            ),
            current_row,
            0,
            1,
            2,
        )

        current_row += 1
        self.screenshot_input = QLineEdit(self.mainFrame)
        self.screenshot_button = QPushButton(self.mainFrame)
        self.screenshot_button.clicked.connect(self.select_screenshot_file)
        self.gridLayout.addLayout(
            self.create_form_row(
                "camera", " Capturas", self.screenshot_input, self.screenshot_button
            ),
            current_row,
            0,
            1,
            2,
        )

        # URL
        current_row += 1
        self.url_input = QLineEdit(self.mainFrame)
        self.gridLayout.addLayout(
            self.create_form_row("link", " URL", self.url_input), current_row, 0, 1, 2
        )

        # Comentarios
        current_row += 1
        self.comments_input = QTextEdit(self.mainFrame)
        self.gridLayout.addLayout(
            self.create_form_row("comment", " Comentarios", self.comments_input),
            current_row,
            0,
            1,
            2,
        )

        # Log
        current_row += 1
        self.info_output = QTextBrowser(self.mainFrame)
        self.info_output.setDisabled(True)
        self.gridLayout.addLayout(
            self.create_form_row("terminal", " Log", self.info_output),
            current_row,
            0,
            1,
            2,
        )

        return current_row

    def setup_buttons(self, current_row):
        """Configura los botones del formulario"""
        buttons_layout = QHBoxLayout()

        # Crear botones principales
        self.save_button = QPushButton(self.mainFrame)
        self.clear_button = QPushButton(self.mainFrame)
        self.cancel_button = QPushButton(self.mainFrame) if self.is_editing else None

        # Configurar textos e iconos según el modo
        if self.is_editing:
            self.save_button.setText(" Actualizar")
            self.save_button.setIcon(qta.icon("fa5s.save", color=self.phosphor_green))

            self.clear_button.setText(" Limpiar")
            self.clear_button.setIcon(qta.icon("fa5s.trash", color=self.phosphor_green))

            self.cancel_button.setText(" Cancelar")
            self.cancel_button.setIcon(
                qta.icon("fa5s.times", color=self.phosphor_green)
            )
        else:
            self.save_button.setText(" Guardar")
            self.save_button.setIcon(qta.icon("fa5s.save", color=self.phosphor_green))

            self.clear_button.setText(" Limpiar")
            self.clear_button.setIcon(qta.icon("fa5s.trash", color=self.phosphor_green))

        # Añadir botones al layout
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        if self.is_editing and self.cancel_button:
            buttons_layout.addWidget(self.cancel_button)

        self.gridLayout.addLayout(buttons_layout, current_row + 1, 0, 1, 2)

    def setupUi(self):
        """Configura la interfaz de usuario del formulario"""
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

        # Configurar estilos
        self.setup_styles()

        # Crear layout principal
        self.mainLayout = QGridLayout(self)
        self.mainFrame = QFrame(self)
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.mainFrame)

        # Configurar campos del formulario
        current_row = self.setup_form_fields()

        # Configurar botones
        self.setup_buttons(current_row)

        # Configuración final
        self.mainLayout.addWidget(self.mainFrame)
        self.gridLayout.setSpacing(15)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)

        # Inicialización final
        self.retranslateUi()
        self.setup_connections()
        self.populate_developer_combobox()

    def process_image(self, pixmap_or_path):
        """Pre-procesa la imagen convirtiéndola a JPG de forma agresiva para eliminar todos los metadatos"""
        try:
            if isinstance(pixmap_or_path, str):
                # Si es una ruta, cargar la imagen
                image = QImage(pixmap_or_path)
            else:
                # Si es un QPixmap, convertir a QImage
                image = pixmap_or_path.toImage()

            if image.isNull():
                return None

            # Crear una imagen limpia en formato RGB32
            clean_image = QImage(image.width(), image.height(), QImage.Format_RGB32)
            clean_image.fill(Qt.white)  # Fondo blanco para evitar transparencias

            # Pintar la imagen original en la nueva usando QPainter
            painter = QPainter(clean_image)
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.drawImage(0, 0, image)
            painter.end()

            # Convertir a JPG usando un buffer de memoria
            buffer = QBuffer()
            buffer.open(QBuffer.WriteOnly)

            # Forzar la conversión con parámetros específicos
            clean_image.save(buffer, "JPG", 95)

            # Crear una nueva imagen desde los datos JPG
            buffer.seek(0)
            final_image = QImage()
            final_image.loadFromData(buffer.data(), "JPG")

            # Convertir a QPixmap con comprobación final
            result = QPixmap.fromImage(final_image)

            if result.isNull():
                raise Exception("Error al convertir la imagen")

            return result

        except Exception as e:
            self.append_message(f"Error al procesar imagen: {str(e)}", "error")
            return None

    def create_animation(button):
        effect = QGraphicsOpacityEffect(button)
        button.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(200)
        animation.setStartValue(0.8)
        animation.setEndValue(1.0)
        return animation

    def populate_developer_combobox(self):
        for developer in self.get_developers():
            self.developer_id_input.addItem(developer[1], developer[0])

    def retranslateUi(self):
        self.setWindowTitle("Formulario de Edición/Adición")

    def setup_connections(self):
        """Configura las conexiones de señales"""
        # Eliminar esta línea ya que la conexión ya existe en setup_buttons
        self.save_button.clicked.connect(self.save_record)
        if self.is_editing:
            self.cancel_button.clicked.connect(self.close)
        self.clear_button.clicked.connect(
            self.clear_form
        )  # Limpiar el formulario # Cerrar el formulario

    def get_developers(self):
        try:
            conn = sqlite3.connect(self.path_to_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM developers order by name asc;")
            developers = cursor.fetchall()
            return developers
        except Exception as e:
            self.append_message("Error al obtener los desarrolladores")
            self.append_message(e)
        finally:
            conn.close()

    def load_data(self, item_data):
        # Cargar los datos en los campos del formulario
        self.game_title_input.setText(item_data.get("game_title", ""))
        release_date = item_data.get("release_date", "2000-01-01")
        if isinstance(release_date, int):  # Si es un entero, convertirlo a cadena
            release_date = f"{release_date}-01-01"
        self.release_date_input.setDate(QDate.fromString(release_date, "yyyy-MM-dd"))

        self.platform_input.setText(str(item_data.get("platform", "")))

        # Seleccionar el desarrollador correspondiente en el QComboBox
        developer_id = item_data.get("developer_id", "")
        self.append_message(f"Developer ID: {developer_id}")
        index = self.developer_id_input.findData(developer_id)  # Buscar por el ID
        if index != -1:
            self.developer_id_input.setCurrentIndex(index)
        else:
            self.developer_id_input.setCurrentIndex(
                0
            )  # Seleccionar el primer elemento si no se encuentra

        self.front_boxart_input.setText(item_data.get("front_boxart_path", ""))
        self.back_boxart_input.setText(item_data.get("back_boxart_path", ""))

        # Cargar screenshot_paths en el campo correspondiente
        screenshot_paths = item_data.get("screenshot_paths", "")
        if isinstance(screenshot_paths, list):
            screenshot_paths = ",".join(screenshot_paths)  # Convertir lista a cadena
        self.screenshot_input.setText(screenshot_paths)

        self.url_input.setText(item_data.get("url", ""))
        self.comments_input.setPlainText(item_data.get("comentarios", ""))

    def save_record(self):
        """Guarda o actualiza un registro en la base de datos"""
        try:
            # Recoger datos del formulario
            game_title = self.game_title_input.text()
            release_date = self.release_date_input.date().year()
            platform = self.platform_input.text()
            developer_id = self.developer_id_input.currentData()
            front_boxart_path = self.front_boxart_input.text()
            back_boxart_path = self.back_boxart_input.text()
            screenshot_paths = [
                path for path in self.screenshot_input.text().split(";") if path
            ]
            url = self.url_input.text()
            comentarios = self.comments_input.toPlainText()

            # Validaciones básicas
            if not game_title:
                self.append_message("El título del juego es obligatorio", "error")
                return False

            # Iniciar conexión
            conn = sqlite3.connect(self.path_to_db)
            cursor = conn.cursor()

            try:
                # Iniciar transacción
                conn.execute("BEGIN")

                if self.is_editing:
                    # Actualizar registro existente
                    cursor.execute(
                        """
                        UPDATE juegos 
                        SET game_title = ?, release_date = ?, platform = ?, 
                            developer_id = ?, front_boxart_path = ?, back_boxart_path = ?,
                            url = ?, comentarios = ?
                        WHERE id = ?
                    """,
                        (
                            game_title,
                            release_date,
                            platform,
                            developer_id,
                            front_boxart_path,
                            back_boxart_path,
                            url,
                            comentarios,
                            self.record_id,
                        ),
                    )

                    # Limpiar screenshots existentes
                    cursor.execute(
                        "DELETE FROM screenshots WHERE game_id = ?", (self.record_id,)
                    )
                else:
                    # Insertar nuevo registro
                    cursor.execute(
                        """
                        INSERT INTO juegos (
                            game_title, release_date, platform, developer_id,
                            front_boxart_path, back_boxart_path, url, comentarios
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            game_title,
                            release_date,
                            platform,
                            developer_id,
                            front_boxart_path,
                            back_boxart_path,
                            url,
                            comentarios,
                        ),
                    )

                    self.record_id = cursor.lastrowid

                # Insertar screenshots
                if screenshot_paths:
                    for path in screenshot_paths:
                        cursor.execute(
                            "INSERT INTO screenshots (game_id, screenshot_path) VALUES (?, ?)",
                            (self.record_id, path),
                        )

                # Confirmar transacción BD
                conn.commit()

                # Mover archivos
                if hasattr(self, "temp_front_boxart"):
                    shutil.move(
                        self.temp_front_boxart["origin"],
                        self.temp_front_boxart["destination"],
                    )

                if hasattr(self, "temp_back_boxart"):
                    shutil.move(
                        self.temp_back_boxart["origin"],
                        self.temp_back_boxart["destination"],
                    )

                if hasattr(self, "temp_screenshots"):
                    for screenshot in self.temp_screenshots:
                        shutil.move(screenshot["origin"], screenshot["destination"])

                self.append_message("Registro guardado correctamente", "success")

                # Limpiar variables temporales
                for attr in [
                    "temp_front_boxart",
                    "temp_back_boxart",
                    "temp_screenshots",
                ]:
                    if hasattr(self, attr):
                        delattr(self, attr)

                if self.is_editing:
                    self.close()

                return True

            except Exception as e:
                conn.rollback()
                self.append_message(f"Error: {str(e)}", "error")
                return False

            finally:
                conn.close()

        except Exception as e:
            self.append_message(f"Error crítico: {str(e)}", "error")
            return False

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
            # Procesar la imagen antes de guardarla
            if QImage(file_path).isNull():
                self.append_message("Archivo de imagen inválido", "error")
                return

            # Procesar la imagen
            processed_image = self.process_image(file_path)
            if not processed_image:
                self.append_message("Error al procesar la imagen", "error")
                return

            # Definir la ruta de destino
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_file_path = os.path.join(
                self.path, "files", "images", "boxart", f"{base_name}.jpg"
            )
            # Guardar las rutas para usarlas después
            self.temp_front_boxart = {"origin": file_path, "destination": new_file_path}
            # Mostrar la ruta relativa en el input
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
            # Procesar la imagen antes de guardarla
            if QImage(file_path).isNull():
                self.append_message("Archivo de imagen inválido", "error")
                return

            # Procesar la imagen
            processed_image = self.process_image(file_path)
            if not processed_image:
                self.append_message("Error al procesar la imagen", "error")
                return

            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_file_path = os.path.join(
                self.path, "files", "images", "boxart", f"{base_name}.jpg"
            )
            self.temp_back_boxart = {"origin": file_path, "destination": new_file_path}
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
            self.temp_screenshots = []
            relative_paths = []
            for file_path in files:
                # Procesar la imagen antes de guardarla
                if QImage(file_path).isNull():
                    self.append_message(
                        f"Archivo inválido: {os.path.basename(file_path)}", "error"
                    )
                    continue

                # Procesar la imagen
                processed_image = self.process_image(file_path)
                if not processed_image:
                    self.append_message(
                        f"Error al procesar: {os.path.basename(file_path)}", "error"
                    )
                    continue

                base_name = os.path.splitext(os.path.basename(file_path))[0]
                new_file_path = os.path.join(
                    self.path, "files", "images", "screenshot", f"{base_name}.jpg"
                )
                self.temp_screenshots.append(
                    {"origin": file_path, "destination": new_file_path}
                )
                relative_path = os.path.relpath(new_file_path, self.path)
                relative_paths.append(relative_path)

            if relative_paths:  # Solo actualizar si hay paths válidos
                self.screenshot_input.setText(";".join(relative_paths))

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def clear_form(self):
        """Limpia todos los campos del formulario."""
        self.game_title_input.clear()
        self.release_date_input.setDate(
            QDate.currentDate()
        )  # Restablecer a la fecha actual
        self.platform_input.clear()
        self.developer_id_input.setCurrentIndex(
            0
        )  # Seleccionar el primer elemento del QComboBox
        self.front_boxart_input.clear()
        self.back_boxart_input.clear()
        self.screenshot_input.clear()
        self.url_input.clear()
        self.comments_input.clear()

    def append_message(self, message, message_type="info"):
        """
        Añade un mensaje al QTextBrowser con formato HTML.
        :param message: El mensaje a mostrar.
        :param message_type: El tipo de mensaje ('info', 'error', 'success').
        """
        self.info_output.setDisabled(False)  # Habilitar el QTextBrowser
        self.info_output.clear()
        if message_type == "info":
            color = "blue"
        elif message_type == "error":
            color = "red"
        elif message_type == "success":
            color = "green"
        else:
            color = "black"

        # Obtener los estilos HTML
        html_styles = get_html_styles()
        html_footer = get_html_footer()

        # Formatear el mensaje con el color correspondiente
        formatted_message = f'<p style="color: {color};">{message}</p>'

        # Insertar el mensaje en el QTextBrowser
        self.info_output.setHtml(html_styles + formatted_message + html_footer)
        self.info_output.setDisabled(True)

    def setup_animations(self):
        """Configura las animaciones para los botones"""

        def create_animation(button):
            effect = QGraphicsOpacityEffect(button)
            button.setGraphicsEffect(effect)
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(200)
            animation.setStartValue(0.8)
            animation.setEndValue(1.0)
            return animation

        def create_hover_handler(animation, is_enter):
            def handler(event):
                if is_enter:
                    animation.setDirection(QAbstractAnimation.Forward)
                else:
                    animation.setDirection(QAbstractAnimation.Backward)
                animation.start()

            return handler

        if self.is_editing:
            for button in [self.save_button, self.clear_button, self.cancel_button]:
                anim = create_animation(button)
                button.enterEvent = create_hover_handler(anim, True)
                button.leaveEvent = create_hover_handler(anim, False)
        else:
            for button in [self.save_button, self.clear_button]:
                anim = create_animation(button)
                button.enterEvent = create_hover_handler(anim, True)
                button.leaveEvent = create_hover_handler(anim, False)
