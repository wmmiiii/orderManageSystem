from PyQt5.QtWidgets import QWidget, QLabel, QColorDialog, QStyledItemDelegate, QCheckBox
from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QPixmap, QMouseEvent


class LoadImagesWidget(QWidget):
    enter = pyqtSignal(bool, str)
    leave = pyqtSignal(bool, str)
    clicked = pyqtSignal(bool, str)

    def __init__(self, object_name, parent):
        super(LoadImagesWidget, self).__init__(parent)
        self.setObjectName(object_name)
        self.object_name = object_name

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self.clicked.emit(True, self.object_name)

    def enterEvent(self, a0: QEvent) -> None:
        self.enter.emit(True, self.object_name)

    def leaveEvent(self, a0: QEvent) -> None:
        self.leave.emit(False, self.object_name)


class DealImagesLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, image, object_name, parent):
        super(DealImagesLabel, self).__init__(parent)
        self.setObjectName(object_name)
        pm = QPixmap(image)
        self.setPixmap(pm)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(self.objectName())


class PreDealAddImageLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent):
        super(PreDealAddImageLabel, self).__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(self.objectName())


class PreDealToolLabel(QLabel):
    clicked = pyqtSignal(bool)

    def __init__(self, parent):
        super(PreDealToolLabel, self).__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(True)

    def enterEvent(self, a0: QEvent) -> None:
        self.findChild(QLabel, 'gray_cover_label')


class QString:
    pass


class SelectColorLabel(QLabel):
    select_signal = pyqtSignal(bool, str)

    def __init__(self, qstyle, selected=False, object_name='', color='white', parent=None):
        super(SelectColorLabel, self).__init__(parent)
        self.qstyle = qstyle
        self.selected = selected
        self.object_name = object_name
        self.color_name = color

    def enterEvent(self, a0: QEvent) -> None:
        self.qstyle = self.styleSheet() + self.qstyle
        self.setStyleSheet(self.qstyle)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setStyleSheet(self.styleSheet().strip(self.qstyle))

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.selected = True
        if self.selected:
            self.select_signal.emit(self.selected, self.object_name)
            pixmap = QPixmap(':/pic/images/right-tick.png')
            self.setPixmap(pixmap)
            self.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        if 'define' in self.object_name:
            color = QColorDialog.getColor()
            if color.isValid():
                self.color_name = color.name()
        self.parent().selected_color = self.color_name


class TargetWidget(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TargetWidget, self).__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(self.objectName())

    def enterEvent(self, a0: QEvent) -> None:
        self.findChild(QLabel, self.objectName() + '_cancel_label').show()

    def leaveEvent(self, a0: QEvent) -> None:
        self.findChild(QLabel, self.objectName() + '_cancel_label').hide()


class PreWidget(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PreWidget, self).__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(self.objectName())

    def enterEvent(self, a0: QEvent) -> None:
        self.findChild(QLabel, self.objectName() + '_left_label').show()
        self.findChild(QLabel, self.objectName() + '_right_label').show()
        self.findChild(QLabel, self.objectName() + '_cancel_label').show()
        if self.findChild(QLabel,
                          self.objectName() + '_label').styleSheet() != 'border: 5px solid gray; border-style: solid;':
            self.findChild(QLabel, self.objectName() + '_label').setStyleSheet(
                'border: 2px solid gray; border-style: solid;')

    def leaveEvent(self, a0: QEvent) -> None:
        self.findChild(QLabel, self.objectName() + '_right_label').hide()
        self.findChild(QLabel, self.objectName() + '_left_label').hide()
        self.findChild(QLabel, self.objectName() + '_cancel_label').hide()
        if self.findChild(QLabel,
                          self.objectName() + '_label').styleSheet() == 'border: 2px solid gray; border-style: solid;':
            self.findChild(QLabel, self.objectName() + '_label').setStyleSheet('border: none;')


class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, text, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)
        self.text = text

    def createEditor(self, parent, option, index):
        editor = QCheckBox(parent)
        # editor.show()
        editor.setText(self.text)
        return editor
