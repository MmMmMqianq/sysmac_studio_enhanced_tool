from PyQt5.QtCore import QDateTime, Qt, QObject, pyqtBoundSignal, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTreeWidgetItem, QComboBox, QHeaderView
import sys
from re import findall
import tool_ui
import xml_handler
import CheckableComboBox
from shutil import make_archive, unpack_archive
from os import listdir, remove


class SysmacStudioEnhancedToolUi(QWidget):
    def __init__(self):
        super(SysmacStudioEnhancedToolUi, self).__init__()
        self.tool_ui = tool_ui.Ui_Form()
        self.tool_ui.setupUi(self)

        self.init_variables()
        self.init_widget()
        self.bind_signals()

    def init_variables(self):
        self.defSignals = Signals()
        self.xml_handler = xml_handler.XMLHandler()
        # self.top_item_df = DataFrame(columns=['top_item', 'cb', 'cb_item_text', 'ccb', 'ccb_item_text'])
        # self.tool_ui.creatDataTimeDT.setDateTime(QDateTime.currentDateTime())
        self.tool_ui.creatDataTimeDT.setDateTime(QDateTime.fromString('2023-04-27 15:18:53', 'yyyy-MM-dd hh:mm:ss'))

        self.item_list = []
        self.cb_list = []
        self.ccb_list = []

    def init_widget(self):
        self.copyItemsCCB = CheckableComboBox.CheckableComboBox()
        self.copyItemsCCB.addItems(['PDO', '单位换算设置', '操作设置', '其他操作设置', '限位设置', '原点返回设置', '位置计数设置', '伺服驱动设置'])
        self.tool_ui.gridLayout.addWidget(self.copyItemsCCB, 3, 1)

    def bind_signals(self):
        self.tool_ui.startSearchBtn.clicked.connect(self.search_project_directory)
        self.tool_ui.addBtn.clicked.connect(self.add_tree_item)
        self.tool_ui.deleteBtn.clicked.connect(self.delete_tree_item)
        self.tool_ui.deleteBtn.clicked.connect(self.set_start_button)
        self.tool_ui.startBtn.clicked.connect(self.start_paste)
        self.tool_ui.controllerNameCB.currentTextChanged.connect(self.init_tree_item)
        self.copyItemsCCB.currentTextChanged.connect(self.set_copyItemsCCB)

        self.defSignals.copy_ok.connect(self.copy_ok_message)

    def search_project_directory(self):
        # creat_time = self.tool_ui.creatDataTimeDT.date().toString('yyyy-MM-dd') + 'T' \
        #              + self.tool_ui.creatDataTimeDT.time().toString('hh:mm:ss')
        # print(creat_time)
        # project_directory = self.xml_handler.get_project_directory(path='C:\OMRON\Data\Solution', dateCreated=creat_time)

        current_time = self.tool_ui.creatDataTimeDT.dateTime().toString('MM/dd/yyyy hh:mm:ss')
        print(current_time)

        is_dc = False
        if self.tool_ui.searchMethodCB.currentText() == '项目创建时间：':
            is_dc = True
        elif self.tool_ui.searchMethodCB.currentText() == '项目修改时间：':
            is_dc = False

        project_directory, self.oem_file_path = self.xml_handler.get_project_directory1(path='C:\OMRON\Data\Solution',
                                                                                        project_time=current_time, is_dateCreated=is_dc)
        if project_directory != '' and self.oem_file_path != '':
            self.tool_ui.projectDirectoryEdt.setText(project_directory)
            project_name, controller_names = self.xml_handler.get_controller_name(self.oem_file_path)

            self.tool_ui.controllerNameCB.clear()
            self.tool_ui.controllerNameCB.addItems(controller_names)
            self.tool_ui.projectNameEdt.setText(project_name)
        else:
            self.tool_ui.projectNameEdt.setText('未找到匹配的项目')
            self.tool_ui.projectDirectoryEdt.setText('')
            self.tool_ui.controllerNameCB.clear()

    def init_tree_item(self):

        # self.axis_file_path = self.xml_handler.get_axis_parameter_file_path(project_directory)
        self.tool_ui.informationTW.clear()

        self.axis_file_path, self.axis_file_path1, self.axis_name_list = self.xml_handler. \
            get_axis_parameter_file_path1(self.oem_file_path,
                                          controller_name=self.tool_ui.controllerNameCB.currentText())
        if self.axis_file_path != {}:
            self.tool_ui.informationTW.clear()
            self.ccb_list.clear()
            self.add_tree_item()

        self.tool_ui.addBtn.setEnabled(True)
        self.tool_ui.deleteBtn.setEnabled(True)

    def add_tree_item(self):
        item = QTreeWidgetItem()
        self.tool_ui.informationTW.insertTopLevelItem(self.tool_ui.informationTW.topLevelItemCount(), item)

        cb = QComboBox()
        cb.addItems(self.axis_name_list)
        self.tool_ui.informationTW.setItemWidget(item, 0, cb)

        ccb = CheckableComboBox.CheckableComboBox()
        self.ccb_list.append(ccb)
        ccb.addItems(self.axis_name_list)
        self.tool_ui.informationTW.setItemWidget(item, 1, ccb)

        self.tool_ui.informationTW.header().setSectionResizeMode(QHeaderView.ResizeToContents)  # 将列设置为合适的宽度

        ccb.currentTextChanged.connect(self.set_start_button)
        self.tool_ui.startBtn.setEnabled(False)

    def delete_tree_item(self):
        """点击删除按钮时删除tree widget中末尾的item"""
        self.tool_ui.informationTW.takeTopLevelItem(self.tool_ui.informationTW.topLevelItemCount()-1)
        if self.ccb_list != []:
            self.ccb_list.pop()

    def start_paste(self):
        if self.copyItemsCCB.texts_list == []:
            message_box = QMessageBox()
            message_box.setText('复制项目不能为空！')
            message_box.exec_()
        else:
            # 将项目备份到r'C:\\OMRON\\Data\\Solution_backup目录下
            if self.tool_ui.isBackupcheckBox.isChecked():
                def backup_project_directory():
                    target_file_name = self.tool_ui.projectDirectoryEdt.text().split('\\')[-1]
                    make_archive(r'C:\\OMRON\\Data\\Solution_backup\\{0:s}'.format(target_file_name),
                                 'zip',
                                 self.tool_ui.projectDirectoryEdt.text())
                    unpack_archive(r'C:\\OMRON\\Data\\Solution_backup\\{0:s}.zip'.format(target_file_name),
                                   r'C:\\OMRON\\Data\\Solution_backup\\{0:s}'.format(target_file_name))
                    remove(r'C:\\OMRON\\Data\\Solution_backup\\{0:s}.zip'.format(target_file_name))
                    self.tool_ui.isBackupcheckBox.setCheckState(False)

                if self.tool_ui.projectDirectoryEdt.text().split('\\')[-1] in listdir(r'C:\\OMRON\\Data\\Solution_backup'):
                    message_box1 = QMessageBox()
                    message_box1.setModal(True)
                    message_box1.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                    message_box1.setText('项目已备份，是否重新备份？')
                    res = message_box1.exec_()
                    if res == 16384:
                        backup_project_directory()
                else:
                    backup_project_directory()

            # 开始粘贴
            for i in range(0, self.tool_ui.informationTW.topLevelItemCount()):
                source_axis = int(findall(r'(?<=\()\d{1,3}(?=,|\))',
                                          self.tool_ui.informationTW.itemWidget(self.tool_ui.informationTW.topLevelItem(i),
                                                                                0).currentText())[0])
                print(source_axis)
                target_axis = []
                for name in self.tool_ui.informationTW.itemWidget(self.tool_ui.informationTW.topLevelItem(i), 1).texts_list:
                    target_axis.append(int(findall(r'(?<=\()\d{1,3}(?=,|\))', name)[0]))
                print(source_axis, target_axis)
                print(self.axis_file_path1)

                for operation in self.copyItemsCCB.texts_list:
                    if operation == 'PDO':
                        self.xml_handler.paste_pdo_parameter(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '单位换算设置':
                        self.xml_handler.paste_unit_conversion_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '操作设置':
                        self.xml_handler.paste_operation_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '其他操作设置':
                        self.xml_handler.paste_other_operation_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '限位设置':
                        self.xml_handler.paste_limits_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '原点返回设置':
                        self.xml_handler.paste_homing_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '位置计数设置':
                        self.xml_handler.paste_position_count_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
                    elif operation == '伺服驱动设置':
                        self.xml_handler.paste_servo_driver_settings(axis_path=self.axis_file_path1, source=source_axis, target=target_axis)
            self.defSignals.copy_ok.emit('copy_ok')

    def set_start_button(self):
        """ 当CheckComboBox中一个轴都未选中时将开始按钮设置为disable，否则设置为enable """
        for i in self.ccb_list:
            if i.currentText() == '':
                self.tool_ui.startBtn.setEnabled(False)
                break
            else:
                self.tool_ui.startBtn.setEnabled(True)

    def set_copyItemsCCB(self):
        """
        判断 copyItemsCCB 中的 单位换算item是否要设置为选中状态
        """
        for k in self.copyItemsCCB.item_dict:
            if k in [2, 4, 5, 6]:
                self.copyItemsCCB.model().item(1).setCheckState(Qt.Checked)
                break

    def copy_ok_message(self):
        message_box = QMessageBox()
        message_box.setText('粘贴完成！')
        message_box.exec_()


class Signals(QObject):
    copy_ok: pyqtBoundSignal

    copy_ok = pyqtSignal(str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SysmacStudioEnhancedToolUi()
    win.show()
    sys.exit(app.exec_())
