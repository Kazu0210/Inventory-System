# Form implementation generated from reading ui file 'new_brand_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 691)
        Form.setMinimumSize(QtCore.QSize(450, 500))
        Form.setMaximumSize(QtCore.QSize(450, 16777215))
        Form.setStyleSheet("*{\n"
"font: 10pt \"Noto Sans\";\n"
"color: #1E1E1E;\n"
"background-color: transparent;\n"
"border: none;\n"
"}\n"
"#Form{\n"
"background-color: #E0F2E9;\n"
"}\n"
"QLineEdit, QPlainTextEdit{\n"
"border: 1px solid #000;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"background-color: #fff;\n"
"}\n"
"QComboBox{\n"
"font: 10pt \"Inter\";\n"
"background-color: #fff;\n"
"border: 1px solid #000;\n"
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
"}\n"
"QSpinBox{\n"
"border: 1px solid #000;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"color: #333333;\n"
"background-color: transparent;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_2 = QtWidgets.QFrame(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("#frame_2{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.brand_lineEdit = QtWidgets.QLineEdit(parent=self.frame_2)
        self.brand_lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.brand_lineEdit.setMaximumSize(QtCore.QSize(200, 30))
        self.brand_lineEdit.setObjectName("brand_lineEdit")
        self.horizontalLayout_2.addWidget(self.brand_lineEdit)
        self.supplier_lineEdit = QtWidgets.QLineEdit(parent=self.frame_2)
        self.supplier_lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.supplier_lineEdit.setMaximumSize(QtCore.QSize(200, 30))
        self.supplier_lineEdit.setObjectName("supplier_lineEdit")
        self.horizontalLayout_2.addWidget(self.supplier_lineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_3 = QtWidgets.QFrame(parent=Form)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 300))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 300))
        self.frame_3.setStyleSheet("#frame_3{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.product_selection_tableWidget = QtWidgets.QTableWidget(parent=self.frame_3)
        self.product_selection_tableWidget.setStyleSheet("*{\n"
"font: 10pt \"Noto Sans\";\n"
"}\n"
"QTableWidget{\n"
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
"}")
        self.product_selection_tableWidget.setObjectName("product_selection_tableWidget")
        self.product_selection_tableWidget.setColumnCount(0)
        self.product_selection_tableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.product_selection_tableWidget)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_17 = QtWidgets.QFrame(parent=Form)
        self.frame_17.setStyleSheet("#frame_17{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_17.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_18 = QtWidgets.QFrame(parent=self.frame_17)
        self.frame_18.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(5)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_7 = QtWidgets.QLabel(parent=self.frame_18)
        self.label_7.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_7.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_11.addWidget(self.label_7)
        self.description_plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.frame_18)
        self.description_plainTextEdit.setMinimumSize(QtCore.QSize(0, 100))
        self.description_plainTextEdit.setPlainText("")
        self.description_plainTextEdit.setObjectName("description_plainTextEdit")
        self.verticalLayout_11.addWidget(self.description_plainTextEdit)
        self.verticalLayout_10.addWidget(self.frame_18)
        self.frame_19 = QtWidgets.QFrame(parent=self.frame_17)
        self.frame_19.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(parent=self.frame_19)
        self.label_8.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_8.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.status_comboBox = QtWidgets.QComboBox(parent=self.frame_19)
        self.status_comboBox.setMinimumSize(QtCore.QSize(200, 30))
        self.status_comboBox.setMaximumSize(QtCore.QSize(200, 30))
        self.status_comboBox.setObjectName("status_comboBox")
        self.horizontalLayout_9.addWidget(self.status_comboBox)
        self.verticalLayout_10.addWidget(self.frame_19)
        self.frame_20 = QtWidgets.QFrame(parent=self.frame_17)
        self.frame_20.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtWidgets.QLabel(parent=self.frame_20)
        self.label_9.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_9.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.low_stock_threshold_spinBox = QtWidgets.QSpinBox(parent=self.frame_20)
        self.low_stock_threshold_spinBox.setMinimumSize(QtCore.QSize(200, 30))
        self.low_stock_threshold_spinBox.setMaximumSize(QtCore.QSize(200, 30))
        self.low_stock_threshold_spinBox.setObjectName("low_stock_threshold_spinBox")
        self.horizontalLayout_10.addWidget(self.low_stock_threshold_spinBox)
        self.verticalLayout_10.addWidget(self.frame_20)
        self.verticalLayout.addWidget(self.frame_17)
        self.frame_21 = QtWidgets.QFrame(parent=Form)
        self.frame_21.setStyleSheet("#frame_21{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_21.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_21)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.confirm_pushButton = QtWidgets.QPushButton(parent=self.frame_21)
        self.confirm_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.confirm_pushButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.confirm_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.confirm_pushButton.setStyleSheet("background-color: #228B22;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.confirm_pushButton.setObjectName("confirm_pushButton")
        self.horizontalLayout_11.addWidget(self.confirm_pushButton)
        self.cancel_pushButton = QtWidgets.QPushButton(parent=self.frame_21)
        self.cancel_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.cancel_pushButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cancel_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.cancel_pushButton.setStyleSheet("background-color: #DC3545;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.horizontalLayout_11.addWidget(self.cancel_pushButton)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 1)
        self.verticalLayout.addWidget(self.frame_21)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Add New Brand:"))
        self.brand_lineEdit.setPlaceholderText(_translate("Form", "Brand"))
        self.supplier_lineEdit.setPlaceholderText(_translate("Form", "Supplier"))
        self.label_7.setText(_translate("Form", "DESCRIPTION"))
        self.description_plainTextEdit.setPlaceholderText(_translate("Form", "Description"))
        self.label_8.setText(_translate("Form", "STATUS"))
        self.label_9.setText(_translate("Form", "LOW STOCK THRESHOLD"))
        self.confirm_pushButton.setText(_translate("Form", "CONFIRM"))
        self.cancel_pushButton.setText(_translate("Form", "CANCEL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())