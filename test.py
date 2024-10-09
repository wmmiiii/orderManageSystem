# from PyQt5.QtCore import Qt, QStringListModel
# from PyQt5.QtGui import QStandardItem, QStandardItemModel
# from PyQt5.QtWidgets import QApplication, QListView, QVBoxLayout, QWidget
#
# app = QApplication([])
# widget = QWidget()
# layout = QVBoxLayout(widget)
#
# # 创建一个字符串列表
# strings = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
#
# # 创建一个字符串列表模型
# model = QStringListModel(strings)
#
# # 创建一个Item Model
# item_model = QStandardItemModel()
# for s in strings:
#     item = QStandardItem(s)
#     item_model.appendRow(item)
#
# # 创建一个QListView，并设置模型
# list_view1 = QListView()
# list_view1.setModel(model)
#
# list_view2 = QListView()
# list_view2.setModel(item_model)
#
# layout.addWidget(list_view1)
# layout.addWidget(list_view2)
#
# widget.show()
# app.exec_()
from PyQt5.QtGui import QStandardItemModel, QStandardItem
# from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QWidget, QVBoxLayout
# from PyQt5.QtCore import Qt, QAbstractTableModel
#
#
# class MyTableModel(QAbstractTableModel):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data
#
#     def rowCount(self, parent):
#         return len(self.data)
#
#     def columnCount(self, parent):
#         return len(self.data[0])
#
#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             return str(self.data[index.row()][index.column()])
#         return None
#
#
# class MainWindow(QMainWindow):
#     def __init__(self, data):
#         super().__init__()
#         self.table_view = QTableView(self)
#         self.setCentralWidget(self.table_view)
#         self.model = MyTableModel(data)
#         self.table_view.setModel(self.model)
#
#
# if __name__ == "__main__":
#     app = QApplication([])
#     data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#     window = MainWindow(data)
#     window.show()
#     app.exec_()


# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
# from PyQt5.QtGui import QColor
#
# class ColorDialog(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.button = QPushButton('选择颜色', self)
#         self.button.move(20, 20)
#         self.button.clicked.connect(self.showDialog)
#
#         self.setGeometry(300, 300, 250, 180)
#         self.setWindowTitle('颜色选择对话框')
#         self.show()
#
#     def showDialog(self):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             self.button.setStyleSheet(f'background-color: {color.name()}')
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = ColorDialog()
#     sys.exit(app.exec_())


# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
# from PyQt5.QtWidgets import QApplication, QTableView, QSpinBox, QStyledItemDelegate
#
# class SpinBoxDelegate(QStyledItemDelegate):
#     def createEditor(self, parent, option, index):
#         editor = QSpinBox(parent)
#         editor.setFrame(False)
#         editor.setMinimum(0)
#         editor.setMaximum(100)
#         return editor
#
# if __name__ == '__main__':
#     app = QApplication([])
#     model = QStandardItemModel(4, 4)
#     for row in range(model.rowCount()):
#         for column in range(model.columnCount()):
#             item = QStandardItem("Item %s-%s" % (row, column))
#             model.setItem(row, column, item)
#
#     tableView = QTableView()
#     tableView.setModel(model)
#     delegate = SpinBoxDelegate()
#     tableView.setItemDelegate(delegate)
#     tableView.show()
#     app.exec_()


import datetime
from dateutil.parser import parse
#
# # 输入日期字符串
# input_date_str = '2023-03-27T03:35:53-05:00'.split('T')[0]
#
# # 将输入日期字符串转换为datetime对象
# input_date = parse(input_date_str)
#
# # 计算输入日期的星期几
# weekday = input_date.strftime('%A')
#
# # 计算输入日期与当前日期的差距
# delta = datetime.date.today() - input_date.date()
#
# # 判断输入日期是否是yesterday、today或星期几，并打印输出
# if delta == datetime.timedelta(days=0):
#     print('today')
# elif delta == datetime.timedelta(days=1):
#     print('yesterday')
# else:
#     print(weekday)

input_time_str = '14:17:42'#'2023-03-27T03:35:53-05:00'.split('T')[1].split('-')[0]

# 将输入时间字符串转换为datetime对象
input_time = datetime.datetime.strptime(input_time_str, '%H:%M:%S')
print(input_time)

# 将datetime对象格式化为输出格式
output_time_str = input_time.strftime('%I:%M %p').lower()
print(output_time_str)


