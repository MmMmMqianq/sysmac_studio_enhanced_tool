# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tool_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(383, 471)
        Form.setMinimumSize(QtCore.QSize(383, 471))
        Form.setMaximumSize(QtCore.QSize(383, 471))
        Form.setToolTip("")
        Form.setWhatsThis("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.searchLab = QtWidgets.QLabel(self.frame)
        self.searchLab.setGeometry(QtCore.QRect(20, 10, 24, 16))
        self.searchLab.setObjectName("searchLab")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 321, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchMethodCB = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchMethodCB.sizePolicy().hasHeightForWidth())
        self.searchMethodCB.setSizePolicy(sizePolicy)
        self.searchMethodCB.setObjectName("searchMethodCB")
        self.searchMethodCB.addItem("")
        self.searchMethodCB.addItem("")
        self.horizontalLayout.addWidget(self.searchMethodCB)
        self.creatDataTimeDT = QtWidgets.QDateTimeEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creatDataTimeDT.sizePolicy().hasHeightForWidth())
        self.creatDataTimeDT.setSizePolicy(sizePolicy)
        self.creatDataTimeDT.setObjectName("creatDataTimeDT")
        self.horizontalLayout.addWidget(self.creatDataTimeDT)
        self.startSearchBtn = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startSearchBtn.sizePolicy().hasHeightForWidth())
        self.startSearchBtn.setSizePolicy(sizePolicy)
        self.startSearchBtn.setObjectName("startSearchBtn")
        self.horizontalLayout.addWidget(self.startSearchBtn)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.resultLab = QtWidgets.QLabel(self.frame_2)
        self.resultLab.setGeometry(QtCore.QRect(20, 10, 31, 16))
        self.resultLab.setObjectName("resultLab")
        self.layoutWidget1 = QtWidgets.QWidget(self.frame_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 32, 321, 92))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.controllerNameCB = QtWidgets.QComboBox(self.layoutWidget1)
        self.controllerNameCB.setObjectName("controllerNameCB")
        self.gridLayout.addWidget(self.controllerNameCB, 2, 1, 1, 1)
        self.controllerNameLab = QtWidgets.QLabel(self.layoutWidget1)
        self.controllerNameLab.setObjectName("controllerNameLab")
        self.gridLayout.addWidget(self.controllerNameLab, 2, 0, 1, 1)
        self.projectDirectoryEdt = QtWidgets.QLineEdit(self.layoutWidget1)
        self.projectDirectoryEdt.setText("")
        self.projectDirectoryEdt.setObjectName("projectDirectoryEdt")
        self.gridLayout.addWidget(self.projectDirectoryEdt, 1, 1, 1, 1)
        self.projectNameLab = QtWidgets.QLabel(self.layoutWidget1)
        self.projectNameLab.setObjectName("projectNameLab")
        self.gridLayout.addWidget(self.projectNameLab, 0, 0, 1, 1)
        self.projectDirectoryLab = QtWidgets.QLabel(self.layoutWidget1)
        self.projectDirectoryLab.setObjectName("projectDirectoryLab")
        self.gridLayout.addWidget(self.projectDirectoryLab, 1, 0, 1, 1)
        self.projectNameEdt = QtWidgets.QLineEdit(self.layoutWidget1)
        self.projectNameEdt.setText("")
        self.projectNameEdt.setObjectName("projectNameEdt")
        self.gridLayout.addWidget(self.projectNameEdt, 0, 1, 1, 1)
        self.controllerNameLab_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.controllerNameLab_2.setObjectName("controllerNameLab_2")
        self.gridLayout.addWidget(self.controllerNameLab_2, 3, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setToolTip("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.frame_3.setMidLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.copyPasteAxisParameterLab = QtWidgets.QLabel(self.frame_3)
        self.copyPasteAxisParameterLab.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.copyPasteAxisParameterLab.setObjectName("copyPasteAxisParameterLab")
        self.informationTW = QtWidgets.QTreeWidget(self.frame_3)
        self.informationTW.setGeometry(QtCore.QRect(20, 40, 321, 131))
        self.informationTW.setObjectName("informationTW")
        self.layoutWidget2 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 180, 61, 25))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addBtn = QtWidgets.QPushButton(self.layoutWidget2)
        self.addBtn.setEnabled(False)
        self.addBtn.setObjectName("addBtn")
        self.horizontalLayout_3.addWidget(self.addBtn)
        self.deleteBtn = QtWidgets.QPushButton(self.layoutWidget2)
        self.deleteBtn.setEnabled(False)
        self.deleteBtn.setObjectName("deleteBtn")
        self.horizontalLayout_3.addWidget(self.deleteBtn)
        self.widget = QtWidgets.QWidget(self.frame_3)
        self.widget.setGeometry(QtCore.QRect(160, 180, 178, 25))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.isBackupcheckBox = QtWidgets.QCheckBox(self.widget)
        self.isBackupcheckBox.setObjectName("isBackupcheckBox")
        self.horizontalLayout_2.addWidget(self.isBackupcheckBox)
        self.startBtn = QtWidgets.QPushButton(self.widget)
        self.startBtn.setEnabled(False)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_2.addWidget(self.startBtn)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sysmac Studio 增强工具"))
        self.searchLab.setText(_translate("Form", "检索"))
        self.searchMethodCB.setItemText(0, _translate("Form", "项目创建时间："))
        self.searchMethodCB.setItemText(1, _translate("Form", "项目修改时间："))
        self.creatDataTimeDT.setDisplayFormat(_translate("Form", "yyyy/M/d HH:mm:ss"))
        self.startSearchBtn.setText(_translate("Form", "检索轴"))
        self.resultLab.setText(_translate("Form", "结果"))
        self.controllerNameLab.setText(_translate("Form", "控制器名："))
        self.projectNameLab.setText(_translate("Form", "项目名称："))
        self.projectDirectoryLab.setText(_translate("Form", "项目目录："))
        self.controllerNameLab_2.setText(_translate("Form", "复制项目："))
        self.copyPasteAxisParameterLab.setText(_translate("Form", "复制/粘贴轴参数"))
        self.informationTW.headerItem().setText(0, _translate("Form", "复制轴"))
        self.informationTW.headerItem().setText(1, _translate("Form", "粘贴轴"))
        self.addBtn.setText(_translate("Form", "+"))
        self.deleteBtn.setText(_translate("Form", "-"))
        self.isBackupcheckBox.setToolTip(_translate("Form", "项目将被备份至C:\\OMRON\\Data\\Solution_backup目录下，\n"
"如果需要恢复可将备份文件复制到C:\\OMRON\\Data\\Solution目录下"))
        self.isBackupcheckBox.setText(_translate("Form", "是否备份项目"))
        self.startBtn.setText(_translate("Form", "开始"))
