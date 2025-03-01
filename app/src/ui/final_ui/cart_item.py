# Form implementation generated from reading ui file 'cart_item.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(314, 190)
        Frame.setMinimumSize(QtCore.QSize(150, 190))
        Frame.setStyleSheet("#Frame{\n"
"font: 10pt \"Noto Sans\";\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}\n"
"*{\n"
"background-color: transparent;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(parent=Frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_6.setMinimumSize(QtCore.QSize(100, 0))
        self.label_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_6.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.product_name_label = QtWidgets.QLabel(parent=self.frame_7)
        self.product_name_label.setStyleSheet("font: 10pt \"Noto Sans\";")
        self.product_name_label.setObjectName("product_name_label")
        self.horizontalLayout_6.addWidget(self.product_name_label)
        self.frame_11 = QtWidgets.QFrame(parent=self.frame_7)
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.remove_pushButton = QtWidgets.QPushButton(parent=self.frame_11)
        self.remove_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.remove_pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../resources/icons/black-theme/trash-bin.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.remove_pushButton.setIcon(icon)
        self.remove_pushButton.setObjectName("remove_pushButton")
        self.horizontalLayout_9.addWidget(self.remove_pushButton)
        self.horizontalLayout_6.addWidget(self.frame_11, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_4.setMinimumSize(QtCore.QSize(100, 0))
        self.label_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_4.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.cylinder_size_label = QtWidgets.QLabel(parent=self.frame_4)
        self.cylinder_size_label.setStyleSheet("font: 10pt \"Noto Sans\";")
        self.cylinder_size_label.setObjectName("cylinder_size_label")
        self.horizontalLayout_3.addWidget(self.cylinder_size_label)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_8)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_3.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_8.addWidget(self.label_3)
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_8)
        self.frame_9.setStyleSheet("#frame_8{\n"
"border: 1px solid #000;\n"
"}")
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.decrement_pushButton = QtWidgets.QPushButton(parent=self.frame_9)
        self.decrement_pushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.decrement_pushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.decrement_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.decrement_pushButton.setStyleSheet("background-color: #EAEAEA;\n"
"border: none;")
        self.decrement_pushButton.setObjectName("decrement_pushButton")
        self.horizontalLayout_7.addWidget(self.decrement_pushButton)
        self.quantity_lineEdit = QtWidgets.QLineEdit(parent=self.frame_9)
        self.quantity_lineEdit.setMaximumSize(QtCore.QSize(30, 30))
        self.quantity_lineEdit.setStyleSheet("border: none;")
        self.quantity_lineEdit.setObjectName("quantity_lineEdit")
        self.horizontalLayout_7.addWidget(self.quantity_lineEdit, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.increment_pushButton = QtWidgets.QPushButton(parent=self.frame_9)
        self.increment_pushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.increment_pushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.increment_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.increment_pushButton.setStyleSheet("background-color: #EAEAEA;\n"
"border: none;")
        self.increment_pushButton.setObjectName("increment_pushButton")
        self.horizontalLayout_7.addWidget(self.increment_pushButton)
        self.horizontalLayout_8.addWidget(self.frame_9, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_3.addWidget(self.frame_8)
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=self.frame_10)
        self.label_5.setMinimumSize(QtCore.QSize(100, 0))
        self.label_5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_5.setStyleSheet("font: 10pt \"Noto Sans\";\n"
"color: #808080;")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.available_quantity_label = QtWidgets.QLabel(parent=self.frame_10)
        self.available_quantity_label.setStyleSheet("font: 10pt \"Noto Sans\";\n"
"color: #808080;")
        self.available_quantity_label.setObjectName("available_quantity_label")
        self.horizontalLayout_5.addWidget(self.available_quantity_label)
        self.verticalLayout_3.addWidget(self.frame_10)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame = QtWidgets.QFrame(parent=self.frame_3)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.unit_price_label = QtWidgets.QLabel(parent=self.frame)
        self.unit_price_label.setStyleSheet("font: 10pt \"Noto Sans\";")
        self.unit_price_label.setObjectName("unit_price_label")
        self.horizontalLayout_2.addWidget(self.unit_price_label)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_5 = QtWidgets.QFrame(parent=self.frame_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_5)
        self.label_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_2.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";\n"
"color: #333333;")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.total_price_label = QtWidgets.QLabel(parent=self.frame_5)
        self.total_price_label.setStyleSheet("font: 10pt \"Noto Sans\";\n"
"color: #228B22;")
        self.total_price_label.setObjectName("total_price_label")
        self.horizontalLayout_4.addWidget(self.total_price_label)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_6.setText(_translate("Frame", "Product Name:"))
        self.product_name_label.setText(_translate("Frame", "Cylinder"))
        self.label_4.setText(_translate("Frame", "Cylinder Size:"))
        self.cylinder_size_label.setText(_translate("Frame", "0kg"))
        self.label_3.setText(_translate("Frame", "Quantity:"))
        self.decrement_pushButton.setText(_translate("Frame", "-"))
        self.increment_pushButton.setText(_translate("Frame", "+"))
        self.label_5.setText(_translate("Frame", "Available:"))
        self.available_quantity_label.setText(_translate("Frame", "0"))
        self.label.setText(_translate("Frame", "Unit Price:"))
        self.unit_price_label.setText(_translate("Frame", "TextLabel"))
        self.label_2.setText(_translate("Frame", "Total Price:"))
        self.total_price_label.setText(_translate("Frame", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec())
