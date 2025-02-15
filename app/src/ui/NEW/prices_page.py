# Form implementation generated from reading ui file 'prices_page.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(854, 835)
        Form.setStyleSheet("font: 10pt \"Noto Sans\";")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setAutoFillBackground(False)
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 901, 1307))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.frame_6)
        self.label.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"    ")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_6)
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
        self.searchBar_lineEdit.setStyleSheet("color: #000;\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"padding: 0px 5px;\n"
"font: 10pt \"Noto Sans\";")
        self.searchBar_lineEdit.setObjectName("searchBar_lineEdit")
        self.horizontalLayout_3.addWidget(self.searchBar_lineEdit, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.search_pushButton = QtWidgets.QPushButton(parent=self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_pushButton.sizePolicy().hasHeightForWidth())
        self.search_pushButton.setSizePolicy(sizePolicy)
        self.search_pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.search_pushButton.setMaximumSize(QtCore.QSize(120, 30))
        self.search_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_pushButton.setStyleSheet("background-color: #274D60;\n"
"border-radius: 5px;\n"
"color: #fff;\n"
"font: 87 10pt \"Noto Sans Black\";")
        self.search_pushButton.setObjectName("search_pushButton")
        self.horizontalLayout_3.addWidget(self.search_pushButton, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.horizontalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.prices_tableWidget = QtWidgets.QTableWidget(parent=self.frame_7)
        self.prices_tableWidget.setMinimumSize(QtCore.QSize(883, 550))
        self.prices_tableWidget.setMaximumSize(QtCore.QSize(16777215, 550))
        self.prices_tableWidget.setStyleSheet("#prices_tableWidget{\n"
"border: none;\n"
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
        self.prices_tableWidget.setObjectName("prices_tableWidget")
        self.prices_tableWidget.setColumnCount(0)
        self.prices_tableWidget.setRowCount(0)
        self.verticalLayout_6.addWidget(self.prices_tableWidget, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.frame = QtWidgets.QFrame(parent=self.frame_2)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setStyleSheet("QPushButton{\n"
"background-color: #597784;\n"
"border-radius: 5px;\n"
"color: #fff;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.prev_pushButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.prev_pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.prev_pushButton.setMaximumSize(QtCore.QSize(120, 30))
        self.prev_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prev_pushButton.setObjectName("prev_pushButton")
        self.horizontalLayout_2.addWidget(self.prev_pushButton, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.next_pushButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.next_pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.next_pushButton.setMaximumSize(QtCore.QSize(120, 30))
        self.next_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.next_pushButton.setObjectName("next_pushButton")
        self.horizontalLayout_2.addWidget(self.next_pushButton, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.frame_3, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_4.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_2.addWidget(self.frame_2, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_5 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.frame_5.setStyleSheet("border: none;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_5)
        self.frame_8.setMinimumSize(QtCore.QSize(0, 32))
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame_8.setStyleSheet("QPushButton{\n"
"background-color: #274D60;\n"
"border-radius: 5px;\n"
"color: #fff;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.price_history_pushButton = QtWidgets.QPushButton(parent=self.frame_8)
        self.price_history_pushButton.setMinimumSize(QtCore.QSize(140, 30))
        self.price_history_pushButton.setMaximumSize(QtCore.QSize(140, 30))
        self.price_history_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.price_history_pushButton.setObjectName("price_history_pushButton")
        self.horizontalLayout_4.addWidget(self.price_history_pushButton, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_5.addWidget(self.frame_8, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_11 = QtWidgets.QFrame(parent=self.frame_5)
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_10.setMinimumSize(QtCore.QSize(0, 36))
        self.frame_10.setMaximumSize(QtCore.QSize(16777215, 36))
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_10)
        self.label_2.setStyleSheet("font: 87 16pt \"Noto Sans Black\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_8.addWidget(self.frame_10)
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 520))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.price_history_tableWidget = QtWidgets.QTableWidget(parent=self.frame_9)
        self.price_history_tableWidget.setMinimumSize(QtCore.QSize(580, 500))
        self.price_history_tableWidget.setMaximumSize(QtCore.QSize(16777215, 500))
        self.price_history_tableWidget.setStyleSheet("            QScrollBar:vertical {\n"
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
        self.verticalLayout_7.addWidget(self.price_history_tableWidget, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_8.addWidget(self.frame_9)
        self.verticalLayout_5.addWidget(self.frame_11)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Prices"))
        self.searchBar_lineEdit.setPlaceholderText(_translate("Form", "Type Product ID or Product Name Here"))
        self.search_pushButton.setText(_translate("Form", "Search"))
        self.prev_pushButton.setText(_translate("Form", "Previous"))
        self.next_pushButton.setText(_translate("Form", "Next"))
        self.price_history_pushButton.setText(_translate("Form", "View Price History"))
        self.label_2.setText(_translate("Form", "Price History"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
