import sys
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QApplication, QFrame, QFormLayout, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTextEdit, QGridLayout

class MyApp(QFrame):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
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
        self.qcpc_attribute_list_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_attribute_list_frame.setObjectName("qcpc_attribute_list_frame")
        self.qcpc_attribute_list_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_attribute_list_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_attributes = QVBoxLayout(self.qcpc_attribute_list_frame)
        self.verticalLayout_attributes.setObjectName("verticalLayout_attributes")
        self.qcpc_attribute_list = QListWidget(self.qcpc_attribute_list_frame)
        self.qcpc_attribute_list.setObjectName("qcpc_attribute_list")
        self.verticalLayout_attributes.addWidget(self.qcpc_attribute_list)

        # Añadir el frame de la lista de atributos al layout principal
        self.gridLayout_2.addWidget(self.qcpc_attribute_list_frame, 0, 0, 2, 1)  # 2 filas de altura

        # Frame de la imagen (Widget 2)
        self.qcpc_image_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_image_frame.setObjectName("qcpc_image_frame")
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_image_layout = QVBoxLayout(self.qcpc_image_frame)
        self.qcpc_image_layout.setObjectName("qcpc_image_layout")
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName("qcpc_image_label")
        self.qcpc_image_label.setMinimumSize(QSize(300, 450))  # Ocupa la mitad de la altura del primer widget
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
        self.qcpc_text_label = QTextEdit(self.qcpc_text_frame)
        self.qcpc_text_label.setObjectName("qcpc_text_label")
        self.qcpc_text_label.setReadOnly(True)
        self.qcpc_text_layout.addWidget(self.qcpc_text_label)

        # Añadir el frame del texto al layout principal
        self.gridLayout_2.addWidget(self.qcpc_text_frame, 1, 1, 1, 1)

        # Añadir el contenedor principal al layout del formulario
        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.qcpc_frame_container)

        # Traducciones y conexiones
        self.retranslateUi()
        self.setup_connections()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("qcpc_search", "Form", None))
        self.qcpc_attribute_list.setWindowTitle(QCoreApplication.translate("qcpc_search", "Atributos", None))
        self.qcpc_image_label.setText(QCoreApplication.translate("qcpc_search", "Imagen", None))
        self.qcpc_text_label.setPlaceholderText(QCoreApplication.translate("qcpc_search", "Resultados", None))

    def setup_connections(self):
        pass  # Aquí puedes definir las conexiones necesarias

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
