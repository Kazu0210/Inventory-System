# Form implementation generated from reading ui file '.\prices_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(878, 671)
        Form.setStyleSheet("font: 10pt \"Noto Sans\";")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet("#scrollArea{\n"
"border: none;\n"
"}\n"
"QScrollBar:hover{\n"
" cursor: pointer;\n"
"}\n"
"            QScrollBar:vertical {\n"
"                border: none;\n"
"                background: #F0F0F0;\n"
"                width: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:vertical {\n"
"                background: #90A4AE;\n"
"                border-radius: 7px;\n"
"                min-height: 30px;\n"
"            }\n"
"            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"                height: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"                background: #F0F0F0;\n"
"            }\n"
"            QScrollBar:horizontal {\n"
"                border: none;\n"
"                background: #f0f0f0;\n"
"                height: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:horizontal {\n"
"                background: #F0F0F0;\n"
"                border-radius: 7px;\n"
"                min-width: 14px;\n"
"            }\n"
"            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"                width: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"                background: #f0f0f0;\n"
"            }")
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1055, 657))
        self.scrollAreaWidgetContents.setStyleSheet("border: none;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_7 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QtCore.QSize(525, 525))
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_7.setStyleSheet("#frame_7{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_7)
        self.frame_6.setStyleSheet("#frame_6{\n"
"background-color: transparent;\n"
"}")
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_12 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_12.setStyleSheet("*{\n"
"background-color: transparent;\n"
"}")
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(parent=self.frame_12)
        self.label.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"color: #333333;")
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_12, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_4.setStyleSheet("border: 1px solid #000;\n"
"border-radius: 5px;\n"
"background-color: #fff;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchBar_lineEdit = QtWidgets.QLineEdit(parent=self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBar_lineEdit.sizePolicy().hasHeightForWidth())
        self.searchBar_lineEdit.setSizePolicy(sizePolicy)
        self.searchBar_lineEdit.setMinimumSize(QtCore.QSize(260, 30))
        self.searchBar_lineEdit.setMaximumSize(QtCore.QSize(350, 30))
        self.searchBar_lineEdit.setStyleSheet("border: none;\n"
"padding: 5px;\n"
"color: #000;")
        self.searchBar_lineEdit.setObjectName("searchBar_lineEdit")
        self.horizontalLayout_3.addWidget(self.searchBar_lineEdit, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.search_pushButton = QtWidgets.QPushButton(parent=self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_pushButton.sizePolicy().hasHeightForWidth())
        self.search_pushButton.setSizePolicy(sizePolicy)
        self.search_pushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.search_pushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.search_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_pushButton.setStyleSheet("border: none;\n"
"background-color: #fff;")
        self.search_pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(".\\../../../resources/icons/black-theme/search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.search_pushButton.setIcon(icon)
        self.search_pushButton.setObjectName("search_pushButton")
        self.horizontalLayout_3.addWidget(self.search_pushButton, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.horizontalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_6.addWidget(self.frame_6, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.prices_tableWidget = QtWidgets.QTableWidget(parent=self.frame_7)
        self.prices_tableWidget.setStyleSheet("#prices_tableWidget{\n"
"color: #000;\n"
"}\n"
"#prices_tableWidget{\n"
"border: none;\n"
"gridline-color: transparent;\n"
"}\n"
"QHeaderView{\n"
"background-color: #228B22;\n"
"}\n"
"QHeaderView::section {\n"
"background-color: #228B22;\n"
"color: #fff;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"}\n"
"            QScrollBar:vertical {\n"
"                border: none;\n"
"                background: #F0F0F0;\n"
"                width: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:vertical {\n"
"                background: #90A4AE;\n"
"                border-radius: 7px;\n"
"                min-height: 30px;\n"
"            }\n"
"            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"                height: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"                background: #11B3BE;\n"
"            }\n"
"            QScrollBar:horizontal {\n"
"                border: none;\n"
"                background: #F0F0F0;\n"
"                height: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:horizontal {\n"
"                background: #90A4AE;\n"
"                border-radius: 7px;\n"
"                min-width: 30px;\n"
"            }\n"
"            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"                width: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"                background: #f0f0f0;\n"
"            }")
        self.prices_tableWidget.setObjectName("prices_tableWidget")
        self.prices_tableWidget.setColumnCount(0)
        self.prices_tableWidget.setRowCount(0)
        self.verticalLayout_6.addWidget(self.prices_tableWidget)
        self.horizontalLayout_2.addWidget(self.frame_7)
        self.frame_9 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.frame_9.setMinimumSize(QtCore.QSize(525, 525))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_9.setStyleSheet("#frame_9{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_7.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 36))
        self.frame_10.setMaximumSize(QtCore.QSize(16777215, 36))
        self.frame_10.setStyleSheet("background-color: transparent;")
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_10)
        self.label_2.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"color: #000;\n"
"")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_7.addWidget(self.frame_10)
        self.price_history_tableWidget = QtWidgets.QTableWidget(parent=self.frame_9)
        self.price_history_tableWidget.setStyleSheet("\n"
"#prices_tableWidget{\n"
"border: none;\n"
"gridline-color: transparent;\n"
"}\n"
"QHeaderView{\n"
"background-color: #228B22;\n"
"}\n"
"QHeaderView::section {\n"
"background-color: #228B22;\n"
"color: #fff;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"}\n"
"            QScrollBar:vertical {\n"
"                border: none;\n"
"                background: #11B3BE;\n"
"                width: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:vertical {\n"
"                background: #002E2C;\n"
"                border-radius: 7px;\n"
"                min-height: 30px;\n"
"            }\n"
"            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"                height: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"                background: #11B3BE;\n"
"            }\n"
"            QScrollBar:horizontal {\n"
"                border: none;\n"
"                background: #f0f0f0;\n"
"                height: 14px;\n"
"                margin: 0px 0px 0px 0px;\n"
"            }\n"
"            QScrollBar::handle:horizontal {\n"
"                background: #555;\n"
"                border-radius: 7px;\n"
"                min-width: 30px;\n"
"            }\n"
"            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"                width: 0px;\n"
"                background: none;\n"
"            }\n"
"            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"                background: #f0f0f0;\n"
"            }")
        self.price_history_tableWidget.setObjectName("price_history_tableWidget")
        self.price_history_tableWidget.setColumnCount(0)
        self.price_history_tableWidget.setRowCount(0)
        self.verticalLayout_7.addWidget(self.price_history_tableWidget)
        self.horizontalLayout_2.addWidget(self.frame_9)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Prices"))
        self.searchBar_lineEdit.setPlaceholderText(_translate("Form", "Type Cylinder Size or Product Name Here"))
        self.label_2.setText(_translate("Form", "Price History"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())