# from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QApplication, QMainWindow, QTableView
# from PyQt5.QtCore import Qt, QModelIndex
#
# class ComboBoxDelegate(QStyledItemDelegate):
#     def __init__(self, parent=None):
#         super(ComboBoxDelegate, self).__init__(parent)
#
#     def createEditor(self, parent, option, index):
#         editor = QComboBox(parent)
#         editor.addItems(['Option 1', 'Option 2', 'Option 3'])
#         return editor
#
#     def setEditorData(self, editor, index):
#         value = index.model().data(index, Qt.EditRole)
#         editor.setCurrentIndex(editor.findText(str(value)))
#
#     def setModelData(self, editor, model, index):
#         value = editor.currentText()
#         model.setData(index, value, Qt.EditRole)
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setGeometry(100, 100, 400, 300)
#         self.setWindowTitle("TableView Example")
#
#         self.table = QTableView()
#         self.setCentralWidget(self.table)
#
#         self.model = QStandardItemModel()
#         self.model.setItem(0, 0, QStandardItem("Cell 1"))
#         self.model.setItem(0, 1, QStandardItem("Cell 2"))
#         self.table.setModel(self.model)
#
#         delegate = ComboBoxDelegate(self)
#         self.table.setItemDelegateForColumn(1, delegate)
#
#         self.show()
#
# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     app.exec_()


# coding=utf-8
# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
#
# class Table(QWidget):
#     def __init__(self,parent=None):
#         super(Table, self).__init__(parent)
#         #设置标题与初始大小
#         self.setWindowTitle('QTableView表格复选框案例')
#         self.resize(500,300)
#         self.tableView=QTableView(parent)
#         self.model = QStandardItemModel(self.tableView)
#
#         #设置数据层次结构，4行4列
#         self.model=QStandardItemModel(4,4)
#         t = QCheckBox(self)
#         #设置水平方向四个头标签文本内容
#         self.model.setHorizontalHeaderLabels(['状态','姓名','身份证','地址'])
#
#         for row in range(4):
#             for column in range(4):
#                 item_checked = QStandardItem()
#                 item_checked.setCheckState(Qt.CheckState.Checked)
#                 item_checked.setCheckable(True)
#                 self.model.setItem(column,0, item_checked)
#                 item=QStandardItem('row %s,column %s'%(row,column))
#                 #设置每个位置的文本值
#                 self.model.setItem(row,column,item)
#
#         self.tableView.setModel(self.model)
#         #设置布局
#         layout=QVBoxLayout()
#         layout.addWidget(self.tableView)
#         self.setLayout(layout)
#
# if __name__ == '__main__':
#     app=QApplication(sys.argv)
#     table=Table()
#     table.show()
#     sys.exit(app.exec_())


# -*- encoding: utf-8 -*-
'''
@Contact :   obj2008@foxmail.com
2020/5/13 12:48 PM   obj2008      1.0         None
--------------------------------------------------------
'''
import sys

from PyQt5.QtWidgets import QApplication, QWidget,  QVBoxLayout,  QTableWidget, QCheckBox, QHeaderView, QStyle, QStyleOptionButton, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, QRect

# 表头字段，全局变量
header_field = ['全选', '姓名', '年龄', '籍贯']
# 用来装行表头所有复选框 全局变量
all_header_combobox = []


class CheckBoxHeader(QHeaderView):
    """自定义表头类"""

    # 自定义 复选框全选信号
    select_all_clicked = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 0
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2.)

        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 自定义信号 select_all_clicked 的槽方法
    def change_state(self, isOn):
        # 如果行表头复选框为勾选状态
        if isOn:
            # 将所有的复选框都设为勾选状态
            for i in all_header_combobox:
                i.setCheckState(Qt.Checked)
        else:
            for i in all_header_combobox:
                i.setCheckState(Qt.Unchecked)


class TableDemo(QWidget):
    """窗口类"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('这是QTableWidget类行表头添加复选框全选功能')
        self.resize(400, 300)

        # 垂直布局
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignTop)  # 设置 垂直布局 的对齐方式
        self.setTableWidget()  # 设置表格

        self.show()

    # 设置表格
    def setTableWidget(self):
        # 表格控件
        self.tablewidget = QTableWidget(3,4)        # 3行4列
        self.tablewidget.setFixedWidth(300)         # 表格宽度
        self.setTableHeaderField()               # 设置表格行表头字段
        self.tablewidget.setAlternatingRowColors(True)      # 交替行颜色
        self.vlayout.addWidget(self.tablewidget)

    # 设置行表头字段
    def setTableHeaderField(self):

        self.tablewidget.setColumnCount(len(header_field))   # 设置列数
        for i in range(len(header_field)-1):
            header_item = QTableWidgetItem(header_field[i])

            checkbox = QCheckBox()
            # 将所有的复选框都添加到 全局变量 all_header_combobox 中
            all_header_combobox.append(checkbox)
            # 为每一行添加复选框
            self.tablewidget.setCellWidget(i,0,checkbox)

        header = CheckBoxHeader()               # 实例化自定义表头
        self.tablewidget.setHorizontalHeader(header)            # 设置表头
        self.tablewidget.setHorizontalHeaderLabels(header_field)        # 设置行表头字段
        self.tablewidget.setColumnWidth(0,60)       # 设置第0列宽度
        header.select_all_clicked.connect(header.change_state)        # 行表头复选框单击信号与槽

    # 设置表格内容，根据实际情况设置即可
    def setTableContents(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ta = TableDemo()
    sys.exit(app.exec_())

