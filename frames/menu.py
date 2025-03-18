from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie
import qtawesome as qta
from .qcpc_search import *
from .qcpc_list import *
from .qcpc_form import *


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1410, 970))

        self.init_widgets()
        self.setup_central_widget(MainWindow)
        self.setup_layouts()
        self.setup_frames()
        self.setup_menu_buttons()
        self.setup_window_controls()
        self.setup_stacked_widget()
        self.setup_gif()

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def init_widgets(self):
        """Initialize main widgets"""
        self.qcpc_search = qcpc_search()
        self.qcpc_search.setupUi()
        self.qcpc_list = qcpc_list()
        self.qcpc_list.setupUi()
        self.qcpc_form = qcpc_form()
        self.qcpc_form.setupUi()

    def setup_central_widget(self, MainWindow):
        """Setup central widget and main layout"""
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

    def setup_layouts(self):
        """Setup main layouts"""
        # Vertical layout for central widget
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Horizontal layout for inferior frame
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Layout for superior frame
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        # Layout for lateral frame
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 9)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

    def setup_frames(self):
        """Setup main frames"""
        # Superior frame
        self.frame_superior = self.create_frame(
            "frame_superior", min_height=35, max_height=50
        )
        self.frame_superior.setLayout(self.horizontalLayout_8)
        self.verticalLayout.addWidget(self.frame_superior)

        # Inferior frame
        self.frame_inferior = self.create_frame("frame_inferior")
        self.frame_inferior.setLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame_inferior)

        # Lateral frame
        self.frame_lateral = self.create_frame("frame_lateral", max_width=0)
        self.frame_lateral.setLayout(self.verticalLayout_2)
        self.horizontalLayout.addWidget(self.frame_lateral, 0, QtCore.Qt.AlignLeft)

        # Container frame
        self.frame_contenedor = self.create_frame("frame_contenedor")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_contenedor)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout.addWidget(self.frame_contenedor)

    def create_frame(
        self, name, min_height=0, max_height=16777215, min_width=0, max_width=16777215
    ):
        """Helper function to create frames"""
        frame = QtWidgets.QFrame(self.centralwidget)
        frame.setObjectName(name)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setMinimumSize(QtCore.QSize(min_width, min_height))
        frame.setMaximumSize(QtCore.QSize(max_width, max_height))
        return frame

    def setup_menu_buttons(self):
        """Setup menu and navigation buttons"""
        self.create_menu_button()
        self.create_navigation_buttons()

    def create_menu_button(self):
        """Create main menu button"""
        self.bt_menu = QtWidgets.QPushButton(self.frame_superior)
        self.bt_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.bt_menu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.icon_menu = QtGui.QIcon()
        self.icon_menu.addPixmap(
            QtGui.QPixmap("./Assets/images/logo.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.bt_menu.setIcon(self.icon_menu)
        self.bt_menu.setIconSize(QtCore.QSize(64, 32))
        self.bt_menu.setObjectName("bt_menu")
        self.horizontalLayout_8.addWidget(self.bt_menu, 0, QtCore.Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(
            265, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_8.addItem(spacerItem)

    def create_navigation_buttons(self):
        """Create navigation buttons"""
        buttons = [
            ("bt_inicio", "fa.github", "yellow"),
            ("bt_uno", "mdi.api", "yellow"),
            ("bt_dos", "fa5.copy", "yellow"),
            ("bt_tres", "mdi.api", "yellow"),
            ("bt_cuatro", "fa5b.firefox-browser", "red"),
        ]

        for btn_id, icon_name, color in buttons:
            button = QtWidgets.QPushButton(self.frame_lateral)
            button.setMinimumSize(QtCore.QSize(0, 40))
            button.setIcon(qta.icon(icon_name, color=color))
            button.setIconSize(QtCore.QSize(32, 32))
            button.setObjectName(btn_id)
            self.verticalLayout_2.addWidget(button)
            setattr(self, btn_id, button)

        # Add spacer and label
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)

    def setup_window_controls(self):
        """Setup window control buttons (minimize, maximize, close)"""
        controls = [
            ("bt_minimizar", "fa.window-minimize"),
            ("bt_restaurar", "fa.window-restore"),
            ("bt_maximizar", "fa.window-maximize"),
            ("bt_cerrar", "fa.window-close"),
        ]

        for btn_id, icon_name in controls:
            button = QtWidgets.QPushButton(self.frame_superior)
            button.setMaximumSize(QtCore.QSize(35, 35))
            button.setIcon(qta.icon(icon_name, color="yellow"))
            button.setIconSize(QtCore.QSize(32, 32))
            button.setObjectName(btn_id)
            self.horizontalLayout_8.addWidget(button, 0, QtCore.Qt.AlignRight)
            setattr(self, btn_id, button)

    def setup_stacked_widget(self):
        """Setup stacked widget and pages"""
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_contenedor)
        self.stackedWidget.setMinimumSize(QtCore.QSize(1190, 900))
        self.stackedWidget.setObjectName("stackedWidget")

        # Add pages
        self.setup_cover_page()
        self.setup_content_pages()

        self.verticalLayout_3.addWidget(self.stackedWidget)

    def setup_cover_page(self):
        """Setup cover page with logo"""
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("cover")
        self.page_one_layout = QtWidgets.QGridLayout(self.page)

        self.label_page = QtWidgets.QLabel(self.page)
        self.label_page.setAlignment(QtCore.Qt.AlignCenter)
        self.icon = QtGui.QPixmap("./Assets/images/cpc.png")
        self.icon = self.icon.scaled(900, 600, Qt.KeepAspectRatio)
        self.label_page.setPixmap(self.icon)

        self.page_one_layout.addWidget(self.label_page, 1, 1, 1, 1)
        self.stackedWidget.addWidget(self.page)

    def setup_content_pages(self):
        """Setup content pages"""
        pages = [
            (self.qcpc_search, "qcpc_search"),
            (self.qcpc_list, "qcpc_list"),
            (self.qcpc_form, "qcpc_form"),
        ]

        for widget, name in pages:
            page = QtWidgets.QWidget()
            page.setObjectName(name)
            self.stackedWidget.addWidget(widget)
            self.stackedWidget.addWidget(page)

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
        """Translate UI elements"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QCPC"))
        self.bt_menu.setText(_translate("MainWindow", "    MENU "))
        self.bt_inicio.setText(_translate("MainWindow", "       Inicio"))
        self.bt_uno.setText(_translate("MainWindow", "   Buscar"))
        self.bt_dos.setText(_translate("MainWindow", "    Listado"))
        self.bt_tres.setText(_translate("MainWindow", "    Formulario"))
        self.bt_cuatro.setText(_translate("MainWindow", "     Links"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<table width="100%"><tr><td width="50%" align="left">Run</td></tr>'
                '<tr><td width="50%" align="right">Press PLAY and then any key:</td></tr>',
            )
        )
