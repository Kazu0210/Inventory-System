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
        Form.resize(640, 480)
        self.prices_tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.prices_tableWidget.setGeometry(QtCore.QRect(10, 40, 621, 192))
        self.prices_tableWidget.setObjectName("prices_tableWidget")
        self.prices_tableWidget.setColumnCount(0)
        self.prices_tableWidget.setRowCount(0)
        self.searchBar_lineEdit = QtWidgets.QLineEdit(parent=Form)
        self.searchBar_lineEdit.setGeometry(QtCore.QRect(10, 10, 271, 20))
        self.searchBar_lineEdit.setObjectName("searchBar_lineEdit")
        self.search_pushButton = QtWidgets.QPushButton(parent=Form)
        self.search_pushButton.setGeometry(QtCore.QRect(290, 10, 75, 23))
        self.search_pushButton.setObjectName("search_pushButton")
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 240, 111, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.searchBar_lineEdit.setPlaceholderText(_translate("Form", "Type Product ID or Product Name Here"))
        self.search_pushButton.setText(_translate("Form", "Search"))
        self.pushButton.setText(_translate("Form", "View Price History"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())