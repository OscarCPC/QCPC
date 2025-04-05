import os
import sys
import warnings
from contextlib import redirect_stderr
from io import StringIO

# Suppress all warnings before importing Qt
warnings.filterwarnings("ignore")
os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"

# Import Qt after warning suppression
from frames.menu import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFile, QIODevice
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget


class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.clickPosition = None  # define clickPosition aquí

        # Aplicar la fuente después de la inicialización de la interfaz de usuario

        # eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        # mover ventana

        self.ui.frame_superior.mouseMoveEvent = self.mover_ventana_event

        # control barra de titulos
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())

        self.ui.bt_restaurar.hide()

        # menu lateral
        self.ui.bt_menu.clicked.connect(self.mover_menu)

    def mover_ventana_event(self, event):
        if event:
            self.mover_ventana(event)

    def mouseMoveEvent(self, event):
        self.mover_ventana_event(event)
        self.mover_menu(event)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.clickPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.clickPosition is not None:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.ui.bt_restaurar.hide()
        self.ui.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.ui.bt_maximizar.hide()
        self.ui.bt_restaurar.show()

    def mover_menu(self, event=None):  # Añade 'event=None' aquí
        if event and self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:  # Ahora 'event' está definido
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if self.clickPosition is not None and event:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
        if True:
            width = self.ui.frame_lateral.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.ui.frame_lateral, b"minimumWidth")
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()

    ## SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    ## mover ventana

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                if self.clickPosition is not None:  # Verificar si clickPosition es None
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
            event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()


if __name__ == "__main__":
    # Redirect stderr to StringIO to capture Qt warnings
    stderr_redirect = StringIO()

    try:
        with redirect_stderr(stderr_redirect):
            # Create Qt application with debug output disabled
            QtCore.qInstallMessageHandler(lambda *args: None)
            app = QtWidgets.QApplication(sys.argv + ["--no-sandbox"])

            # Disable Qt debug output
            app.setApplicationName("QCPC")
            QtCore.QLoggingCategory.setFilterRules("*.debug=false\nqt.*=false")

            # ...existing font loading code...
            # Cargar y verificar la fuente
            font_path = "./Assets/fonts/amstrad_cpc464.ttf"
            if not os.path.exists(font_path):
                print(f"Error: Font file not found at {font_path}")
                sys.exit(1)

            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    default_font = QFont(font_families[0], 10)
                    app.setFont(default_font)
                else:
                    print("Error: No font families found in the font file")
            else:
                print("Error: Failed to load font")

            app.setWindowIcon(QtGui.QIcon("./Assets/images/logo.png"))

            # ...existing QSS loading code...
            file_path = "./qss/style.qss"
            qss_file = QFile(file_path)

            if qss_file.open(
                QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
            ):
                qss_content = qss_file.readAll()
                app.setStyleSheet(str(qss_content, "utf-8"))
                qss_file.close()

            # Create and show main window
            mi_app = MiApp()
            mi_app.show()
            sys.exit(app.exec_())

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
