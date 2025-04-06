from contextlib import contextmanager
from typing import Optional, Set
from pathlib import Path
import shutil
import sqlite3
import requests
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome as qta
from .common import *
from .qcpc_form import qcpc_form
from .config.base_config import QCPCConfig


class qcpc_search(QWidget):
    def __init__(self, parent=None):
        super(qcpc_search, self).__init__(parent)
        self.project_root = Path(__file__).parent.parent.absolute()
        self.config = QCPCConfig.from_json()
        self.setupUi()

    def test_path(self):
        """Verificar y crear directorios necesarios"""
        paths = [
            self.config.get_path("path_to_download"),
            self.config.get_path("boxart_path"),
            self.config.get_path("screenshot_path"),
            self.config.get_path("path_to_image"),
            self.config.get_path("boxart_path_images"),
            self.config.get_path("screenshot_path_images"),
        ]
        for path in paths:
            if not path.exists():
                path.mkdir(parents=True)

    def _get_absolute_path(self, path: Path) -> Path:
        """Convierte una ruta relativa en absoluta"""
        if path.is_absolute():
            return path
        return self.project_root / path

    def get_api_key(self):
        """Obtener API key de la configuración"""
        return self.config.api_key

    def setupUi(self):
        # Frame contenedor principal que recibirá la imagen de fondo
        self.main_container = QFrame(self)
        self.main_container.setObjectName("body_widget")

        # Layout principal que contiene el frame principal
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.main_container)

        # Layout para el contenido dentro del frame principal
        main_layout = QVBoxLayout(self.main_container)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Configuración inicial del widget
        self.resize(1100, 950)
        self.setMinimumSize(QSize(1100, 950))

        # Header con búsqueda
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_frame.setMaximumHeight(80)  # Limitar la altura del frame de búsqueda
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(10, 5, 10, 5)  # Reducir márgenes

        # Campo de búsqueda con icono
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_container_layout = QHBoxLayout(search_container)
        search_container_layout.setContentsMargins(5, 0, 5, 0)

        search_icon = QLabel()
        search_icon.setPixmap(qta.icon("fa5s.search", color="yellow").pixmap(16, 16))

        self.qcpc_input_text = QLineEdit()
        self.qcpc_input_text.setPlaceholderText("Buscar juego...")
        self.qcpc_input_text.setMinimumHeight(30)  # Reducir altura mínima
        self.qcpc_input_text.setMaximumHeight(30)  # Asegurar altura máxima
        self.qcpc_input_text.setObjectName("qcpc_input_text")
        self.qcpc_input_text.installEventFilter(self)

        search_container_layout.addWidget(search_icon)
        search_container_layout.addWidget(self.qcpc_input_text)

        # Botones de acción
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)

        self.qcpc_input_search = QPushButton("Buscar")
        self.qcpc_input_frame_clean = QPushButton("Limpiar")

        for button in [self.qcpc_input_search, self.qcpc_input_frame_clean]:
            button.setMinimumHeight(35)
            button.setCursor(Qt.PointingHandCursor)

        buttons_layout.addWidget(self.qcpc_input_search)
        buttons_layout.addWidget(self.qcpc_input_frame_clean)

        search_layout.addWidget(search_container, 1)
        search_layout.addWidget(buttons_container)

        # Contenedor principal split
        content_splitter = QSplitter(Qt.Horizontal)

        # Panel izquierdo: Resultados y acciones
        left_panel = QFrame()
        left_panel.setObjectName("qcpc_search_frame_container")
        left_layout = QVBoxLayout(left_panel)

        # Etiqueta de resultados
        self.qcpc_result_label = QLabel("Resultados")
        self.qcpc_result_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.qcpc_result_label)

        # Lista de resultados
        self.qcpc_result_table = QListWidget()
        self.qcpc_result_table.setObjectName("qcpc_result_table")

        # Panel de acciones
        actions_panel = QFrame()
        actions_layout = QHBoxLayout(actions_panel)

        self.qcpc_input_frame_save = QPushButton("Guardar")
        self.qcpc_input_frame_edit = QPushButton("Editar")
        self.qcpc_input_frame_delete = QPushButton("Eliminar")

        for button in [
            self.qcpc_input_frame_save,
            self.qcpc_input_frame_edit,
            self.qcpc_input_frame_delete,
        ]:
            actions_layout.addWidget(button)

        left_layout.addWidget(self.qcpc_result_table)
        left_layout.addWidget(actions_panel)

        # Panel derecho: Visualización de imagen
        self.qcpc_image_frame = QFrame()
        self.qcpc_image_frame.setObjectName("qcpc_image_frame")

        # Crear scroll area para la imagen
        image_scroll = QScrollArea()
        image_scroll.setWidgetResizable(True)
        image_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        image_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        image_scroll.setObjectName("image_scroll_area")

        # Container para la imagen dentro del scroll area
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(8, 8, 8, 8)
        image_layout.setAlignment(Qt.AlignCenter)

        self.qcpc_image_label = QLabel()
        self.qcpc_image_label.setObjectName("qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(QSize(600, 900))
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)

        image_layout.addWidget(self.qcpc_image_label)
        image_scroll.setWidget(image_container)

        # Layout principal del frame de imagen
        main_image_layout = QVBoxLayout(self.qcpc_image_frame)
        main_image_layout.setContentsMargins(0, 0, 0, 0)
        main_image_layout.addWidget(image_scroll)

        # Ajustar el splitter
        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(self.qcpc_image_frame)
        content_splitter.setStretchFactor(0, 40)
        content_splitter.setStretchFactor(1, 60)

        # Añadir espacio entre los paneles
        content_splitter.setHandleWidth(10)

        # Área de mensajes/output
        self.qcpc_input_output_text = QTextEdit()
        self.qcpc_input_output_text.setObjectName("qcpc_input_output_text")
        self.qcpc_input_output_text.setMaximumHeight(100)

        # Añadir todo al layout principal
        main_layout.addWidget(search_frame)
        main_layout.addWidget(content_splitter)
        main_layout.addWidget(self.qcpc_input_output_text)

        # Verificar y crear directorios necesarios
        self.test_path()

        # Configurar conexiones
        self.setup_connections()

        # Traducir textos
        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    @contextmanager
    def get_db_connection(self):
        """Context manager para conexiones a BD"""
        conn = None
        try:
            conn = sqlite3.connect(self.config.db_path)
            yield conn
        finally:
            if conn:
                conn.close()

    def create_editable_form(self):
        """Crea y muestra el formulario de edición"""
        try:
            selected_item = self.qcpc_result_table.currentItem()
            if not selected_item:
                show_results(
                    self.qcpc_input_output_text, "No hay ningún juego seleccionado."
                )
                return

            game_data = selected_item.data(Qt.UserRole)
            if not game_data:
                show_results(
                    self.qcpc_input_output_text,
                    "Datos del juego inválidos o incompletos.",
                )
                return

            # Remove the on_close parameter since we don't need refresh_list
            self.edit_form = open_edit_form(parent=self, item_data=game_data)

        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error creando formulario: {str(e)}"
            )

    def update_image(self, game_id: int):
        """Actualiza la imagen mostrada para un juego específico"""
        # Obtener el tamaño actualizado del QLabel
        label_width = self.qcpc_image_label.width()
        label_height = self.qcpc_image_label.height()

        front_boxart_path = (
            self.config.get_path("boxart_path") / f"{game_id}_front_boxart.jpg"
        )

        if front_boxart_path.exists():
            self.show_image(str(front_boxart_path), label_width, label_height)

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
        self.qcpc_input_frame_clean.setText(
            QCoreApplication.translate("qcpc_search", "Limpiar imágenes", None)
        )

    # retranslateUi

    def setup_connections(self):
        """Configura las conexiones de señales y slots"""
        # Búsqueda
        self.qcpc_input_search.clicked.connect(self.get_game)

        # Visualización
        self.qcpc_result_table.itemClicked.connect(self.show_game_image)

        # Gestión
        self.qcpc_input_frame_save.clicked.connect(self.guardar_seleccion)
        self.qcpc_input_frame_edit.clicked.connect(self.create_editable_form)

        # Limpieza
        self.qcpc_input_frame_delete.clicked.connect(self.clear_search)
        self.qcpc_input_frame_clean.clicked.connect(self.clean_unused_images)

    def clear_search(self):
        """Limpia todos los elementos de la interfaz"""
        self.qcpc_input_text.clear()
        self.qcpc_result_table.clear()
        self.qcpc_image_label.clear()
        self.clear_editable_form()
        show_results(self.qcpc_input_output_text, "Búsqueda limpiada")

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """Maneja eventos personalizados"""
        if source is self.qcpc_input_text:
            if event.type() == QEvent.KeyPress:
                key = event.key()
                if key in (Qt.Key_Return, Qt.Key_Enter):
                    self.qcpc_input_search.click()
                    return True
                elif key == Qt.Key_Escape:
                    self.clear_search()
                    return True

        return super().eventFilter(source, event)

    def clear_editable_form(self):
        """Limpia el formulario editable si existe"""
        try:
            if hasattr(self, "edit_form"):
                self.edit_form.close()
                delattr(self, "edit_form")
        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error limpiando formulario: {str(e)}"
            )

    def get_game(self):
        """Realiza la búsqueda de juegos"""
        try:
            search_text = self.qcpc_input_text.text().strip()

            if not search_text:
                show_results(
                    self.qcpc_input_output_text,
                    "Por favor ingrese un texto para buscar",
                )
                return

            self.clear_editable_form()
            self.qcpc_result_table.clear()
            self.qcpc_image_label.clear()

            url_base = "https://api.thegamesdb.net/v1/Games/ByGameName"
            params = {
                "apikey": self.get_api_key(),
                "name": search_text,
                "filter[platform]": "4914",
            }

            with requests.get(url_base, params=params, timeout=10) as response:
                response.raise_for_status()
                data = response.json()

                if not data.get("data", {}).get("games"):
                    self.qcpc_result_table.addItem("No se han encontrado resultados")
                    return

                for game in data["data"]["games"]:
                    try:
                        game_data = {
                            "game_id": game.get("id"),
                            "game_title": game.get("game_title", "Sin título"),
                            "release_date": (
                                game.get("release_date", "")[:4]
                                if game.get("release_date")
                                else "????"
                            ),
                            "platform": game.get("platform"),
                            "region_id": game.get("region_id"),
                            "country_id": game.get("country_id"),
                            "developer_id": game.get("developers", [None])[0],
                        }

                        # Obtener el nombre del desarrollador
                        developer_name = self.get_developer_name(
                            game_data["developer_id"]
                        )
                        game_data["developers"] = developer_name

                        # Crear item para la lista
                        item = QListWidgetItem(
                            f"{game_data['game_title']} - {game_data['release_date']} - Desarrollador: {developer_name}"
                        )
                        item.setData(Qt.UserRole, game_data)
                        self.qcpc_result_table.addItem(item)

                    except Exception as e:
                        show_results(
                            self.qcpc_input_output_text,
                            f"Error procesando juego: {str(e)}",
                        )
                        continue

        except requests.RequestException as e:
            show_results(
                self.qcpc_input_output_text, f"Error en la petición REST: {str(e)}"
            )
        except Exception as e:
            show_results(self.qcpc_input_output_text, f"Error inesperado: {str(e)}")

    def get_developer_name(self, developer_id):
        """Obtiene el nombre del desarrollador desde la base de datos"""
        if developer_id is None:
            return "Desconocido"

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM developers WHERE id = ?", (developer_id,)
                )
                developer_name = cursor.fetchone()
                return developer_name[0] if developer_name else "Desconocido"
        except sqlite3.Error as e:
            show_results(
                self.qcpc_input_output_text,
                f"Error accediendo a la base de datos: {str(e)}",
            )
            return "Desconocido"

    def show_game_image(self, item):
        # Obtener el game_id del item
        game_data = item.data(Qt.UserRole)
        game_id = game_data["game_id"]
        # Obtener la imagen del juego y mostrarla en qcpc_image_label
        self.get_game_image(game_id)

    def get_game_image(self, game_id):
        """Obtiene y procesa las imágenes del juego (boxart y screenshots)"""
        try:
            # Definir las rutas de las imágenes
            boxart_path_front = (
                self.config.get_path("boxart_path") / f"{game_id}_front_boxart.jpg"
            )
            boxart_path_back = (
                self.config.get_path("boxart_path") / f"{game_id}_back_boxart.jpg"
            )
            screenshot_dir = self.config.get_path("screenshot_path") / str(game_id)

            # Crear la carpeta de capturas de pantalla si no existe
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            # Realizar la solicitud a la API primero
            url = "https://api.thegamesdb.net/v1/Games/Images"
            params = {"apikey": self.config.api_key, "games_id": game_id}

            request = requests.get(url, params=params)
            request.raise_for_status()
            data = request.json()

            if data["data"]["count"] > 0:
                images = data["data"]["images"].get(str(game_id), [])
                base_url_thumb = data["data"]["base_url"]["thumb"]
                base_url_full = data["data"]["base_url"]["original"]

                boxart_found = False
                screenshots_found = False

                # Procesar imágenes
                for image in images:
                    image_type = image.get("type")
                    filename = image.get("filename")

                    if not image_type or not filename:
                        continue

                    # Procesar boxart
                    if image_type == "boxart":
                        image_side = image.get("side", "")
                        if image_side == "front":
                            target_path = boxart_path_front
                        elif image_side == "back":
                            target_path = boxart_path_back
                        else:
                            continue

                        # Siempre intentar descargar el boxart frontal
                        if image_side == "front" or not target_path.exists():
                            image_url = f"{base_url_thumb}{filename}"
                            self.download_image(
                                image_url,
                                str(target_path),
                                game_id,
                                f"{image_side} boxart",
                            )
                            if image_side == "front":
                                self.show_image(str(target_path))
                                boxart_found = True

                    # Procesar screenshots
                    elif image_type == "screenshot":
                        screenshot_path = screenshot_dir / filename
                        if not screenshot_path.exists():
                            image_url = f"{base_url_full}{filename}"
                            self.download_image(
                                image_url, str(screenshot_path), game_id, "screenshot"
                            )
                            screenshots_found = True

                # Mostrar mensaje según lo que se encontró
                if boxart_found or screenshots_found:
                    messages = []
                    if boxart_found:
                        messages.append("Boxart descargado")
                    if screenshots_found:
                        messages.append("Screenshots descargados")
                    show_results(self.qcpc_input_output_text, " y ".join(messages))
                else:
                    # Si no se descargó nada nuevo pero existe el boxart, mostrarlo
                    if boxart_path_front.exists():
                        self.show_image(str(boxart_path_front))
                        show_results(
                            self.qcpc_input_output_text, "Usando boxart existente"
                        )
                    else:
                        show_results(
                            self.qcpc_input_output_text,
                            "No se encontraron imágenes nuevas",
                        )
            else:
                show_results(
                    self.qcpc_input_output_text,
                    "No hay imágenes disponibles para este juego",
                )

        except requests.RequestException as e:
            show_results(
                self.qcpc_input_output_text, f"Error en la petición REST: {str(e)}"
            )
        except Exception as e:
            show_results(self.qcpc_input_output_text, f"Error inesperado: {str(e)}")

    def download_image(
        self, image_url: str, image_path: str, game_id: int, image_type: str
    ):
        """Descarga y guarda una imagen"""
        try:
            image_path = self._get_absolute_path(Path(image_path))
            image_path.parent.mkdir(parents=True, exist_ok=True)

            with requests.get(image_url, timeout=10, stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))

                with open(image_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            show_results(
                self.qcpc_input_output_text,
                f"Imagen {image_type} descargada ({total_size/1024:.1f}KB)",
            )

        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error descargando imagen: {str(e)}"
            )
            raise

    def show_image(
        self, image_path: str, label_width: int = None, label_height: int = None
    ):
        """Muestra una imagen en el QLabel ajustándola al tamaño"""
        try:
            # Cargar la imagen
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise ValueError("No se pudo cargar la imagen")

            # Obtener dimensiones del label si no se proporcionan
            if label_width is None:
                label_width = self.qcpc_image_label.width()
            if label_height is None:
                label_height = self.qcpc_image_label.height()

            # Escalar manteniendo proporción
            scaled_pixmap = pixmap.scaled(
                label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            # Mostrar imagen
            self.qcpc_image_label.setPixmap(scaled_pixmap)
            self.qcpc_image_label.setAlignment(Qt.AlignCenter)
            self.qcpc_image_label.update()

        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error mostrando imagen: {str(e)}"
            )

    def guardar_seleccion(self):
        """Guarda el juego seleccionado en la base de datos"""
        # Obtener el elemento seleccionado
        selected_item = self.qcpc_result_table.currentItem()
        if selected_item is None:
            show_results(
                self.qcpc_input_output_text, "No hay ningún juego seleccionado."
            )
            return

        # Obtener datos del juego
        game_data = selected_item.data(Qt.UserRole)
        game_id = game_data["game_id"]
        developer_id = game_data.get("developer_id", 10861)

        # Definir rutas de imágenes usando Path y asegurar que son absolutas
        boxart_temp = self._get_absolute_path(self.config.get_path("boxart_path"))
        boxart_final = self._get_absolute_path(
            self.config.get_path("boxart_path_images")
        )
        screenshot_temp = self._get_absolute_path(
            self.config.get_path("screenshot_path") / str(game_id)
        )
        screenshot_final = self._get_absolute_path(
            self.config.get_path("screenshot_path_images")
        )

        # Verificar y preparar rutas
        front_boxart_path = None
        back_boxart_path = None
        screenshot_paths = []

        # Comprobar boxarts
        front_temp = boxart_temp / f"{game_id}_front_boxart.jpg"
        back_temp = boxart_temp / f"{game_id}_back_boxart.jpg"

        if front_temp.exists():
            front_boxart_path = front_temp
        if back_temp.exists():
            back_boxart_path = back_temp

        # Comprobar screenshots
        if screenshot_temp.exists():
            screenshot_paths.extend(screenshot_temp.glob("*.jpg"))

        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()

                # Verificar si el juego ya existe
                cursor.execute("SELECT id FROM juegos WHERE id = ?", (game_id,))
                if cursor.fetchone():
                    show_results(
                        self.qcpc_input_output_text,
                        f"El juego con ID {game_id} ya está en la base de datos.",
                    )
                    return

                # Preparar las rutas relativas
                relative_front = "null"
                relative_back = "null"
                screenshot_relatives = []

                # Mover y registrar boxarts
                if front_boxart_path:
                    front_final = boxart_final / f"{game_id}_front_boxart.jpg"
                    front_final.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(front_boxart_path), str(front_final))
                    relative_front = str(front_final.relative_to(self.project_root))

                if back_boxart_path:
                    back_final = boxart_final / f"{game_id}_back_boxart.jpg"
                    back_final.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(back_boxart_path), str(back_final))
                    relative_back = str(back_final.relative_to(self.project_root))

                # Insertar datos del juego
                cursor.execute(
                    """
                    INSERT INTO juegos 
                    (id, game_title, release_date, platform, developer_id, front_boxart_path, back_boxart_path) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        game_id,
                        game_data["game_title"],
                        game_data["release_date"],
                        game_data["platform"],
                        developer_id,
                        relative_front,
                        relative_back,
                    ),
                )

                # Mover y registrar screenshots
                for screenshot_path in screenshot_paths:
                    screenshot_final_path = screenshot_final / screenshot_path.name
                    screenshot_final_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(screenshot_path), str(screenshot_final_path))
                    relative_screenshot = str(
                        screenshot_final_path.relative_to(self.project_root)
                    )
                    screenshot_relatives.append(relative_screenshot)

                # Si hay screenshots, insertarlos como una única entrada concatenada
                if screenshot_relatives:
                    screenshot_paths_str = ",".join(screenshot_relatives)
                    cursor.execute(
                        "INSERT INTO screenshots (game_id, screenshot_path) VALUES (?, ?)",
                        (game_id, screenshot_paths_str),
                    )

                conn.commit()
                show_results(
                    self.qcpc_input_output_text,
                    "Selección guardada correctamente en la base de datos.",
                )

                # Limpiar archivos temporales después de guardar exitosamente
                self.clean_unused_images()

        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error guardando la selección: {str(e)}"
            )

    def clean_unused_images(self):
        """Limpia imágenes temporales y no utilizadas"""
        try:
            # Limpiar carpetas temporales
            temp_dirs = [
                self.config.get_path("path_to_download"),
                self.config.get_path("boxart_path"),
                self.config.get_path("screenshot_path"),
            ]
            temp_deleted = self._clean_temp_directories(temp_dirs)
            permanent_deleted = self._clean_permanent_images()
            # Mostrar resumen
            self._show_cleanup_summary(temp_deleted, permanent_deleted)
        except Exception as e:
            show_results(
                self.qcpc_input_output_text, f"Error durante la limpieza: {str(e)}"
            )

    def _clean_temp_directories(self, directories):
        """Limpia directorios temporales incluyendo subdirectorios"""
        deleted_count = 0
        for dir_path in directories:
            if dir_path.exists():
                # Primero eliminar archivos
                for path in dir_path.rglob("*"):
                    if path.is_file():
                        try:
                            path.unlink()
                            deleted_count += 1
                            show_results(
                                self.qcpc_input_output_text,
                                f"Eliminado temporal: {path.relative_to(Path.cwd())}",
                            )
                        except Exception as e:
                            show_results(
                                self.qcpc_input_output_text,
                                f"Error eliminando archivo {path.name}: {e}",
                            )

                # Luego eliminar directorios vacíos (de abajo hacia arriba)
                for path in sorted(dir_path.rglob("*"), reverse=True):
                    if path.is_dir():
                        try:
                            path.rmdir()  # Solo elimina directorios vacíos
                            show_results(
                                self.qcpc_input_output_text,
                                f"Eliminado directorio: {path.relative_to(Path.cwd())}",
                            )
                        except Exception as e:
                            show_results(
                                self.qcpc_input_output_text,
                                f"Error eliminando directorio {path.name}: {e}",
                            )

        return deleted_count

    def _clean_permanent_images(self):
        """Limpia imágenes permanentes no utilizadas"""
        deleted_count = 0
        used_paths = self._get_used_image_paths()

        for dir_path in [
            self.config.get_path("boxart_path_images"),
            self.config.get_path("screenshot_path_images"),
        ]:
            if dir_path.exists():
                for file_path in dir_path.glob("*"):
                    if file_path.is_file() and str(file_path) not in used_paths:
                        try:
                            file_path.unlink()
                            deleted_count += 1
                            show_results(
                                self.qcpc_input_output_text,
                                f"Eliminada imagen no utilizada: {file_path.relative_to(Path.cwd())}",
                            )
                        except Exception as e:
                            show_results(
                                self.qcpc_input_output_text,
                                f"Error eliminando {file_path.name}: {e}",
                            )
        return deleted_count

    def _get_used_image_paths(self) -> set:
        """Obtiene el conjunto de rutas de imágenes usadas en la base de datos"""
        used_paths = set()
        try:
            with self.get_db_connection() as conn:
                cursor = conn.cursor()

                # Obtener rutas de boxart
                cursor.execute(
                    """
                    SELECT front_boxart_path, back_boxart_path 
                    FROM juegos 
                    WHERE front_boxart_path IS NOT NULL 
                    OR back_boxart_path IS NOT NULL
                """
                )
                for row in cursor.fetchall():
                    if row[0] and row[0] != "null":
                        used_paths.add(str(Path(row[0]).absolute()))
                    if row[1] and row[1] != "null":
                        used_paths.add(str(Path(row[1]).absolute()))

                # Obtener rutas de screenshots (que están concatenadas con comas)
                cursor.execute(
                    """
                    SELECT screenshot_path 
                    FROM screenshots 
                    WHERE screenshot_path IS NOT NULL
                """
                )
                for (paths_str,) in cursor.fetchall():
                    if paths_str and paths_str != "null":
                        # Dividir la cadena en rutas individuales
                        screenshot_paths = paths_str.split(",")
                        for path in screenshot_paths:
                            if path.strip():  # Ignorar cadenas vacías
                                used_paths.add(str(Path(path.strip()).absolute()))

        except sqlite3.Error as e:
            show_results(
                self.qcpc_input_output_text, f"Error accediendo a la base de datos: {e}"
            )

        return used_paths

    def _show_cleanup_summary(self, temp_deleted: int, permanent_deleted: int):
        """Muestra un resumen de la limpieza de imágenes"""
        summary = []

        if temp_deleted > 0:
            summary.append(f"{temp_deleted} archivos temporales eliminados")

        if permanent_deleted > 0:
            summary.append(f"{permanent_deleted} imágenes no utilizadas eliminadas")

        if not summary:
            message = "No se encontraron archivos para eliminar"
        else:
            message = "Limpieza completada: " + ", ".join(summary)

        show_results(self.qcpc_input_output_text, message)
