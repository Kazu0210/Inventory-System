# Form implementation generated from reading ui file '.\activity_logs_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(791, 625)
        Form.setStyleSheet("*{\n"
"border: none;\n"
"font: 10pt \"Noto Sans\";\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=Form)
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
"                background: #90A4AE;\n"
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
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 774, 643))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents_2)
        self.frame.setStyleSheet("*{\n"
"background-color: transparent;\n"
"}\n"
"#frame{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QComboBox{\n"
"font: 10pt \"Inter\";\n"
"background-color: #fff;\n"
"border: 1px solid #228B22;\n"
"border-radius: 5px;\n"
"padding: 5px\n"
"}\n"
"QComboBox::drop-down{\n"
"border: none;\n"
"background: transparent;\n"
"}\n"
"QComboBox::down-arrow {\n"
"image: none;               \n"
"border: none;              \n"
"width: 0; height: 0;       \n"
"border-left: 5px solid none; \n"
"border-right: 5px solid none;\n"
"border-top: 7px solid #228B22; \n"
"margin: 0;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_2.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.categories_combobox = QtWidgets.QComboBox(parent=self.frame_3)
        self.categories_combobox.setMinimumSize(QtCore.QSize(140, 30))
        self.categories_combobox.setMaximumSize(QtCore.QSize(140, 30))
        self.categories_combobox.setStyleSheet("background-color: white;\n"
"color: black;")
        self.categories_combobox.setObjectName("categories_combobox")
        self.horizontalLayout_3.addWidget(self.categories_combobox)
        self.horizontalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_3.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.status_combobox = QtWidgets.QComboBox(parent=self.frame_4)
        self.status_combobox.setMinimumSize(QtCore.QSize(140, 30))
        self.status_combobox.setMaximumSize(QtCore.QSize(140, 30))
        self.status_combobox.setStyleSheet("background-color: white;\n"
"color: black;")
        self.status_combobox.setObjectName("status_combobox")
        self.horizontalLayout_4.addWidget(self.status_combobox)
        self.horizontalLayout.addWidget(self.frame_4, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.frame_5 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_2 = QtWidgets.QFrame(parent=self.frame_5)
        self.frame_2.setStyleSheet("*{\n"
"background-color: transparent;\n"
"}\n"
"#frame_2{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QComboBox{\n"
"font: 10pt \"Inter\";\n"
"background-color: #fff;\n"
"border: 1px solid #228B22;\n"
"border-radius: 5px;\n"
"padding: 5px\n"
"}\n"
"QComboBox::drop-down{\n"
"border: none;\n"
"background: transparent;\n"
"}\n"
"QComboBox::down-arrow {\n"
"image: none;               \n"
"border: none;              \n"
"width: 0; height: 0;       \n"
"border-left: 5px solid none; \n"
"border-right: 5px solid none;\n"
"border-top: 7px solid #228B22; \n"
"margin: 0;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.frame_7)
        self.label.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"color: #333333;")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.frame_2)
        self.tableWidget.setMinimumSize(QtCore.QSize(300, 500))
        self.tableWidget.setStyleSheet("#tableWidget{\n"
"border:none;\n"
"}")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.prev_pushButton = QtWidgets.QPushButton(parent=self.frame_6)
        self.prev_pushButton.setMinimumSize(QtCore.QSize(150, 30))
        self.prev_pushButton.setMaximumSize(QtCore.QSize(150, 30))
        self.prev_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.prev_pushButton.setStyleSheet("background-color: #fff;\n"
"border: 1px solid #000;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #1E1E1E;")
        self.prev_pushButton.setObjectName("prev_pushButton")
        self.horizontalLayout_5.addWidget(self.prev_pushButton)
        self.next_pushButton = QtWidgets.QPushButton(parent=self.frame_6)
        self.next_pushButton.setMinimumSize(QtCore.QSize(150, 30))
        self.next_pushButton.setMaximumSize(QtCore.QSize(150, 30))
        self.next_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.next_pushButton.setStyleSheet("background-color: #fff;\n"
"border: 1px solid #000;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #1E1E1E;")
        self.next_pushButton.setObjectName("next_pushButton")
        self.horizontalLayout_5.addWidget(self.next_pushButton)
        self.verticalLayout_4.addWidget(self.frame_6, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Activity:"))
        self.label_3.setText(_translate("Form", "Status:"))
        self.label.setText(_translate("Form", "Logs Table"))
        self.prev_pushButton.setText(_translate("Form", "Previous"))
        self.next_pushButton.setText(_translate("Form", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
