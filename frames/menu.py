from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    pyqtSignal,
    pyqtProperty,
)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie, QPixmap, QIcon
import qtawesome as qta
from .qcpc_search import *
from .qcpc_list import *
from .qcpc_form import *


class StackedWidgetFadeTransition(QWidget):
    """
    Widget para proporcionar transiciones suaves entre páginas de un QStackedWidget.
    Esta clase maneja cuidadosamente los recursos de pintura para evitar conflictos.
    """

    transitionFinished = pyqtSignal()

    def __init__(self, stackedWidget):
        super().__init__(stackedWidget.parent())
        self.stackedWidget = stackedWidget
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

        # Configurar geometría inicial
        self.setGeometry(self.stackedWidget.geometry())

        # Inicializar variables
        self._opacity = (
            0.0  # Usar nombre con guión bajo para evitar conflictos con property
        )
        self.nextWidget = None
        self.currentWidget = None
        self.inTransition = False

        # Crear animación
        self.fadeAnimation = QPropertyAnimation(self, b"opacity")
        self.fadeAnimation.setDuration(300)
        self.fadeAnimation.setEasingCurve(QEasingCurve.InOutCubic)
        self.fadeAnimation.finished.connect(self.onFadeFinished)

        # Hacer seguimiento a cambios de geometría del stackedWidget
        self.stackedWidget.installEventFilter(self)

        # Ocultar inicialmente
        self.hide()

    def eventFilter(self, obj, event):
        """Mantener la geometría del widget de transición sincronizada con el stackedWidget"""
        if obj == self.stackedWidget and event.type() == event.Resize:
            self.setGeometry(self.stackedWidget.geometry())
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        """Pintar efecto de transición con opacidad controlada"""
        if not self.isVisible():
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Pintar fondo negro con opacidad controlada
        color = QColor(0, 0, 0, int(self._opacity * 255))
        painter.fillRect(self.rect(), color)

        painter.end()

    # Eliminar la definición de property Python para evitar conflictos
    # Ya que usaremos pyqtProperty directamente

    # Estos métodos son necesarios para que QPropertyAnimation funcione
    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        if self._opacity != opacity:
            self._opacity = opacity
            self.update()

    # Definir la propiedad para QPropertyAnimation
    opacity = pyqtProperty(float, getOpacity, setOpacity)

    def transitionTo(self, nextWidget):
        """Iniciar transición hacia el widget especificado"""
        if self.inTransition or nextWidget == self.stackedWidget.currentWidget():
            return

        self.inTransition = True
        self.nextWidget = nextWidget
        self.currentWidget = self.stackedWidget.currentWidget()

        # Mostrar el widget de transición
        self.raise_()
        self.show()

        # Configurar y comenzar la animación de entrada
        self.fadeAnimation.setStartValue(0.0)
        self.fadeAnimation.setEndValue(0.7)  # 70% de opacidad, más suave visualmente
        self.fadeAnimation.start()

    def onFadeFinished(self):
        """Manejar el final de la animación"""
        if not self.inTransition:
            return

        # Si estamos en fade-in, cambiar al widget destino y comenzar fade-out
        if self.fadeAnimation.direction() == QPropertyAnimation.Forward:
            # Cambiar al widget destino
            self.stackedWidget.setCurrentWidget(self.nextWidget)

            # Configurar animación de salida
            self.fadeAnimation.setDirection(QPropertyAnimation.Backward)
            self.fadeAnimation.start()
        else:
            # Fin de la transición
            self.hide()
            self.inTransition = False
            self.nextWidget = None
            self.currentWidget = None
            self.fadeAnimation.setDirection(QPropertyAnimation.Forward)
            self.transitionFinished.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Configuración básica
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1590, 970))

        # Inicializar componentes
        self.initComponents()

        # Crear estructura principal
        self.createCentralWidget(MainWindow)
        self.createHeader()
        self.createMainPanel()
        self.setup_gif()

        # Aplicar textos
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def initComponents(self):
        """Inicializar componentes principales"""
        self.qcpc_search = qcpc_search()  # Página de búsqueda
        self.qcpc_list = qcpc_list()  # Página de listado
        self.qcpc_form = qcpc_form()

    def createCentralWidget(self, MainWindow):
        # Widget central y layout principal
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        MainWindow.setCentralWidget(self.centralwidget)

    def createHeader(self):
        # Barra superior
        self.frame_superior = QtWidgets.QFrame(self.centralwidget)
        self.frame_superior.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_superior.setMaximumSize(QtCore.QSize(16777215, 50))
        # self.frame_superior.setFrameShape(QtWidgets.QFrame.StyledPanel)

        # Layout horizontal para la barra superior
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_superior)
        self.horizontalLayout_8.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_8.setSpacing(0)

        # Botón de menú
        self.bt_menu = QtWidgets.QPushButton(self.frame_superior)
        self.bt_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.bt_menu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.bt_menu.setIcon(QIcon("./Assets/images/logo.png"))
        self.bt_menu.setIconSize(QtCore.QSize(64, 32))
        self.horizontalLayout_8.addWidget(self.bt_menu, 0, QtCore.Qt.AlignLeft)

        # Espaciador
        spacerItem = QtWidgets.QSpacerItem(
            265, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_8.addItem(spacerItem)

        # Botones de control de ventana
        self.createWindowControlButtons()

        # Agregar barra superior al layout principal
        self.verticalLayout.addWidget(self.frame_superior)

    def createWindowControlButtons(self):
        # Botón minimizar
        self.bt_minimizar = self.createWindowButton("fa.window-minimize", 35, 35)
        self.horizontalLayout_8.addWidget(self.bt_minimizar, 0, QtCore.Qt.AlignRight)

        # Botón restaurar
        self.bt_restaurar = self.createWindowButton("fa.window-restore", 35, 35)
        self.horizontalLayout_8.addWidget(self.bt_restaurar, 0, QtCore.Qt.AlignRight)

        # Botón maximizar
        self.bt_maximizar = self.createWindowButton("fa.window-maximize", 35, 35)
        self.horizontalLayout_8.addWidget(self.bt_maximizar, 0, QtCore.Qt.AlignRight)

        # Botón cerrar
        self.bt_cerrar = self.createWindowButton("fa.window-close", 35, 16777215)
        self.horizontalLayout_8.addWidget(self.bt_cerrar, 0, QtCore.Qt.AlignRight)

    def createWindowButton(self, icon_name, min_width, max_width):
        button = QtWidgets.QPushButton(self.frame_superior)
        button.setMinimumSize(QtCore.QSize(min_width, 35))
        button.setMaximumSize(QtCore.QSize(max_width, 35))
        button.setText("")
        button.setIcon(qta.icon(icon_name, color="yellow"))
        button.setIconSize(QtCore.QSize(32, 32))
        return button

    def createMainPanel(self):
        # Panel inferior principal
        self.frame_inferior = QtWidgets.QFrame(self.centralwidget)
        # self.frame_inferior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_inferior)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        # Crear panel lateral y contenedor principal
        self.createSidePanel()
        self.createContentPanel()

        # Agregar panel inferior al layout principal
        self.verticalLayout.addWidget(self.frame_inferior)

    def createSidePanel(self):
        # Panel lateral
        self.frame_lateral = QtWidgets.QFrame(self.frame_inferior)
        self.frame_lateral.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_lateral.setMaximumSize(QtCore.QSize(0, 16777215))
        # self.frame_lateral.setFrameShape(QtWidgets.QFrame.StyledPanel)

        # Layout vertical para botones laterales
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_lateral)
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 9)
        self.verticalLayout_2.setSpacing(20)

        # Crear botones laterales
        self.createSideButtons()

        # Agregar panel lateral al layout del panel inferior
        self.horizontalLayout.addWidget(self.frame_lateral, 0, QtCore.Qt.AlignLeft)

    def createSideButtons(self):
        """Crear y añadir botones al panel lateral"""
        # Botón inicio
        self.bt_inicio = self.createSideButton("fa.github", "bt_inicio")
        self.verticalLayout_2.addWidget(self.bt_inicio)

        # Botón uno (Text Editor)
        self.bt_qcpc_search = self.createSideButton("fa.text-width", "bt_qcpc_search")
        self.verticalLayout_2.addWidget(self.bt_qcpc_search)

        # Botón dos (Copy Files)
        self.bt_qcpc_list = self.createSideButton("fa5.copy", "bt_qcpc_list")
        self.verticalLayout_2.addWidget(self.bt_qcpc_list)

        # Botón tres (WA Zara)
        self.bt_qcpc_form = self.createSideButton("mdi.api", "bt_qcpc_form")
        self.verticalLayout_2.addWidget(self.bt_qcpc_form)

        # Espaciador para empujar los elementos hacia arriba si hay espacio adicional
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)

        # Etiqueta inferior
        self.label_2 = QtWidgets.QLabel(self.frame_lateral)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_2)

    def createSideButton(self, icon_name, obj_name, color="yellow"):
        button = QtWidgets.QPushButton(self.frame_lateral)
        button.setMinimumSize(QtCore.QSize(0, 40))
        button.setIcon(qta.icon(icon_name, color=color))
        button.setIconSize(QtCore.QSize(32, 32))
        button.setObjectName(obj_name)
        return button

    def createContentPanel(self):
        # Panel contenedor
        self.frame_contenedor = QtWidgets.QFrame(self.frame_inferior)
        # self.frame_contenedor.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_contenedor.setLineWidth(1)

        # Layout vertical para el contenido
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_contenedor)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)

        # Crear y configurar el stackedWidget
        self.createStackedWidget()
        self.configureStackedPages()

        # Agregar contenedor al layout del panel inferior
        self.horizontalLayout.addWidget(self.frame_contenedor)

    def createStackedWidget(self):
        # StackedWidget para mostrar diferentes páginas
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_contenedor)
        self.stackedWidget.setMinimumSize(QtCore.QSize(1390, 900))
        # self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.verticalLayout_3.addWidget(self.stackedWidget)

    def configureStackedPages(self):
        # Crear página inicial (home)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("cover")
        self.page_one_layout = QtWidgets.QGridLayout(self.page)

        # Imagen principal
        self.label_page = QtWidgets.QLabel(self.page)
        self.label_page.setAlignment(QtCore.Qt.AlignCenter)
        icon = QPixmap("./Assets/images/cpc.png")
        self.label_page.setPixmap(icon.scaled(900, 600, Qt.KeepAspectRatio))
        self.page_one_layout.addWidget(self.label_page, 1, 1, 1, 1)

        # Agregar páginas al stack y conectar botones
        self.addPagesToStack()
        self.connectButtons()

    def addPagesToStack(self):
        """Agregar todas las páginas al stackedWidget"""
        self.stackedWidget.addWidget(self.page)  # Index 0 - Home page
        self.stackedWidget.addWidget(self.qcpc_search)  # Index 1 - Buscar
        self.stackedWidget.addWidget(self.qcpc_list)  # Index 2 - Listado
        self.stackedWidget.addWidget(self.qcpc_form)  # Index 3 - Formulario

        # Crear el manejador de transiciones usando la clase externa
        self.transition = StackedWidgetFadeTransition(self.stackedWidget)

        # Conectar la señal de finalización si es necesario hacer algo cuando termine
        self.transition.transitionFinished.connect(self.onTransitionFinished)

    def onTransitionFinished(self):
        """Se llama cuando la transición entre páginas ha terminado"""
        # Puedes agregar aquí cualquier acción adicional cuando finaliza la transición
        pass

    def connectButtons(self):
        """Conectar botones con sus respectivas páginas usando la transición"""
        self.bt_inicio.clicked.connect(lambda: self.transition.transitionTo(self.page))
        self.bt_qcpc_search.clicked.connect(
            lambda: self.transition.transitionTo(self.qcpc_search)
        )
        self.bt_qcpc_list.clicked.connect(
            lambda: self.transition.transitionTo(self.qcpc_list)
        )
        self.bt_qcpc_form.clicked.connect(
            lambda: self.transition.transitionTo(self.qcpc_form)
        )

    def setup_gif(self):
        """Setup GIF in QLabel"""
        self.gif_label = QtWidgets.QLabel(self.frame_lateral)
        self.gif_label.setAlignment(QtCore.Qt.AlignCenter)
        self.movie = QMovie("./Assets/images/mini_renegade.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Create a layout for the GIF and label
        self.gif_layout = QtWidgets.QVBoxLayout()
        self.gif_layout.setContentsMargins(0, 0, 0, 0)
        self.gif_layout.setSpacing(2)  # Set spacing between GIF and label

        # Add spacer to push GIF and label to the bottom
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gif_layout.addItem(spacerItem1)

        # Add GIF and label to the layout
        self.gif_layout.addWidget(self.gif_label)
        self.label_2 = QtWidgets.QLabel(self.frame_lateral)
        self.label_2.setAlignment(Qt.AlignLeft)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gif_layout.addWidget(self.label_2)

        # Add the GIF layout to the main vertical layout
        self.verticalLayout_2.addLayout(self.gif_layout)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", 'Run"'))
        self.bt_menu.setText(_translate("MainWindow", "    MENU "))
        self.bt_inicio.setText(_translate("MainWindow", "       Inicio"))
        self.bt_qcpc_search.setText(_translate("MainWindow", "   Buscar"))
        self.bt_qcpc_list.setText(_translate("MainWindow", "    Listado"))
        self.bt_qcpc_form.setText(_translate("MainWindow", "      Formulario"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<table width="100%"><tr><td width="50%" align="left">Run"</td></tr>'
                '<tr><td width="50%" align="right">Press <strong>PLAY</strong> and then any key:</td></tr>',
            )
        )
