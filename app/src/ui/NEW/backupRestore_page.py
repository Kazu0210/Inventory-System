# Form implementation generated from reading ui file 'backupRestore_page.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(839, 637)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 16))
        self.label.setObjectName("label")
        self.backupNow_pushButton = QtWidgets.QPushButton(parent=Form)
        self.backupNow_pushButton.setGeometry(QtCore.QRect(10, 30, 91, 23))
        self.backupNow_pushButton.setObjectName("backupNow_pushButton")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 111, 16))
        self.label_2.setObjectName("label_2")
        self.backupStat_label = QtWidgets.QLabel(parent=Form)
        self.backupStat_label.setGeometry(QtCore.QRect(60, 10, 91, 16))
        self.backupStat_label.setObjectName("backupStat_label")
        self.setSched_pushButton = QtWidgets.QPushButton(parent=Form)
        self.setSched_pushButton.setGeometry(QtCore.QRect(10, 90, 91, 23))
        self.setSched_pushButton.setObjectName("setSched_pushButton")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(10, 350, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(10, 370, 141, 16))
        self.label_4.setObjectName("label_4")
        self.fileFormat_comboBox = QtWidgets.QComboBox(parent=Form)
        self.fileFormat_comboBox.setGeometry(QtCore.QRect(160, 370, 141, 22))
        self.fileFormat_comboBox.setObjectName("fileFormat_comboBox")
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(10, 400, 171, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=Form)
        self.label_6.setGeometry(QtCore.QRect(10, 440, 91, 16))
        self.label_6.setObjectName("label_6")
        self.backup_file_name_label = QtWidgets.QLabel(parent=Form)
        self.backup_file_name_label.setGeometry(QtCore.QRect(10, 460, 91, 16))
        self.backup_file_name_label.setObjectName("backup_file_name_label")
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 120, 721, 221))
        self.listWidget.setMinimumSize(QtCore.QSize(721, 192))
        self.listWidget.setObjectName("listWidget")
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setGeometry(QtCore.QRect(10, 480, 261, 111))
        self.frame.setStyleSheet("#dragDrop_frame{\n"
"border: 1px solid #000;\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.restore_pushButton = QtWidgets.QPushButton(parent=Form)
        self.restore_pushButton.setGeometry(QtCore.QRect(280, 480, 91, 23))
        self.restore_pushButton.setObjectName("restore_pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Backup"))
        self.backupNow_pushButton.setText(_translate("Form", "Backup Now"))
        self.label_2.setText(_translate("Form", "Schedule Backup"))
        self.backupStat_label.setText(_translate("Form", "Backup Status"))
        self.setSched_pushButton.setText(_translate("Form", "Set Schedule"))
        self.label_3.setText(_translate("Form", "Backup Format"))
        self.label_4.setText(_translate("Form", "Select backup file format:"))
        self.label_5.setText(_translate("Form", "backup_YYYY-MM-DD_HH-MM.sql"))
        self.label_6.setText(_translate("Form", "Upload Backup"))
        self.backup_file_name_label.setText(_translate("Form", "File name"))
        self.restore_pushButton.setText(_translate("Form", "Restore Now"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
