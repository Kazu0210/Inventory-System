# Form implementation generated from reading ui file 'monthly_backup_page.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(639, 429)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.calendarWidget = QtWidgets.QCalendarWidget(parent=Form)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 30, 312, 221))
        self.calendarWidget.setObjectName("calendarWidget")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(330, 30, 91, 16))
        self.label_2.setObjectName("label_2")
        self.selectedDate_label = QtWidgets.QLabel(parent=Form)
        self.selectedDate_label.setGeometry(QtCore.QRect(420, 30, 151, 16))
        self.selectedDate_label.setText("")
        self.selectedDate_label.setObjectName("selectedDate_label")
        self.timeEdit = QtWidgets.QTimeEdit(parent=Form)
        self.timeEdit.setGeometry(QtCore.QRect(10, 260, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.enable_checkBox = QtWidgets.QCheckBox(parent=Form)
        self.enable_checkBox.setGeometry(QtCore.QRect(10, 290, 151, 17))
        self.enable_checkBox.setObjectName("enable_checkBox")
        self.enableNotif_checkBox = QtWidgets.QCheckBox(parent=Form)
        self.enableNotif_checkBox.setGeometry(QtCore.QRect(10, 310, 291, 17))
        self.enableNotif_checkBox.setObjectName("enableNotif_checkBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Monthly Backup"))
        self.label_2.setText(_translate("Form", "Selected Date:"))
        self.enable_checkBox.setText(_translate("Form", "Enable Daily Backup"))
        self.enableNotif_checkBox.setText(_translate("Form", "Send Notification on Backup Completion"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())