from PyQt5.QtCore import *  # Agregamos Qt aquí
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
import qtawesome as qta
from .qcpc_search import *
from .qcpc_list import *
from .qcpc_form import *



class Ui_MainWindow(object):  
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1410, 970))    
        
        self.qcpc_search = qcpc_search()
        self.qcpc_search.setupUi()         
        self.qcpc_list = qcpc_list()
        self.qcpc_list.setupUi()
        self.qcpc_form = qcpc_form()
        self.qcpc_form.setupUi()
        #self.roland_browser = RolandBrowser()
        #self.roland_browser.setupUi()
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_superior = QtWidgets.QFrame(self.centralwidget)
        self.frame_superior.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_superior.setMaximumSize(QtCore.QSize(16777215, 50))
        
        #Menu
        self.frame_superior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_superior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_superior.setObjectName("frame_superior")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_superior)
        self.horizontalLayout_8.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.bt_menu = QtWidgets.QPushButton(self.frame_superior)
        self.bt_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.bt_menu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.icon_menu = QtGui.QIcon()
        self.icon_menu.addPixmap(QtGui.QPixmap("./Assets/images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                   
        self.bt_menu.setIcon(self.icon_menu)
        self.bt_menu.setIconSize(QtCore.QSize(64, 32))
        self.bt_menu.setAutoDefault(False)
        self.bt_menu.setDefault(False)
        self.bt_menu.setFlat(False)
        self.bt_menu.setObjectName("bt_menu")
        self.horizontalLayout_8.addWidget(self.bt_menu, 0, QtCore.Qt.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(265, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.bt_minimizar = QtWidgets.QPushButton(self.frame_superior)
        self.bt_minimizar.setMinimumSize(QtCore.QSize(35, 35))
        
        #Window Minimize
        self.bt_minimizar.setText("")        
        self.bt_minimizar.setIcon(qta.icon('fa.window-minimize', color="yellow"))
        self.bt_minimizar.setIconSize(QtCore.QSize(32, 32))
        self.bt_minimizar.setFlat(False)
        self.bt_minimizar.setObjectName("bt_minimizar")
        self.horizontalLayout_8.addWidget(self.bt_minimizar, 0, QtCore.Qt.AlignRight)
        #Window Resize
        self.bt_restaurar = QtWidgets.QPushButton(self.frame_superior)
        self.bt_restaurar.setMaximumSize(QtCore.QSize(35, 35))        
        self.bt_restaurar.setText("")        
        self.bt_restaurar.setIcon(qta.icon('fa.window-restore', color="yellow"))
        self.bt_restaurar.setIconSize(QtCore.QSize(30, 30))
        self.bt_restaurar.setObjectName("bt_restaurar")
        self.horizontalLayout_8.addWidget(self.bt_restaurar, 0, QtCore.Qt.AlignRight)
        #window maximize
        self.bt_maximizar = QtWidgets.QPushButton(self.frame_superior)
        self.bt_maximizar.setMaximumSize(QtCore.QSize(35, 35))        
        self.bt_maximizar.setText("")                
        self.bt_maximizar.setIcon(qta.icon('fa.window-maximize', color="yellow"))
        self.bt_maximizar.setIconSize(QtCore.QSize(32, 32))
        self.bt_maximizar.setObjectName("bt_maximizar")
        self.horizontalLayout_8.addWidget(self.bt_maximizar, 0, QtCore.Qt.AlignRight)
        #Window Close
        self.bt_cerrar = QtWidgets.QPushButton(self.frame_superior)
        self.bt_cerrar.setMaximumSize(QtCore.QSize(35, 16777215))       
        self.bt_cerrar.setText("")        
        self.bt_cerrar.setIcon(qta.icon('fa.window-close', color="yellow"))
        self.bt_cerrar.setIconSize(QtCore.QSize(32, 32))
        self.bt_cerrar.setObjectName("bt_cerrar")
        self.horizontalLayout_8.addWidget(self.bt_cerrar, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame_superior)
        
        #Frame inferior
        self.frame_inferior = QtWidgets.QFrame(self.centralwidget)        
        self.frame_inferior.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_inferior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inferior.setObjectName("frame_inferior")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_inferior)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        #Frame Lateral
        self.frame_lateral = QtWidgets.QFrame(self.frame_inferior)
        self.frame_lateral.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_lateral.setMaximumSize(QtCore.QSize(0, 16777215))
        self.frame_lateral.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_lateral.setAutoFillBackground(False)        
        self.frame_lateral.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lateral.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_lateral.setObjectName("frame_lateral")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_lateral)
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 9)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        #Boton inicio
        self.bt_inicio = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_inicio.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_inicio.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.bt_inicio.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.bt_inicio.setIcon(qta.icon('fa.github', color="yellow"))
        self.bt_inicio.setIconSize(QtCore.QSize(32, 32))
        self.bt_inicio.setObjectName("bt_inicio")
        self.verticalLayout_2.addWidget(self.bt_inicio)
        
        #Boton 1        
        self.bt_uno = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_uno.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_uno.setToolTipDuration(0)
        self.bt_uno.setIcon(qta.icon('mdi.api', color="yellow"))
        self.bt_uno.setIconSize(QtCore.QSize(32, 32))
        self.bt_uno.setObjectName("bt_uno")        
        self.verticalLayout_2.addWidget(self.bt_uno)
        
        #Boton 2
        self.bt_dos = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_dos.setMinimumSize(QtCore.QSize(0, 40))        
        self.bt_dos.setIcon(qta.icon('fa5.copy', color="yellow"))        
        self.bt_dos.setIconSize(QtCore.QSize(32, 32))
        self.bt_dos.setObjectName("bt_dos")
        self.verticalLayout_2.addWidget(self.bt_dos)
        
        #Boton 3
        self.bt_tres = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_tres.setMinimumSize(QtCore.QSize(0, 40))        
        self.bt_tres.setIcon(qta.icon('mdi.api', color="yellow"))
        self.bt_tres.setIconSize(QtCore.QSize(32, 32))
        self.bt_tres.setObjectName("bt_tres")
        self.verticalLayout_2.addWidget(self.bt_tres)
        
        #Boton 4
        self.bt_cuatro = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_cuatro.setMinimumSize(QtCore.QSize(0, 40))                
        self.bt_cuatro.setIcon(qta.icon('fa5b.firefox-browser', color="red"))
        self.bt_cuatro.setIconSize(QtCore.QSize(32, 32))
        self.bt_cuatro.setObjectName("bt_cuatro")
        self.verticalLayout_2.addWidget(self.bt_cuatro)
        
        
        #Boton 5
        self.bt_cinco = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_cinco.setMinimumSize(QtCore.QSize(0, 40))        
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("videojuego.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_cinco.setIcon(icon10)
        self.bt_cinco.setIconSize(QtCore.QSize(32, 32))
        self.bt_cinco.setObjectName("bt_cinco")
        self.verticalLayout_2.addWidget(self.bt_cinco)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        
        
        self.label_2 = QtWidgets.QLabel(self.frame_lateral)
        self.label_2.setAlignment(Qt.AlignLeft)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.frame_lateral, 0, QtCore.Qt.AlignLeft)
        
        #Frame Contenedor
        self.frame_contenedor = QtWidgets.QFrame(self.frame_inferior)        
        self.frame_contenedor.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_contenedor.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_contenedor.setLineWidth(1)
        self.frame_contenedor.setObjectName("frame_contenedor")
        self.frame_contenedor.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_contenedor.setMaximumSize(QtCore.QSize(16777215, 16777215))
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_contenedor)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3") 
        
        #Stacked Widget       
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_contenedor)
        self.stackedWidget.setMinimumSize(QtCore.QSize(1190, 900))
        self.stackedWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.addWidget(self.qcpc_search)
        self.stackedWidget.addWidget(self.qcpc_list)
        self.stackedWidget.addWidget(self.qcpc_form)
        
        #self.bt_uno.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.text_editor))
        

        
        #Pagina 0
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("cover")
        self.page_one_layout = QtWidgets.QGridLayout(self.page)
        self.page_one_layout.setObjectName("page_one_layout")
        self.label_page = QtWidgets.QLabel(self.page)        
        self.label_page.setScaledContents(False)
        self.label_page.setAlignment(QtCore.Qt.AlignCenter)
        self.label_page.setIndent(0)
        self.label_page.setObjectName("label")
        self.page_one_layout.addWidget(self.label_page)
        self.stackedWidget.addWidget(self.page)
        self.icon = QtGui.QPixmap('./Assets/images/cpc.png') 
        self.icon = self.icon.scaled(900, 600, Qt.KeepAspectRatio)            
        self.label_page.setPixmap(self.icon)         
        self.page_one_layout.addWidget(self.label_page,1,1,1,1)
        
        
        #pagina 1
        self.page_one = QtWidgets.QWidget()        
        self.page_one.setObjectName("qcpc_search")
        self.stackedWidget.addWidget(self.page_one)
        
        #pagina 2
        self.page_two = QtWidgets.QWidget()        
        self.page_two.setObjectName("qcpc_list")
        self.stackedWidget.addWidget(self.page_two)
        
        #pagina 3
        self.page_three = QtWidgets.QWidget()        
        self.page_three.setObjectName("qcpc_form")
        self.stackedWidget.addWidget(self.page_three)
        
        
        #Creación del stacked widget
        self.verticalLayout_3.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.frame_contenedor)
        self.verticalLayout.addWidget(self.frame_inferior)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Run\""))
        self.bt_menu.setText(_translate("MainWindow", "    MENU "))
        self.bt_inicio.setText(_translate("MainWindow", "       Inicio"))
        self.bt_uno.setText(_translate("MainWindow", "   Buscar"))
        self.bt_dos.setText(_translate("MainWindow", "    Listado"))
        self.bt_tres.setText(_translate("MainWindow", "    Formulario"))
        #self.bt_cuatro.setText(_translate("MainWindow", "     Links"))
        #self.bt_cinco.setText(_translate("MainWindow", "  CONECTIVIDAD"))
        #self.label_2.setText(_translate("MainWindow", "Run\"\n Press PLAY and then any key:"))
        self.label_2.setText(_translate("MainWindow", "<table width=\"100%\"><tr><td width=\"50%\" align=\"left\">Run\"</td></tr><tr><td width=\"50%\" align=\"right\">Press PLAY and then any key:</td></tr></table>"))                
        #self.pushButton.setText(_translate("MainWindow", "5"))

