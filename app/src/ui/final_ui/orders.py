# Form implementation generated from reading ui file '.\orders.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(769, 486)
        Form.setStyleSheet("*{\n"
"color: #333333;\n"
"font: 10pt \"Noto Sans\";\n"
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(parent=Form)
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 769, 486))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(5)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame_2 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(parent=self.frame_2)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setStyleSheet("font: 87 16pt \"Noto Sans Black\";\n"
"color: #333333;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_5.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_3.setStyleSheet("#frame_3{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.view_order_pushButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.view_order_pushButton.setMinimumSize(QtCore.QSize(125, 30))
        self.view_order_pushButton.setMaximumSize(QtCore.QSize(125, 30))
        self.view_order_pushButton.setStyleSheet("background-color: #32CD32;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #fff;\n"
"border: none;\n"
"border-radius: 5px;")
        self.view_order_pushButton.setObjectName("view_order_pushButton")
        self.horizontalLayout_2.addWidget(self.view_order_pushButton)
        self.order_history_pushButton = QtWidgets.QPushButton(parent=self.frame_3)
        self.order_history_pushButton.setMinimumSize(QtCore.QSize(125, 30))
        self.order_history_pushButton.setMaximumSize(QtCore.QSize(125, 30))
        self.order_history_pushButton.setStyleSheet("background-color: #fff;\n"
"border: 1px solid #000;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #1E1E1E;")
        self.order_history_pushButton.setObjectName("order_history_pushButton")
        self.horizontalLayout_2.addWidget(self.order_history_pushButton)
        self.verticalLayout_5.addWidget(self.frame_3, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.frame_18 = QtWidgets.QFrame(parent=self.frame_2)
        self.frame_18.setStyleSheet("#frame_18{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_18.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_18)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_10)
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_2.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.name_input = QtWidgets.QLineEdit(parent=self.frame_4)
        self.name_input.setMinimumSize(QtCore.QSize(200, 30))
        self.name_input.setMaximumSize(QtCore.QSize(200, 30))
        self.name_input.setObjectName("name_input")
        self.horizontalLayout_4.addWidget(self.name_input)
        self.name_input.raise_()
        self.label_2.raise_()
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(parent=self.frame_5)
        self.label_4.setMinimumSize(QtCore.QSize(150, 0))
        self.label_4.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_4.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.productName_comboBox = QtWidgets.QComboBox(parent=self.frame_5)
        self.productName_comboBox.setMinimumSize(QtCore.QSize(200, 30))
        self.productName_comboBox.setMaximumSize(QtCore.QSize(200, 30))
        self.productName_comboBox.setObjectName("productName_comboBox")
        self.horizontalLayout_5.addWidget(self.productName_comboBox)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(parent=self.frame_6)
        self.label_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_5.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.cylindersize_box = QtWidgets.QComboBox(parent=self.frame_6)
        self.cylindersize_box.setMinimumSize(QtCore.QSize(200, 30))
        self.cylindersize_box.setMaximumSize(QtCore.QSize(200, 30))
        self.cylindersize_box.setObjectName("cylindersize_box")
        self.horizontalLayout_6.addWidget(self.cylindersize_box)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(parent=self.frame_7)
        self.label_6.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_6.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.quantity_box = QtWidgets.QSpinBox(parent=self.frame_7)
        self.quantity_box.setMinimumSize(QtCore.QSize(200, 30))
        self.quantity_box.setMaximumSize(QtCore.QSize(200, 30))
        self.quantity_box.setObjectName("quantity_box")
        self.horizontalLayout_7.addWidget(self.quantity_box)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(parent=self.frame_8)
        self.label_7.setMinimumSize(QtCore.QSize(150, 0))
        self.label_7.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_7.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.payment_box = QtWidgets.QComboBox(parent=self.frame_8)
        self.payment_box.setMinimumSize(QtCore.QSize(200, 30))
        self.payment_box.setMaximumSize(QtCore.QSize(200, 30))
        self.payment_box.setObjectName("payment_box")
        self.horizontalLayout_8.addWidget(self.payment_box)
        self.verticalLayout_2.addWidget(self.frame_8)
        self.frame_20 = QtWidgets.QFrame(parent=self.frame_9)
        self.frame_20.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setSpacing(5)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_20)
        self.label_3.setMinimumSize(QtCore.QSize(150, 0))
        self.label_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_3.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_16.addWidget(self.label_3)
        self.label_13 = QtWidgets.QLabel(parent=self.frame_20)
        self.label_13.setMinimumSize(QtCore.QSize(0, 30))
        self.label_13.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_16.addWidget(self.label_13)
        self.verticalLayout_2.addWidget(self.frame_20)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_9.addWidget(self.frame_9, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.frame_11 = QtWidgets.QFrame(parent=self.frame_10)
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_12 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(5)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(parent=self.frame_12)
        self.label_8.setMinimumSize(QtCore.QSize(150, 0))
        self.label_8.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_8.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.status_box = QtWidgets.QComboBox(parent=self.frame_12)
        self.status_box.setMinimumSize(QtCore.QSize(200, 30))
        self.status_box.setMaximumSize(QtCore.QSize(200, 30))
        self.status_box.setObjectName("status_box")
        self.horizontalLayout_10.addWidget(self.status_box)
        self.verticalLayout_3.addWidget(self.frame_12)
        self.frame_15 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_15.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(5)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_12 = QtWidgets.QLabel(parent=self.frame_15)
        self.label_12.setMinimumSize(QtCore.QSize(150, 0))
        self.label_12.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_12.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_11.addWidget(self.label_12)
        self.contact_info = QtWidgets.QLineEdit(parent=self.frame_15)
        self.contact_info.setMinimumSize(QtCore.QSize(200, 30))
        self.contact_info.setMaximumSize(QtCore.QSize(200, 30))
        self.contact_info.setObjectName("contact_info")
        self.horizontalLayout_11.addWidget(self.contact_info)
        self.verticalLayout_3.addWidget(self.frame_15)
        self.frame_14 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_14.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(5)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_10 = QtWidgets.QLabel(parent=self.frame_14)
        self.label_10.setMinimumSize(QtCore.QSize(150, 0))
        self.label_10.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_10.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_12.addWidget(self.label_10, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.note_input = QtWidgets.QPlainTextEdit(parent=self.frame_14)
        self.note_input.setMinimumSize(QtCore.QSize(200, 65))
        self.note_input.setMaximumSize(QtCore.QSize(200, 120))
        self.note_input.setObjectName("note_input")
        self.horizontalLayout_12.addWidget(self.note_input)
        self.verticalLayout_3.addWidget(self.frame_14)
        self.frame_13 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_13.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setSpacing(5)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_9 = QtWidgets.QLabel(parent=self.frame_13)
        self.label_9.setMinimumSize(QtCore.QSize(150, 0))
        self.label_9.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_9.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_13.addWidget(self.label_9)
        self.price_input = QtWidgets.QLineEdit(parent=self.frame_13)
        self.price_input.setMinimumSize(QtCore.QSize(200, 30))
        self.price_input.setMaximumSize(QtCore.QSize(200, 30))
        self.price_input.setObjectName("price_input")
        self.horizontalLayout_13.addWidget(self.price_input)
        self.verticalLayout_3.addWidget(self.frame_13)
        self.frame_16 = QtWidgets.QFrame(parent=self.frame_11)
        self.frame_16.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setSpacing(5)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_11 = QtWidgets.QLabel(parent=self.frame_16)
        self.label_11.setMinimumSize(QtCore.QSize(150, 0))
        self.label_11.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_11.setStyleSheet("font: 63 10pt \"Noto Sans SemiBold\";")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_14.addWidget(self.label_11)
        self.amount_input = QtWidgets.QLineEdit(parent=self.frame_16)
        self.amount_input.setMinimumSize(QtCore.QSize(200, 30))
        self.amount_input.setMaximumSize(QtCore.QSize(200, 30))
        self.amount_input.setObjectName("amount_input")
        self.horizontalLayout_14.addWidget(self.amount_input)
        self.verticalLayout_3.addWidget(self.frame_16)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_9.addWidget(self.frame_11, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout_4.addWidget(self.frame_10)
        self.frame_17 = QtWidgets.QFrame(parent=self.frame_18)
        self.frame_17.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(5)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.addItem_btn = QtWidgets.QPushButton(parent=self.frame_17)
        self.addItem_btn.setMinimumSize(QtCore.QSize(125, 30))
        self.addItem_btn.setMaximumSize(QtCore.QSize(125, 30))
        self.addItem_btn.setStyleSheet("background-color: #32CD32;\n"
"font: 87 10pt \"Noto Sans Black\";\n"
"color: #fff;\n"
"border: none;\n"
"border-radius: 5px;")
        self.addItem_btn.setObjectName("addItem_btn")
        self.horizontalLayout_15.addWidget(self.addItem_btn)
        self.cancelItem_btn = QtWidgets.QPushButton(parent=self.frame_17)
        self.cancelItem_btn.setMinimumSize(QtCore.QSize(125, 30))
        self.cancelItem_btn.setMaximumSize(QtCore.QSize(125, 30))
        self.cancelItem_btn.setStyleSheet("background-color: #DC3545;\n"
"font: 87 12pt \"Noto Sans Black\";\n"
"color: #fff;\n"
"border-radius: 5px;")
        self.cancelItem_btn.setObjectName("cancelItem_btn")
        self.horizontalLayout_15.addWidget(self.cancelItem_btn)
        self.verticalLayout_4.addWidget(self.frame_17, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.verticalLayout_5.addWidget(self.frame_18)
        self.horizontalLayout_17.addWidget(self.frame_2)
        self.frame_19 = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.frame_19.setStyleSheet("#frame_19{\n"
"background-color: #fff;\n"
"border-radius: 5px;\n"
"}")
        self.frame_19.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_19.setObjectName("frame_19")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_19)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_17.addWidget(self.frame_19)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Orders"))
        self.view_order_pushButton.setText(_translate("Form", "View Orders"))
        self.order_history_pushButton.setText(_translate("Form", "Order History"))
        self.label_2.setText(_translate("Form", "Customer Name:"))
        self.label_4.setText(_translate("Form", "Product:"))
        self.label_5.setText(_translate("Form", "Cylinder Size:"))
        self.label_6.setText(_translate("Form", "Quantity:"))
        self.label_7.setText(_translate("Form", "Payment Status:"))
        self.label_3.setText(_translate("Form", "Order Date:"))
        self.label_13.setText(_translate("Form", "TextLabel"))
        self.label_8.setText(_translate("Form", "Order Status:"))
        self.label_12.setText(_translate("Form", "Contact:"))
        self.label_10.setText(_translate("Form", "Remarks:"))
        self.label_9.setText(_translate("Form", "Price:"))
        self.label_11.setText(_translate("Form", "Total Amount:"))
        self.addItem_btn.setText(_translate("Form", "Create"))
        self.cancelItem_btn.setText(_translate("Form", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
