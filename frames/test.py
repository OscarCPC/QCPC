class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Configuración inicial del UI
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

        # Conectar la señal itemClicked a la función handle_item_click
        self.qcpc_attribute_list.itemClicked.connect(self.handle_item_click)

        # Añadir el frame de la lista de atributos al layout principal
        self.gridLayout_2.addWidget(self.qcpc_attribute_list_frame, 0, 0, 2, 1)

        # Añadir nuevo frame para los botones en la parte inferior
        self.qcpc_button_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_button_frame.setObjectName("qcpc_button_frame")
        self.qcpc_button_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_button_frame.setFrameShadow(QFrame.Raised)
        self.button_layout = QHBoxLayout(self.qcpc_button_frame)
        self.button_layout.setObjectName("button_layout")
        
        self.button1 = QPushButton("Botón 1")
        self.button2 = QPushButton("Botón 2")
        self.button3 = QPushButton("Botón 3")
        self.button4 = QPushButton("Vaciar Lista")
        self.button4.clicked.connect(self.clear_attribute_list)  # Conectar el botón a la función

        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)
        self.button_layout.addWidget(self.button4)

        # Añadir el frame de los botones al layout principal
        self.gridLayout_2.addWidget(self.qcpc_button_frame, 2, 0, 1, 2)

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.qcpc_frame_container)

        # Traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)
        
        self.show_all_games()

    def retranslateUi(self):
        # Añadir traducciones aquí si es necesario
        pass

    def setup_connections(self):
        # Añadir conexiones de señales aquí si es necesario
        pass

    def clear_attribute_list(self):
        self.qcpc_attribute_list.clear()

    def handle_item_click(self, item):
        # Manejar el evento de clic en un elemento de la lista
        data = item.data(Qt.UserRole)
        print(f"Clicked item: {data['game_title']}")  # Ejemplo de acción: imprimir el título del juego

    def show_all_games(self):
        # Ejemplo de función para mostrar juegos (conectar a base de datos, etc.)
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mi_app = MyApp()
    mi_app.show()
    sys.exit(app.exec_())
