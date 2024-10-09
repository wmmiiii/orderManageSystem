# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'previewOrder.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class ShopifyPreviewOrderUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(790, 767)
        self.shopify_table_widget = QtWidgets.QTableWidget(Form)
        self.shopify_table_widget.setGeometry(QtCore.QRect(0, 180, 791, 591))
        self.shopify_table_widget.setAlternatingRowColors(True)
        self.shopify_table_widget.setRowCount(20)
        self.shopify_table_widget.setObjectName("shopify_table_widget")
        self.shopify_table_widget.setColumnCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.shopify_table_widget.setHorizontalHeaderItem(5, item)
        self.order_directory_lineedit = QtWidgets.QLineEdit(Form)
        self.order_directory_lineedit.setGeometry(QtCore.QRect(40, 40, 301, 31))
        self.order_directory_lineedit.setObjectName("order_directory_lineedit")
        self.change_order_directory_btton = QtWidgets.QPushButton(Form)
        self.change_order_directory_btton.setGeometry(QtCore.QRect(360, 40, 93, 28))
        self.change_order_directory_btton.setObjectName("change_order_directory_btton")
        self.save_order_button = QtWidgets.QPushButton(Form)
        self.save_order_button.setGeometry(QtCore.QRect(360, 90, 93, 28))
        self.save_order_button.setObjectName("save_order_button")
        self.order_excel_lineeidt = QtWidgets.QLineEdit(Form)
        self.order_excel_lineeidt.setGeometry(QtCore.QRect(40, 90, 301, 31))
        self.order_excel_lineeidt.setObjectName("order_excel_lineeidt")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "订单预览"))
        item = self.shopify_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Order"))
        item = self.shopify_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Title"))
        item = self.shopify_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Variant title"))
        item = self.shopify_table_widget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "quantity"))
        item = self.shopify_table_widget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Carga to imagen"))
        item = self.shopify_table_widget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Thumbnail"))
        self.change_order_directory_btton.setText(_translate("Form", "更改"))
        self.save_order_button.setText(_translate("Form", "保存"))
