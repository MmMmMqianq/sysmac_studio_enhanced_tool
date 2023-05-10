"""
可多选的下拉框
通过CheckableComboBox.texts_list 可以获取选中的item值组成的列表；用CheckableComboBox.currentText没法显示全

texts_list = []  # 所有选中的item文本组成的列表
item_list = []  # 所有选中的item组成的列表
"""


from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QStandardItem, QFontMetrics, QPalette
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox, qApp

class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.texts_list = []  # 所有选中的item文本组成的列表
        self.item_list = []  # 所有选中的item组成的列表
        self.item_dict = {}

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        self.texts_list = []
        self.item_list = []
        self.item_dict = {}
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                self.texts_list.append(self.model().item(i).text())
                self.item_list.append(self.model().item(i))
                self.item_dict[i] = self.model().item(i)
        text = ", ".join(self.texts_list)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res

if __name__ == '__main__':
    from PyQt5 import QtWidgets,QtCore
    import sys

    comunes = ['Ameglia', 'Arcola', 'Bagnone', 'Bolano', 'Carrara', 'Casola', 'Castelnuovo Magra',
               'Comano, località Crespiano', 'Fivizzano', 'Fivizzano località Pieve S. Paolo',
               'Fivizzano località Pieve di Viano', 'Fivizzano località Soliera', 'Fosdinovo', 'Genova',
               'La Spezia', 'Levanto', 'Licciana Nardi', 'Lucca', 'Lusuolo', 'Massa', 'Minucciano',
               'Montignoso', 'Ortonovo', 'Piazza al sercho', 'Pietrasanta', 'Pignine', 'Pisa',
               'Podenzana', 'Pontremoli', 'Portovenere', 'Santo Stefano di Magra', 'Sarzana',
               'Serravezza', 'Sesta Godano', 'Varese Ligure', 'Vezzano Ligure', 'Zignago']

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    comboBox1 = CheckableComboBox(Form)
    comboBox1.addItems(comunes)

    Form.show()
    sys.exit(app.exec_())