import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMenuBar, QMenu, QAction, QLabel, QVBoxLayout
import SysmacStudioEnhancedToolFunction
from os import startfile


class SysmacStudioToolMainWindow(QMainWindow):
    def __init__(self):
        super(SysmacStudioToolMainWindow, self).__init__()
        self.setWindowIcon(QIcon(r'./images/main_window_icon.svg'))
        sst_widget = SysmacStudioEnhancedToolFunction.SysmacStudioEnhancedToolUi()

        self.menu_bar = QMenuBar()

        self.help_menu = QMenu()
        self.help_menu.setTitle('帮助')

        self.tool_use_action = QAction()
        self.tool_use_action.setText('工具使用')
        self.tool_use_action.triggered.connect(self.open_PDF)


        self.about_action = QAction()
        self.about_action.setText('关于')
        self.about_action.triggered.connect(self.about_widget)

        self.menu_bar.addMenu(self.help_menu)
        self.help_menu.addAction(self.tool_use_action)
        self.help_menu.addAction(self.about_action)
        self.setMenuBar(self.menu_bar)

        self.setCentralWidget(sst_widget)

    def about_widget(self):
        self.aboutWidget = QWidget()
        self.aboutWidget.setWindowTitle('关于')
        self.aboutEdt = QLabel(self.aboutWidget)
        self.aboutEdt.setText('SysmacStudio增强工具，用于轴设置参数的复制。\n作者：MQSQ\n注意：本工具非官方，仅用于学习交流。\n如果对SysmacStudio原工程造成影响概不负责！')
        self.v_layout = QVBoxLayout(self.aboutWidget)
        self.v_layout.addWidget(self.aboutEdt)

        self.aboutWidget.show()

    def open_PDF(self):
        startfile('.\\data\\SysmacStudio增强工具使用说明.pdf')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SysmacStudioToolMainWindow()
    win.show()
    sys.exit(app.exec_())