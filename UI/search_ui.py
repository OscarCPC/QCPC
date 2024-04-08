# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPlainTextEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_qcpc_search(object):
    def setupUi(self, qcpc_search):
        if not qcpc_search.objectName():
            qcpc_search.setObjectName(u"qcpc_search")
        qcpc_search.resize(1100, 950)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(qcpc_search.sizePolicy().hasHeightForWidth())
        qcpc_search.setSizePolicy(sizePolicy)
        qcpc_search.setMinimumSize(QSize(1100, 950))
        self.formLayout_2 = QFormLayout(qcpc_search)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(-1, -1, -1, 100)
        self.qcpc_frame_container = QFrame(qcpc_search)
        self.qcpc_frame_container.setObjectName(u"qcpc_frame_container")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.qcpc_frame_container.sizePolicy().hasHeightForWidth())
        self.qcpc_frame_container.setSizePolicy(sizePolicy1)
        self.qcpc_frame_container.setFrameShape(QFrame.StyledPanel)
        self.qcpc_frame_container.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.qcpc_frame_container)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.qcpc_input_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_input_frame.setObjectName(u"qcpc_input_frame")
        sizePolicy1.setHeightForWidth(self.qcpc_input_frame.sizePolicy().hasHeightForWidth())
        self.qcpc_input_frame.setSizePolicy(sizePolicy1)
        self.qcpc_input_frame.setLayoutDirection(Qt.RightToLeft)
        self.qcpc_input_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_input_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_input_layout = QFormLayout(self.qcpc_input_frame)
        self.qcpc_input_layout.setObjectName(u"qcpc_input_layout")
        self.qcpc_input_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.qcpc_input_layout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.qcpc_input_layout.setLabelAlignment(Qt.AlignCenter)
        self.qcpc_input_label = QLabel(self.qcpc_input_frame)
        self.qcpc_input_label.setObjectName(u"qcpc_input_label")
        sizePolicy1.setHeightForWidth(self.qcpc_input_label.sizePolicy().hasHeightForWidth())
        self.qcpc_input_label.setSizePolicy(sizePolicy1)
        self.qcpc_input_label.setMinimumSize(QSize(250, 0))
        self.qcpc_input_label.setMaximumSize(QSize(16777215, 16777211))
        self.qcpc_input_label.setAlignment(Qt.AlignCenter)

        self.qcpc_input_layout.setWidget(0, QFormLayout.FieldRole, self.qcpc_input_label)

        self.qcpc_input_text = QPlainTextEdit(self.qcpc_input_frame)
        self.qcpc_input_text.setObjectName(u"qcpc_input_text")
        self.qcpc_input_text.setMinimumSize(QSize(275, 30))
        self.qcpc_input_text.setMaximumSize(QSize(16777215, 30))

        self.qcpc_input_layout.setWidget(1, QFormLayout.FieldRole, self.qcpc_input_text)

        self.qcpc_input_output_text = QTextEdit(self.qcpc_input_frame)
        self.qcpc_input_output_text.setObjectName(u"qcpc_input_output_text")

        self.qcpc_input_layout.setWidget(5, QFormLayout.FieldRole, self.qcpc_input_output_text)

        self.qcpc_inner_input_layout = QHBoxLayout()
        self.qcpc_inner_input_layout.setObjectName(u"qcpc_inner_input_layout")
        self.qcpc_input_frame_save = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_save.setObjectName(u"qcpc_input_frame_save")
        self.qcpc_input_frame_save.setMinimumSize(QSize(275, 0))
        self.qcpc_input_frame_save.setLayoutDirection(Qt.RightToLeft)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_save)

        self.qcpc_input_frame_delete = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_frame_delete.setObjectName(u"qcpc_input_frame_delete")

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_frame_delete)

        self.qcpc_input_search = QPushButton(self.qcpc_input_frame)
        self.qcpc_input_search.setObjectName(u"qcpc_input_search")
        self.qcpc_input_search.setMinimumSize(QSize(80, 30))
        self.qcpc_input_search.setMaximumSize(QSize(80, 30))
        self.qcpc_input_search.setLayoutDirection(Qt.LeftToRight)

        self.qcpc_inner_input_layout.addWidget(self.qcpc_input_search)


        self.qcpc_input_layout.setLayout(4, QFormLayout.SpanningRole, self.qcpc_inner_input_layout)


        self.gridLayout_2.addWidget(self.qcpc_input_frame, 0, 0, 1, 1)

        self.qcpc_result_frame = QFrame(self.qcpc_frame_container)
        self.qcpc_result_frame.setObjectName(u"qcpc_result_frame")
        self.qcpc_result_frame.setStyleSheet(u"background-color: rgb(53, 39, 255);")
        self.qcpc_result_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_result_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.qcpc_result_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.qcpc_result_table = QListWidget(self.qcpc_result_frame)
        self.qcpc_result_table.setObjectName(u"qcpc_result_table")

        self.verticalLayout.addWidget(self.qcpc_result_table)

        self.qcpc_result_label = QLabel(self.qcpc_result_frame)
        self.qcpc_result_label.setObjectName(u"qcpc_result_label")
        self.qcpc_result_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.qcpc_result_label)


        self.gridLayout_2.addWidget(self.qcpc_result_frame, 1, 0, 1, 1)


        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.qcpc_frame_container)

        self.qcpc_image_frame = QFrame(qcpc_search)
        self.qcpc_image_frame.setObjectName(u"qcpc_image_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.qcpc_image_frame.sizePolicy().hasHeightForWidth())
        self.qcpc_image_frame.setSizePolicy(sizePolicy2)
        self.qcpc_image_frame.setMinimumSize(QSize(463, 900))
        self.qcpc_image_frame.setMaximumSize(QSize(16777215, 16777215))
        self.qcpc_image_frame.setStyleSheet(u"background-color: red;")
        self.qcpc_image_frame.setFrameShape(QFrame.StyledPanel)
        self.qcpc_image_frame.setFrameShadow(QFrame.Raised)
        self.qcpc_image_frame.setLineWidth(20)
        self.horizontalLayout = QHBoxLayout(self.qcpc_image_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(8, 8, 8, 8)
        self.qcpc_image_label = QLabel(self.qcpc_image_frame)
        self.qcpc_image_label.setObjectName(u"qcpc_image_label")
        sizePolicy1.setHeightForWidth(self.qcpc_image_label.sizePolicy().hasHeightForWidth())
        self.qcpc_image_label.setSizePolicy(sizePolicy1)
        self.qcpc_image_label.setMinimumSize(QSize(400, 800))
        self.qcpc_image_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.qcpc_image_label)


        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.qcpc_image_frame)


        self.retranslateUi(qcpc_search)

        QMetaObject.connectSlotsByName(qcpc_search)
    # setupUi

    def retranslateUi(self, qcpc_search):
        qcpc_search.setWindowTitle(QCoreApplication.translate("qcpc_search", u"Form", None))
        self.qcpc_input_label.setText(QCoreApplication.translate("qcpc_search", u"Titulo a buscar", None))
        self.qcpc_input_frame_save.setText(QCoreApplication.translate("qcpc_search", u"Guardar Selecci\u00f3n", None))
        self.qcpc_input_frame_delete.setText(QCoreApplication.translate("qcpc_search", u"Borrar", None))
        self.qcpc_input_search.setText(QCoreApplication.translate("qcpc_search", u"Buscar", None))
        self.qcpc_result_label.setText(QCoreApplication.translate("qcpc_search", u"Resultados", None))
        self.qcpc_image_label.setText(QCoreApplication.translate("qcpc_search", u"Imagen", None))
    # retranslateUi

