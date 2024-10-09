import base64
import re
import time
from urllib.parse import urlparse, parse_qs

import pandas as pd
from PyQt5 import sip
from PyQt5.QtCore import QRegExp, QPoint, QPropertyAnimation, QParallelAnimationGroup, QSize
from PIL import ImageFile
from ui_repeat_form import *
from ui_main import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QGridLayout, QMessageBox, QHeaderView, \
    QTableWidgetItem
from PyQt5.QtGui import QFont, QTransform, QIcon, QStandardItemModel, QStandardItem, QMovie
from recevthread import *
from show_images_label import *
from dataDisplayViewModel import *
from ui_newBackground import *
import sys
from resources_rc import *
from ui_previewOrder import *


ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class Index(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Index, self).__init__(parent)
        self.page = 0
        self.last_id = {}
        self.shopify_model = None
        self.img_num = None
        self.img_nums = None
        self.find_similarity_threads = None
        self.n = None
        self.show_repeat_progress_widget = None
        self.add_target_progress_widget = None
        self.img_deal_threads = None
        self.target_grid = None
        self.selected_label = None
        self.setupUi(self)
        self.pre_deal_widget.enterEvent = self.enter_pre_deal_label
        self.pre_deal_widget.leaveEvent = self.leave_pre_deal_label
        self.pre_deal_widget.mouseReleaseEvent = self.click_pre_deal_label
        self.get_images_widget.enterEvent = self.enter_get_images_label
        self.get_images_widget.mouseReleaseEvent = self.click_get_images_label
        self.get_images_widget.leaveEvent = self.leave_get_images_label
        self.shopify_orders_widget.enterEvent = self.enter_shopify_label
        self.shopify_orders_widget.leaveEvent = self.leave_shopify_label
        self.shopify_orders_widget.mouseReleaseEvent = self.click_shopify_label
        self.setting_widget.enterEvent = self.enter_setting_label
        self.setting_widget.mouseReleaseEvent = self.click_setting_label
        self.setting_widget.leaveEvent = self.leave_setting_label
        self.help_widget.enterEvent = self.enter_help_label
        self.help_widget.leaveEvent = self.leave_help_label
        self.pre_deal_scroll_area.hide()
        self.add_images_label = PreDealAddImageLabel(self.add_images_frame)
        self.add_images_label.setGeometry(QtCore.QRect(170, 390, 241, 71))
        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.add_images_label.setFont(font)
        self.add_images_label.setStyleSheet("background-color: rgb(132, 198, 0);")
        self.add_images_label.setAlignment(QtCore.Qt.AlignCenter)
        self.add_images_label.setObjectName("add_images_label")
        self.add_image_dir_label = PreDealAddImageLabel(self.add_images_frame)
        self.add_image_dir_label.setGeometry(QtCore.QRect(240, 490, 111, 31))
        self.add_image_dir_label.setStyleSheet("color: rgb(226, 226, 226);")
        self.add_image_dir_label.setObjectName("add_image_dir_label")
        _translate = QtCore.QCoreApplication.translate
        self.add_images_label.setText(_translate("MainWindow", "+添加多张图片"))
        self.add_image_dir_label.setText(_translate("MainWindow", "添加整个文件夹"))
        self.add_images_label.clicked.connect(self.load_images)
        self.add_image_dir_label.clicked.connect(self.load_images)
        self.find_same_button.clicked.connect(self.slot_find_repeat_images)
        self.read_excel_pushButton.clicked.connect(self.slot_read_excel)
        self.get_images_add_col_button.clicked.connect(self.slot_add_col_name)
        self.save_excel_images_pushButton.clicked.connect(self.slot_save_images_directory)
        self.read_excel_pushButton.setStyleSheet('QPushButton {background-color: white; color: black;} '
                                                 'QPushButton:hover {background-color: argb(85, 170, 255, 150);}')
        self.get_images_add_col_button.setStyleSheet('QPushButton {background-color: white; color: black;} '
                                                     'QPushButton:hover {background-color: argb(85, 170, 255, 150);}')
        self.save_excel_images_pushButton.setStyleSheet('QPushButton {background-color: white; color: black;} '
                                                        'QPushButton:hover {background-color: argb(85, 170, 255, '
                                                        '150);}')
        self.start_download_button.setStyleSheet('QPushButton {border-radius: 15px;background-color: white; color: '
                                                 'black;} QPushButton:hover {background-color: argb(85, 170, 255, '
                                                 '150);}')
        self.start_download_button.setFixedSize(30, 30)
        self.start_download_button.setIcon(QIcon(':/pic/images/start.png'))
        self.start_download_button.clicked.connect(self.slot_start_download_images)
        self.pause_download_button.setFixedSize(30, 30)
        self.pause_download_button.setIcon(QIcon(':/pic/images/pause.png'))
        self.pause_download_button.setStyleSheet("QPushButton {border-radius: 15px; background-color: red; color: "
                                                 "white;} QPushButton:hover {background-color: white;}")
        self.stop_download_button.setFixedSize(30, 30)
        self.stop_download_button.setIcon(QIcon(':/pic/images/stop.png'))
        self.stop_download_button.setStyleSheet('QPushButton {border-radius: 15px;background-color: red; color: '
                                                'black;} QPushButton:hover {background-color: white;}')
        self.resume_download_button.setFixedSize(30, 30)
        self.resume_download_button.setIcon(QIcon(':/pic/images/resume.png'))
        self.resume_download_button.setStyleSheet('QPushButton {border-radius: 15px;background-color: red; color: '
                                                  'black;} QPushButton:hover {background-color: white;}')
        self.clear_all_settings_button.setFixedSize(30, 30)
        self.clear_all_settings_button.setIcon(QIcon(':/pic/images/clear_all_settings.png'))
        self.clear_all_settings_button.setStyleSheet('QPushButton {border-radius: 15px;background-color: blue; color: '
                                                     'black;} QPushButton:hover {background-color: white;}')
        self.clear_all_settings_button.clicked.connect(self.add_col_name_label.clear)
        self.clear_all_settings_button.clicked.connect(self.get_images_show_example_ledit.clear)
        self.add_target_selectcolor_button.clicked.connect(self.slot_new_color_bg)

        self.pre_after_add_images_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                                       '140);}QPushButton:hover {border: 2px solid black; '
                                                       'border-style: solid;}')
        self.pre_after_add_images_button.clicked.connect(lambda x=self.pre_after_add_images_button.objectName():
                                                         self.load_images(x))
        self.pre_after_add_directory_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                                          '140);}QPushButton:hover {border: 2px solid black; '
                                                          'border-style: solid;}')
        self.pre_after_add_directory_button.clicked.connect(
            lambda x=self.pre_after_add_directory_button.objectName(): self.load_images(x))
        self.cancel_image_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                               '140);}QPushButton:hover {border: 2px solid black; '
                                               'border-style: solid;}')
        self.cancel_image_button.clicked.connect(self.slot_cancel_single_image)
        self.turn_image_right_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                                   '140);}QPushButton:hover {border: 2px solid black; '
                                                   'border-style: solid;}')
        self.turn_image_right_button.clicked.connect(self.slot_right_image_rotate)
        self.turn_left_image_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                                  '140);}QPushButton:hover {border: 2px solid black; '
                                                  'border-style: solid;}')
        self.turn_left_image_button.clicked.connect(self.slot_left_image_rotate)
        self.pre_clear_all_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                                '140);}QPushButton:hover {border: 2px solid black; '
                                                'border-style: solid;}')
        self.pre_clear_all_button.clicked.connect(self.slot_trash_all_images)
        self.preview_button.setStyleSheet('QPushButton {border-radius: 5px; color: rgb(140, 140, '
                                          '140);}QPushButton:hover {border: 2px solid black; '
                                          'border-style: solid;}')
        self.updown_preview_button.clicked.connect(self.slot_up_scroll)
        self.more_change_quality_slider.setStyleSheet("QSlider::groove:horizontal {"
                                                      "border: 1px solid #bbb;"
                                                      "background-color: #ddd;"
                                                      "height: 10px;"
                                                      "border-radius: 5px;"
                                                      "}"
                                                      "QSlider::handle:horizontal {"
                                                      "background-color: gray;"
                                                      "border: 1px solid #777;"
                                                      "width: 20px;"
                                                      "height: 20px;"
                                                      "border-radius: 10px;"
                                                      "margin: -5px 0;"
                                                      "}")
        self.change_size_button.clicked.connect(lambda: self.slot_move_save_setting_widget('change_size_click_widget'))
        self.change_size_click_widget.mouseReleaseEvent = lambda event: self.slot_move_save_setting_widget(
            'change_size_click_widget')
        self.rename_image_button.clicked.connect(
            lambda: self.slot_move_save_setting_widget('rename_images_click_widget'))
        self.rename_images_click_widget.mouseReleaseEvent = lambda event: self.slot_move_save_setting_widget(
            'rename_images_click_widget')
        self.more_func_button.clicked.connect(
            lambda: self.slot_move_save_setting_widget('more_other_click_widget'))
        self.more_other_click_widget.mouseReleaseEvent = lambda event: self.slot_move_save_setting_widget(
            'more_other_click_widget')
        self.pre_load_trash_widget.hide()
        self.pre_deal_tools_frame.hide()
        self.display_widget.hide()
        self.setAcceptDrops(True)
        self.grid_widget = None
        self.add_target_button.clicked.connect(self.slot_add_target)
        self.crop_circle_button.clicked.connect(self.slot_crop2circle)
        # 创建一个Item Model
        self.item_model = QStandardItemModel()
        # lineEdit聚焦
        self.rename_first_ledit.focusInEvent = self.event_focus_in_first_edit
        self.rename_order_num_ledit.focusInEvent = self.event_focus_in_order_edit
        self.rename_image_false_rbutton.clicked.connect(self.event_click_rename_image_false_rbutton)
        self.rename_first_ledit.keyReleaseEvent = self.event_watch_first_ledit_input
        self.check_order_button.clicked.connect(self.check_order)
        self.clear_order_button.clicked.connect(self.clear_order)
        self.preview_order_button.clicked.connect(self.preview_order)
        self.pre_page_btn.clicked.connect(self.load_pre_page)
        self.next_page_btn.clicked.connect(self.load_next_page)
        self.cookie_text_edit.textChanged.connect(self.change_cookie)
        # self.shopify_orders_widget.hide()

    # # 添加特殊背景
    # def add_new_bg(self):
    #     img_paths =

    # 修改cookie
    def change_cookie(self):
        with open('cookie.txt', 'w') as f:
            f.write(self.cookie_text_edit.toPlainText())
            f.close()

    # 预览订单
    def preview_order(self):
        self.preview_shopify_order_widget = PreviewShopifyWidget()
        orders = self.all_order_lineedit.text().split(' ')
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        data = []
        for i, order in enumerate(orders):
            # order = '#' + order
            print(order)
            c.execute(f'select * from orders where order_id="{order}";')
            order = c.fetchall()
            print(order)
            for d in order:
                data.append(d)
        conn.close()
        self.preview_shopify_order_widget.shopify_table_widget.setRowCount(len(data))
        for i, d in enumerate(data):
            for j in range(6):
                self.preview_shopify_order_widget.shopify_table_widget.setItem(i, j, QTableWidgetItem(str(d[j])))
        self.preview_shopify_order_widget.change_order_directory_btton.clicked.connect(self.change_order_directory)
        self.preview_shopify_order_widget.save_order_button.clicked.connect(self.save_order)
        self.preview_shopify_order_widget.show()

    # 保存excel文件的位置
    def change_order_directory(self):
        dir = QFileDialog.getExistingDirectory(self, "选择存储文件夹", os.getcwd())
        self.preview_shopify_order_widget.order_directory_lineedit.setText(dir)

    # excel文件名
    def save_order(self):
        excel_name = self.preview_shopify_order_widget.order_excel_lineeidt.text() + '.xlsx'
        cells = []
        for i in range(self.preview_shopify_order_widget.shopify_table_widget.rowCount()):
            cell = []
            for j in range(6):
                cell.append(self.preview_shopify_order_widget.shopify_table_widget.item(i, j).text())
            cells.append(cell)
        df = pd.DataFrame(data=cells, columns=["Order", "Title", "Variant title", "quantity", "Carga to imagen", "Thumbnail"])
        df.to_excel(self.preview_shopify_order_widget.order_directory_lineedit.text() + '/' + excel_name, index=False)
        self.preview_shopify_order_widget.close()

    # 勾选订单
    def check_order(self):
        for i in range(self.shopify_model.rowCount()):
            item = self.shopify_model.item(i, 0)
            if item.text().strip('#') in self.add_order_lineedit.text():
                item.setCheckState(Qt.Checked)
                self.all_order_lineedit.setText(self.all_order_lineedit.text() + item.text() + ' ')

    # 加载下一页订单
    def load_next_page(self):
        self.page += 1
        self.order_widget.hide()
        self.row_index = 0
        url = 'https://admin.shopify.com/store/alanna-mx/orders.json?inContextTimeframe=none&after' \
              '=eyJsYXN0X2lkIjo1MDg1MDQ4ODk3NzAzLCJsYXN0X3ZhbHVlIjoiMjAyMy0wNy0xOSAyMzozNzoyOC40MDA1MDMifQ%3D%3D' \
              '&direction=next&last_id=' + str(self.last_id[self.page - 1])
        cookie = open('cookie.txt', 'r').read()
        self.load_thread = LoadShopifyOrdersThread(url, cookie)
        self.shopify_model = QStandardItemModel()
        self.shopify_model.itemChanged.connect(self.model_change)
        self.shopify_model.setHorizontalHeaderLabels(['Order', 'Date', 'Customer', 'Channel', 'Total', 'Payment status',
                                                      'Fulfillment status', 'Items', 'Delivery method', 'Tags'])
        self.order_checkbox = QCheckBox(self.tab_2)
        self.order_checkbox.clicked.connect(self.update_check_state)
        self.order_checkbox.setGeometry(QRect(self.tab_2.x() + 50, self.tab_2.y() + 165, 20, 20))
        self.shopify_tabelview.setAlternatingRowColors(True)
        self.load_thread.loading.connect(self.update_shopify_table)
        self.cover_shopify_label.setGeometry(0, 0, 1350, 960)
        self.cover_shopify_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(':/pic/images/loading.gif')
        self.cover_shopify_label.setMovie(self.movie)
        self.movie.start()
        self.load_thread.start()
        self.pre_page_btn.setCheckable(True)
        self.pre_page_btn.setStyleSheet('border-radius: 5px;color: rgb(0, 0, 0);background-color: rgb(255, '
                                        '255, 255);')

    def load_pre_page(self):
        self.page -= 1
        if self.page == 0:
            url = 'https://admin.shopify.com/store/alanna-mx/orders.json'
            self.load_shopify_orders(url)
            self.pre_page_btn.setCheckable(False)
            self.pre_page_btn.setStyleSheet('border-radius: 5px;color: rgb(216, 216, 216);background-color: rgb(255, '
                                            '255, 255);')
        else:
            self.order_widget.hide()
            self.row_index = 0
            url = 'https://admin.shopify.com/store/alanna-mx/orders.json?inContextTimeframe=none&after' \
                  '=eyJsYXN0X2lkIjo1MzI1NzgzODI2NzQ3LCJsYXN0X3ZhbHVlIjoiMjAyMy0wNi0xMSAyMzozMDoyNi45MzQ1NjAifQ%3D%3D' \
                  '&direction=next&last_id=' + str(self.last_id[self.page - 1])
            cookie = open('cookie.txt', 'r').read()
            self.load_thread = LoadShopifyOrdersThread(url, cookie)
            self.shopify_model = QStandardItemModel()
            self.shopify_model.itemChanged.connect(self.model_change)
            self.shopify_model.setHorizontalHeaderLabels(
                ['Order', 'Date', 'Customer', 'Channel', 'Total', 'Payment status',
                 'Fulfillment status', 'Items', 'Delivery method', 'Tags'])
            self.order_checkbox = QCheckBox(self.tab_2)
            self.order_checkbox.clicked.connect(self.update_check_state)
            self.order_checkbox.setGeometry(QRect(self.tab_2.x() + 50, self.tab_2.y() + 165, 20, 20))
            self.shopify_tabelview.setAlternatingRowColors(True)
            self.load_thread.loading.connect(self.update_shopify_table)
            self.cover_shopify_label.setGeometry(0, 0, 1350, 960)
            self.cover_shopify_label.setAlignment(Qt.AlignCenter)
            self.movie = QMovie(':/pic/images/loading.gif')
            self.cover_shopify_label.setMovie(self.movie)
            self.movie.start()
            self.load_thread.start()

    # 取消勾选订单
    def clear_order(self):
        for i in range(self.shopify_model.rowCount()):
            item = self.shopify_model.item(i, 0)
            item.setCheckState(Qt.Unchecked)

    # 搜索订单
    def search_order(self):
        gaol_order = self.search_box.text()
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        sql = f"select * from orders where order_id='{gaol_order}'"
        c.execute(sql)
        orders = c.fetchall()

    # 加载订单
    def load_shopify_orders(self, url):
        self.order_widget.hide()
        self.row_index = 0
        cookie = open('cookie.txt', 'r').read()
        self.load_thread = LoadShopifyOrdersThread(url, cookie)
        self.shopify_model = QStandardItemModel()
        self.shopify_model.itemChanged.connect(self.model_change)
        self.shopify_model.setHorizontalHeaderLabels(['Order', 'Date', 'Customer', 'Channel', 'Total', 'Payment status',
                                                      'Fulfillment status', 'Items', 'Delivery method', 'Tags'])
        self.order_checkbox = QCheckBox(self.tab_2)
        self.order_checkbox.clicked.connect(self.update_check_state)
        self.order_checkbox.setGeometry(QRect(self.tab_2.x() + 50, self.tab_2.y() + 165, 20, 20))
        self.shopify_tabelview.setAlternatingRowColors(True)
        self.load_thread.loading.connect(self.update_shopify_table)
        self.cover_shopify_label.setGeometry(0, 0, 1350, 960)
        self.cover_shopify_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(':/pic/images/loading.gif')
        self.cover_shopify_label.setMovie(self.movie)
        self.movie.start()
        self.load_thread.start()

    def model_change(self):
        checked = 0
        unchecked = 0
        for i in range(self.shopify_model.rowCount()):
            if self.shopify_model.item(i, 0).checkState() == Qt.Checked:
                checked += 1
            else:
                unchecked += 1
        if checked and unchecked:
            self.order_checkbox.setCheckState(True)
        elif checked:
            self.order_checkbox.setChecked(True)
        else:
            self.order_checkbox.setChecked(False)

    def update_check_state(self):
        if self.order_checkbox.isChecked():
            for i in range(self.shopify_model.rowCount()):
                self.shopify_model.item(i, 0).setCheckState(Qt.Checked)
        else:
            for i in range(self.shopify_model.rowCount()):
                self.shopify_model.item(i, 0).setCheckState(Qt.Unchecked)

    def update_shopify_table(self, order):
        for col_index, item in enumerate(order[0:-1]):
            if col_index == 0:
                item = QStandardItem(item)
                item.setCheckable(True)
                self.shopify_model.setItem(self.row_index, col_index, item)
                # checkbox_delegate = CheckBoxDelegate(text=item)
                # self.shopify_tabelview.setItemDelegateForColumn(0, checkbox_delegate)
            self.shopify_model.setItem(self.row_index, col_index, QStandardItem(item))
        self.row_index += 1
        self.last_id[self.page] = order[-1]
        if self.row_index == 50:
            self.cover_shopify_label.setGeometry(0, 0, 0, 0)
            self.order_checkbox.show()
            self.order_widget.show()
        self.shopify_tabelview.setModel(self.shopify_model)

    def event_click_rename_image_false_rbutton(self, e):
        self.rename_first_ledit.setPlaceholderText('例如：mtxx')
        self.rename_order_num_ledit.setPlaceholderText('例如：01')
        self.rename_display_example_label.setText('mtxx01、mtxx02...')

    def event_focus_in_first_edit(self, e):
        QLineEdit.focusInEvent(self.rename_first_ledit, e)
        self.rename_image_true_rbutton.click()
        self.rename_first_ledit.setPlaceholderText('')
        self.rename_display_example_label.setText('01、02...')
        if self.rename_order_num_ledit.placeholderText() == '':
            self.rename_display_example_label.setText('')
        self.rename_first_ledit.setFocusPolicy(Qt.StrongFocus)

    def event_focus_in_order_edit(self, e):
        QLineEdit.focusInEvent(self.rename_order_num_ledit, e)
        self.rename_image_true_rbutton.click()
        self.rename_order_num_ledit.setPlaceholderText('')
        self.rename_display_example_label.setText('mtxx0、mtxx1...')
        if self.rename_first_ledit.placeholderText() == '':
            self.rename_display_example_label.setText('')
        self.rename_first_ledit.setFocusPolicy(Qt.StrongFocus)

    def event_watch_first_ledit_input(self, e):
        text = self.rename_first_ledit.text()
        if self.rename_order_num_ledit.placeholderText() == '':
            self.rename_display_example_label.setText(f'{text}0、{text}1...')
        else:
            self.rename_display_example_label.setText(f'{text}01、{text}02...')

    def enter_pre_deal_label(self, QEvent):
        self.pre_deal_label.setPixmap(
            QPixmap(":/pic/images/after-deal-1.png"))
        self.pre_deal_text_label.setStyleSheet('color: rgb(255, 255, 255);')

    def click_pre_deal_label(self, QEvent):
        self.tabWidget.setCurrentIndex(0)

    def leave_pre_deal_label(self, QEvent):
        self.pre_deal_label.setPixmap(
            QPixmap(":/pic/images/pre-deal.png"))
        self.pre_deal_text_label.setStyleSheet('color: rgb(0, 0, 0);')

    def enter_get_images_label(self, QEvent):
        self.get_images_label.setPixmap(
            QPixmap(":/pic/images/after-download.png"))
        self.get_images_text_label.setStyleSheet('color: rgb(255, 255, 255);')

    def enter_shopify_label(self, QEvent):
        self.shopify_orders_label.setPixmap(
            QPixmap(":/pic/images/shopify_white.png"))
        self.shopify_orders_text_label.setStyleSheet('color: rgb(255, 255, 255);')

    def click_shopify_label(self, QEvent):
        self.tabWidget.setCurrentIndex(3)
        self.load_shopify_orders('https://admin.shopify.com/store/alanna-mx/orders.json')

    def click_get_images_label(self, QEvent):
        self.tabWidget.setCurrentIndex(2)

    def enter_help_label(self, QEvent):
        self.help_label.setPixmap(
            QPixmap(":/pic/images/after-help.png"))
        self.help_text_label.setStyleSheet('color: rgb(255, 255, 255);')

    def enter_setting_label(self, QEvent):
        self.setting_label.setPixmap(
            QPixmap(":/pic/images/after-setting.png"))
        self.setting_text_label.setStyleSheet('color: rgb(255, 255, 255);')

    def click_setting_label(self, QEvent):
        self.tabWidget.setCurrentIndex(1)

    def leave_get_images_label(self, QEvent):
        self.get_images_label.setPixmap(
            QPixmap(":/pic/images/pre-download.png"))
        self.get_images_text_label.setStyleSheet('color: rgb(0, 0, 0);')

    def leave_shopify_label(self, QEvent):
        self.shopify_orders_label.setPixmap(
            QPixmap(":/pic/images/shopify_black.png"))
        self.shopify_orders_text_label.setStyleSheet('color: rgb(0, 0, 0);')

    def leave_help_label(self, QEvent):
        self.help_label.setPixmap(
            QPixmap(":/pic/images/pre-help.png"))
        self.help_text_label.setStyleSheet('color: rgb(0, 0, 0);')

    def leave_setting_label(self, QEvent):
        self.setting_label.setPixmap(
            QPixmap(":/pic/images/pre-help.png"))
        self.setting_text_label.setStyleSheet('color: rgb(0, 0, 0);')

    def slot_is_clicked_add_images_label(self, is_clicked):
        if is_clicked:
            files, _ = QFileDialog.getOpenFileNames(self, "选择图片",
                                                    os.getcwd(), '所有格式(*.bmp;*.jpg;*.png;*.tif;*.gif;*.pcx;*.tga;'
                                                                 '*.exif;*.fpx;*.svg;*.psd;*.cdr;*.pcd;*.dxf;*.ufo;'
                                                                 '*.eps;*.ai;*.raw;*.WMF;*.webp;*.avif;*.apng;*.jpeg)'
                                                                 ';;Files(*.jpg; *.jpeg; *.jfif);;Files(*.png; *.webp)')
            self.load_images(files)

    def slot_is_clicked_add_directory_label(self, is_clicked):
        if is_clicked:
            directory = QFileDialog.getExistingDirectory(self, "选择存储文件夹", os.getcwd())
            files = os.listdir(directory)
            files = [directory + '/' + file for file in files]
            self.load_images(files)

    def load_images(self, object_name):
        if object_name == 'add_images_label' or 'pre_after_add_images_button':
            files, _ = QFileDialog.getOpenFileNames(self, "选择图片", os.getcwd(),
                                                    '所有格式(*.bmp;*.jpg;*.png;*.tif;*.gif;*.pcx;*.tga;'
                                                    '*.exif;*.fpx;*.svg;*.psd;*.cdr;*.pcd;*.dxf;*.ufo;'
                                                    '*.eps;*.ai;*.raw;*.WMF;*.webp;*.avif;*.apng;*.jpeg)'
                                                    ';;Files(*.jpg; *.jpeg; *.jfif);;Files(*.png; *.webp)')
        else:
            directory = QFileDialog.getExistingDirectory(self, "选择存储文件夹", os.getcwd())
            if directory:
                files = [directory + '/' + file for file in os.listdir(directory)]
            else:
                files = []
        if files:
            self.add_image_dir_label.hide()
            self.add_images_label.hide()
            self.or_label.hide()
            col = 4
            start_option = [0, 0]
            if not self.grid_widget:
                self.grid_widget = QGridLayout()
                self.scrollAreaWidgetContents_4.setLayout(self.grid_widget)
            labels = self.grid_widget.count()
            if labels % col == 0:
                if len(files) % col >= 1:
                    row = len(files) // col + 1
                else:
                    row = len(files) // col
                start_option[0] = labels // col
                start_option[1] = 0
            else:
                start_option[1] = labels % col
                if (len(files) + start_option[1]) % col >= 1:
                    row = (len(files) + start_option[1]) // col + 1
                else:
                    row = (len(files) + start_option[1]) // col
                start_option[0] = labels // col
            i = 0
            for r in range(start_option[0], row + start_option[0]):
                for c in range(start_option[1], col):
                    if i == len(files):
                        break
                    file = files[i]
                    i += 1
                    img = Image.open(file)
                    max_side = max(img.size)
                    w = int(img.width / (max_side / 140))
                    h = int(img.height / (max_side / 140))
                    img = img.resize((w, h), Image.BICUBIC)
                    target_widget = PreWidget(self)
                    target_widget.setObjectName(f'row_{r}_col_{c}_pre_widget')
                    target_widget.setFixedSize(140, 140)
                    img_label = QLabel(target_widget)
                    img_label.setAlignment(Qt.AlignCenter)
                    img_label.setGeometry(0, 0, 140, 140)
                    img_label.setObjectName(f'row_{r}_col_{c}_pre_widget_label')
                    qimg = ImageQt.ImageQt(img)
                    qimg.setText('FilePath', file)
                    qimg.setText('Image', f'row_{r}_col_{c}_pre_widget_label_qimg')
                    pixmap = QPixmap.fromImage(qimg)
                    img_label.setPixmap(pixmap)
                    target_cancel_label = DealImagesLabel(':/pic/images/cancel.png',
                                                          f'row_{r}_col_{c}_pre_widget_cancel_label',
                                                          target_widget)
                    target_cancel_label.setGeometry(110, 0, 20, 20)
                    target_cancel_label.setStyleSheet('QLabel {border-radius: 10px;}QLabel:hover {'
                                                      'background-color:rgba(255, 25, 60, 150);}')
                    target_cancel_label.setObjectName(f'row_{r}_col_{c}_pre_widget_cancel_label')
                    target_cancel_label.clicked.connect(self.slot_cancel_image)
                    target_cancel_label.hide()
                    pre_rotate_left_label = DealImagesLabel(':/pic/images/left-rotation.png',
                                                            f'row_{r}_col_{c}_pre_widget_left_label',
                                                            target_widget)
                    pre_rotate_left_label.setGeometry(10, 120, 20, 20)
                    pre_rotate_left_label.setStyleSheet('QLabel {border-radius: 10px;}QLabel:hover {'
                                                        'background-color:rgba(255, 25, 60, 150);}')
                    pre_rotate_left_label.clicked.connect(self.slot_left_rotate)
                    pre_rotate_left_label.hide()
                    pre_rotate_right_label = DealImagesLabel(':/pic/images/right-rotation.png',
                                                             f'row_{r}_col_{c}_pre_widget_right_label',
                                                             target_widget)
                    pre_rotate_right_label.setGeometry(110, 120, 20, 20)
                    pre_rotate_right_label.setStyleSheet('QLabel {border-radius: 10px;}QLabel:hover {'
                                                         'background-color:rgba(255, 25, 60, 150);}')
                    pre_rotate_right_label.clicked.connect(self.slot_right_rotate)
                    pre_rotate_right_label.hide()
                    self.grid_widget.addWidget(target_widget, r, c, Qt.AlignCenter)
                    target_widget.clicked.connect(self.slot_click_pre_image)
                if start_option[1] != 0:
                    start_option[1] = 0
            self.images_num_label.setText(str(self.grid_widget.count()))
            self.pre_deal_scroll_area.show()
            self.pre_load_trash_widget.show()
            self.display_widget.show()
            self.pre_deal_tools_frame.show()

    def slot_click_pre_image(self, object_name):
        for widget in self.findChildren(QWidget,
                                        QRegExp(r'row_\d+_col_\d+_pre_widget$', Qt.CaseSensitive)):
            widget.findChild(QLabel, widget.objectName() + '_label').setStyleSheet('border: none;')
        self.findChild(QLabel, object_name + '_label').setStyleSheet('border: 5px solid gray; border-style: solid;')
        img = self.findChild(QLabel, object_name + '_label').pixmap().toImage()
        qimg = img.scaled(280, 280, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.display_widget_label.setPixmap(QPixmap.fromImage(qimg))

    # 逆时针旋转图片
    def slot_left_rotate(self, name):
        label = self.findChild(QLabel, name.replace('_left', ''))
        pixmap = label.pixmap()
        transform = QTransform().rotate(-90)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        label.setPixmap(rotated_pixmap)

    def slot_left_image_rotate(self):
        for label in self.findChildren(QLabel,
                                       QRegExp(r'row_\d+_col_\d+_pre_widget_label$', Qt.CaseSensitive)):
            if label.styleSheet() == 'border: 5px solid gray; border-style: solid;':
                self.slot_left_rotate(label.objectName())
                break

    # 顺时针旋转图片
    def slot_right_rotate(self, name):
        label = self.findChild(QLabel, name.replace('_right', ''))
        pixmap = label.pixmap()
        transform = QTransform().rotate(90)
        rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        label.setPixmap(rotated_pixmap)

    def slot_right_image_rotate(self):
        for label in self.findChildren(QLabel,
                                       QRegExp(r'row_\d+_col_\d+_pre_widget_label$', Qt.CaseSensitive)):
            if label.styleSheet() == 'border: 5px solid gray; border-style: solid;':
                self.slot_left_rotate(label.objectName())
                break

    def slot_cancel_image(self, name):
        cancel_widget = self.findChild(QWidget, name.replace('_cancel_label', ''))
        widgets = self.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$', Qt.CaseSensitive))
        i = widgets.index(cancel_widget)
        new_positions = [tuple(re.findall(r'\d+', widget.objectName())) for widget in widgets][i:-1]
        new_names = [widget.objectName() for widget in widgets][i:-1]
        sip.delete(cancel_widget)
        exist_widgets = self.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$', Qt.CaseSensitive))[i:]
        for i, exist_widget in enumerate(exist_widgets):
            exist_name = exist_widget.objectName()
            exist_widget.setObjectName(new_names[i])
            exist_widget.findChild(QLabel, exist_name + '_label').setObjectName(new_names[i] + '_label')
            exist_widget.findChild(QLabel, exist_name + '_left_label').setObjectName(new_names[i] + '_left_label')
            exist_widget.findChild(QLabel, exist_name + '_cancel_label').setObjectName(new_names[i] + '_cancel_label')
            exist_widget.findChild(QLabel, exist_name + '_right_label').setObjectName(new_names[i] + '_right_label')
            self.grid_widget.addWidget(exist_widget, int(new_positions[i][0]), int(new_positions[i][1]), Qt.AlignCenter)
        self.images_num_label.setText(str(self.grid_widget.count()))
        if self.grid_widget.count() == 0:
            self.pre_deal_scroll_area.hide()
            self.pre_deal_tools_frame.hide()
            self.display_widget.hide()
            self.pre_load_trash_widget.hide()
            self.add_image_dir_label.show()
            self.add_images_label.show()
            self.or_label.show()
            self.grid_widget.deleteLater()
            self.grid_widget = None

    def slot_cancel_single_image(self):
        for label in self.findChildren(QLabel,
                                       QRegExp(r'row_\d+_col_\d+_pre_widget_label$', Qt.CaseSensitive)):
            if label.styleSheet() == 'border: 5px solid gray; border-style: solid;':
                self.slot_cancel_image(label.objectName().replace('_label', ''))
                break

    def slot_trash_all_images(self):
        messagebox = QMessageBox()
        messagebox.setWindowTitle('温馨提示')
        messagebox.setText('确定清空所有图片？')
        messagebox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        messagebox.setStyleSheet('background-color: white;')
        messagebox.setFixedSize(360, 160)
        response = messagebox.exec_()
        if response == QMessageBox.Ok:
            for label in self.findChildren(QLabel,
                                           QRegExp(r'row_\d+_col_\d+_pre_widget_label$', Qt.CaseSensitive)):
                self.slot_cancel_image(label.objectName().replace('_label', ''))

    def slot_tools_labels_color_change(self, is_enter, object_name):
        if is_enter:
            widget = self.pre_deal_tools_frame.findChild(QWidget, object_name)
            if 'add_other_images' in object_name:
                widget.findChild(QLabel, object_name.replace('widget', 'text_label')) \
                    .setStyleSheet('color: rgb(255, 255, 255); font: 14pt "黑体";')
                widget.findChild(QLabel, object_name.replace('widget', 'label')).setPixmap(
                    QPixmap(':/pic/images/add_images_after.png'))
            if 'clear_all' in object_name:
                widget.findChild(QLabel, object_name.replace('widget', 'text_label')) \
                    .setStyleSheet('color: rgb(255, 255, 255); font: 14pt "黑体";')
                widget.findChild(QLabel, object_name.replace('widget', 'label')).setPixmap(
                    QPixmap(':/pic/images/clear_all_after.png'))

    def slot_tools_labels_color_resume(self, is_leave, object_name):
        if not is_leave:
            widget = self.pre_deal_tools_frame.findChild(QWidget, object_name)
            if 'add_other_images' in object_name:
                widget.findChild(QLabel, object_name.replace('widget', 'text_label')) \
                    .setStyleSheet('color: rgb(100, 100, 100); font: 14pt "黑体";')
                widget.findChild(QLabel, object_name.replace('widget', 'label')).setPixmap(
                    QPixmap(':/pic/images/add_images.png'))
            if 'clear_all' in object_name:
                widget.findChild(QLabel, object_name.replace('widget', 'text_label')) \
                    .setStyleSheet('color: rgb(100, 100, 100); font: 14pt "黑体";')
                widget.findChild(QLabel, object_name.replace('widget', 'label')).setPixmap(
                    QPixmap(':/pic/images/clear_all.png'))

    def slot_up_scroll(self):
        if self.pre_load_trash_widget.pos().y() == 350:
            self.updown_preview_button.setIcon(QIcon(':/pic/images/dropdown_trash.png'))
            self.updown_preview_button.setIconSize(QSize(15, 15))
            group = QParallelAnimationGroup(self)
            animation = QPropertyAnimation(self.pre_load_trash_widget, b'pos')
            animation.setDuration(340)
            animation.setEndValue(self.pre_load_trash_widget.pos() + QPoint(0, -340))
            group.addAnimation(animation)
            group.start(QParallelAnimationGroup.DeleteWhenStopped)
            scroll_group = QParallelAnimationGroup(self)
            scroll_anim = QPropertyAnimation(self.pre_deal_scroll_area, b'pos')
            scroll_anim.setDuration(340)
            scroll_anim.setEndValue(self.pre_deal_scroll_area.pos() + QPoint(0, -340))
            scroll_group.addAnimation(scroll_anim)
            scroll_group.start(QParallelAnimationGroup.DeleteWhenStopped)
            self.pre_deal_scroll_area.setGeometry(0, 390, 631, 871)
        else:
            self.updown_preview_button.setIcon(QIcon(':/pic/images/updown.png'))
            self.updown_preview_button.setIconSize(QSize(20, 20))
            group = QParallelAnimationGroup(self)
            animation = QPropertyAnimation(self.pre_load_trash_widget, b'pos')
            animation.setDuration(340)
            animation.setEndValue(self.pre_load_trash_widget.pos() + QPoint(0, 340))
            group.addAnimation(animation)
            group.start(QParallelAnimationGroup.DeleteWhenStopped)
            scroll_group = QParallelAnimationGroup(self)
            scroll_anim = QPropertyAnimation(self.pre_deal_scroll_area, b'pos')
            scroll_anim.setDuration(340)
            scroll_anim.setEndValue(self.pre_deal_scroll_area.pos() + QPoint(0, 340))
            scroll_group.addAnimation(scroll_anim)
            scroll_group.start(QParallelAnimationGroup.DeleteWhenStopped)
            time.sleep(0.34)
            self.pre_deal_scroll_area.setGeometry(0, 50, 631, 531)

    def slot_move_save_setting_widget(self, widget_name):
        if widget_name == 'change_size_click_widget':
            self.move_change_size_widget()
        if widget_name == 'rename_images_click_widget':
            self.move_rename_widget()
        if widget_name == 'more_other_click_widget':
            self.move_more_func_widget()

    def move_more_func_widget(self):
        if self.more_other_func_widget.size().height() == 0:
            self.more_func_button.setIcon(QIcon(':/pic/images/dropdown_clicked.png'))
            self.more_func_button.setIconSize(QSize(20, 20))
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y(),
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height() + 120
            )
        else:
            self.more_func_button.setIcon(QIcon(':/pic/images/dropdown.png'))
            self.more_func_button.setIconSize(QSize(20, 20))
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y(),
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height() - 120
            )

    def move_rename_widget(self):
        if self.rename_image_widget.size().height() == 0:
            self.rename_image_button.setIcon(QIcon(':/pic/images/dropdown_clicked.png'))
            self.rename_image_button.setIconSize(QSize(20, 20))
            self.more_other_click_widget.setGeometry(
                self.more_other_click_widget.pos().x(), self.more_other_click_widget.pos().y() + 180,
                self.more_other_click_widget.size().width(), self.more_other_click_widget.size().height()
            )
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y() + 180,
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height()
            )
            self.rename_image_widget.setGeometry(
                self.rename_image_widget.pos().x(), self.rename_image_widget.pos().y(),
                self.rename_image_widget.size().width(), self.rename_image_widget.size().height() + 180
            )
        else:
            self.rename_image_button.setIcon(QIcon(':/pic/images/dropdown.png'))
            self.rename_image_button.setIconSize(QSize(20, 20))
            self.more_other_click_widget.setGeometry(
                self.more_other_click_widget.pos().x(), self.more_other_click_widget.pos().y() - 180,
                self.more_other_click_widget.size().width(), self.more_other_click_widget.size().height()
            )
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y() - 180,
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height()
            )
            self.rename_image_widget.setGeometry(
                self.rename_image_widget.pos().x(), self.rename_image_widget.pos().y(),
                self.rename_image_widget.size().width(), self.rename_image_widget.size().height() - 180
            )

    def move_change_size_widget(self):
        if self.change_size_widget.size().height() == 0:
            self.change_size_button.setIconSize(QSize(20, 20))
            self.change_size_button.setIcon(QIcon(':/pic/images/dropdown_clicked.png'))
            self.rename_images_click_widget.setGeometry(
                self.rename_images_click_widget.pos().x(), self.rename_images_click_widget.pos().y() + 140,
                self.rename_images_click_widget.size().width(), self.rename_images_click_widget.size().height()
            )
            self.rename_image_widget.setGeometry(
                self.rename_image_widget.pos().x(), self.rename_image_widget.pos().y() + 140,
                self.rename_image_widget.size().width(), self.rename_image_widget.size().height()
            )
            self.more_other_click_widget.setGeometry(
                self.more_other_click_widget.pos().x(), self.more_other_click_widget.pos().y() + 140,
                self.more_other_click_widget.size().width(), self.more_other_click_widget.size().height()
            )
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y() + 140,
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height()
            )
            self.change_size_widget.setGeometry(
                self.change_size_widget.pos().x(), self.change_size_widget.pos().y(),
                self.change_size_widget.size().width(), self.change_size_widget.size().height() + 140
            )
        else:
            self.change_size_button.setIconSize(QSize(20, 20))
            self.change_size_button.setIcon(QIcon(':/pic/images/dropdown.png'))
            self.rename_images_click_widget.setGeometry(
                self.rename_images_click_widget.pos().x(), self.rename_images_click_widget.pos().y() - 140,
                self.rename_images_click_widget.size().width(), self.rename_images_click_widget.size().height()
            )
            self.rename_image_widget.setGeometry(
                self.rename_image_widget.pos().x(), self.rename_image_widget.pos().y() - 140,
                self.rename_image_widget.size().width(), self.rename_image_widget.size().height()
            )
            self.more_other_click_widget.setGeometry(
                self.more_other_click_widget.pos().x(), self.more_other_click_widget.pos().y() - 140,
                self.more_other_click_widget.size().width(), self.more_other_click_widget.size().height()
            )
            self.more_other_func_widget.setGeometry(
                self.more_other_func_widget.pos().x(), self.more_other_func_widget.pos().y() - 140,
                self.more_other_func_widget.size().width(), self.more_other_func_widget.size().height()
            )
            self.change_size_widget.setGeometry(
                self.change_size_widget.pos().x(), self.change_size_widget.pos().y(),
                self.change_size_widget.size().width(), self.change_size_widget.size().height() - 140
            )

    # 加底
    def slot_add_target(self):
        widgets_list = self.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$', Qt.CaseSensitive))
        labels_list = [widget.findChild(QLabel, widget.objectName() + '_label') for widget in widgets_list]
        paths_list = [label.pixmap().toImage().text('FilePath') for label in labels_list]
        qimage_list = [label.pixmap().toImage() for label in labels_list]
        num_threads = 5
        bg_color = self.bg_image_widget.styleSheet().replace('background-color: ', '').replace(';', '')
        print(bg_color)
        path_list_pre_thread = [paths_list[i::num_threads] for i in range(num_threads)]
        qimage_list_pre_thread = [qimage_list[i::num_threads] for i in range(num_threads)]
        self.img_deal_threads = []
        self.add_target_progress_widget = ShowProgressWidget()
        self.add_target_progress_widget.show_repeat_progressbar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);  background-color: "
            "#FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: "
            "10px; margin: 0.1px;  width: 1px;}")
        self.add_target_progress_widget.show()
        self.n = 0
        for i in range(num_threads):
            thread = ImageAddTargetThread(img_paths=path_list_pre_thread[i], bg_color=bg_color,
                                          qimages=qimage_list_pre_thread[i], window=self)
            thread.completed.connect(self.update_add_target_progress)
            self.img_deal_threads.append(thread)
        # 启动所有的DownloadThread线程
        for thread in self.img_deal_threads:
            thread.start()

    # 裁圆
    def slot_crop2circle(self):
        widgets_list = self.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$', Qt.CaseSensitive))
        labels_list = [widget.findChild(QLabel, widget.objectName() + '_label') for widget in widgets_list]
        paths_list = [label.pixmap().toImage().text('FilePath') for label in labels_list]
        qimage_list = [label.pixmap().toImage() for label in labels_list]
        num_threads = 5
        path_list_pre_thread = [paths_list[i::num_threads] for i in range(num_threads)]
        qimage_list_pre_thread = [qimage_list[i::num_threads] for i in range(num_threads)]
        self.img_deal_threads = []
        self.add_target_progress_widget = ShowProgressWidget()
        self.add_target_progress_widget.show_repeat_progressbar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);  background-color: "
            "#FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: "
            "10px; margin: 0.1px;  width: 1px;}")
        self.add_target_progress_widget.show()
        self.n = 0
        for i in range(num_threads):
            thread = ImageCropperThread(img_paths=path_list_pre_thread[i], border_color=(31, 31, 31, 31),
                                        qimages=qimage_list_pre_thread[i], window=self)
            thread.completed.connect(self.update_add_target_progress)
            self.img_deal_threads.append(thread)
        # 启动所有的DownloadThread线程
        for thread in self.img_deal_threads:
            thread.start()

    def update_add_target_progress(self, path):
        self.n += 1
        num = len(self.findChildren(QLabel, QRegExp(r'row_\d+_col_\d+_pre_widget_label$', Qt.CaseSensitive)))
        self.add_target_progress_widget.show_repeat_progressbar.setValue(int(self.n / num * 100))
        self.add_target_progress_widget.show_repeat_name_label.setText(path)
        if self.n == num:
            time.sleep(0.5)
            self.add_target_progress_widget.hide()
            self.add_target_progress_widget.deleteLater()

    def slot_find_repeat_images(self):
        self.show_repeat_progress_widget = ShowProgressWidget()
        self.show_repeat_progress_widget.show_repeat_progressbar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);  background-color: "
            "#FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: "
            "10px; margin: 0.1px;  width: 1px;}")
        self.show_repeat_progress_widget.show()
        self.n = 1
        widgets = self.scrollAreaWidgetContents_4.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$',
                                                                                Qt.CaseSensitive))
        self.show_similar_progress_thread = ShowProgressThread(widgets)
        self.show_similar_progress_thread.clicked.connect(self.slot_start_find_repeat)
        self.show_similar_progress_thread.start()

    def slot_start_find_repeat(self, image_path):
        widgets = self.scrollAreaWidgetContents_4.findChildren(QWidget, QRegExp(r'row_\d+_col_\d+_pre_widget$',
                                                                                Qt.CaseSensitive))
        self.n += 1
        self.show_repeat_progress_widget.show_repeat_progressbar.setValue(int(self.n / len(widgets) * 100))
        self.show_repeat_progress_widget.show_repeat_name_label.setText(image_path)
        if self.n == len(widgets):
            time.sleep(0.5)
            self.show_repeat_progress_widget.hide()
            self.show_repeat_progress_widget.close()
            self.show_repeat_progress_widget.deleteLater()

    # 读取excel文件
    def slot_read_excel(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择文件",
                                              os.getcwd(), '所有格式(*.xlsx;*.xls)')
        self.save_images_directory_ledit.setText(file.split('.xls')[0])
        self.get_images_excel_ledit.setText(file)
        if self.get_images_excel_ledit.text():
            df = pd.read_excel(self.get_images_excel_ledit.text())
            headers = df.columns.astype(str).tolist()
            for i, h in enumerate(headers):
                self.get_images_sheet_headers_combox.addItem('')
                self.get_images_sheet_urls_combox.addItem('')
                self.get_images_sheet_nums_combox.addItem('')
                self.get_images_sheet_headers_combox.setItemText(i, h)
                self.get_images_sheet_urls_combox.setItemText(i, h)
                self.get_images_sheet_nums_combox.setItemText(i, h)
            data = df.values
            excel_tabel_model = MyTableModel(data, headers)
            self.exceltableView.setModel(excel_tabel_model)

    # 添加example列名
    def slot_add_col_name(self):
        df = pd.read_excel(self.get_images_excel_ledit.text())
        for i in range(26):
            if i == self.get_images_sheet_headers_combox.currentIndex():
                example_col = df.iloc[0, i]
                original_example_col = self.get_images_show_example_ledit.text()
                if original_example_col:
                    self.get_images_show_example_ledit.setText(
                        original_example_col + self.get_images_split_ledit.text() + str(example_col))
                    col_name = self.add_col_name_label.text() + '+' + self.get_images_sheet_headers_combox.currentText()
                else:
                    self.get_images_show_example_ledit.setText(str(example_col))
                    col_name = self.get_images_sheet_headers_combox.currentText()
                self.add_col_name_label.setText(col_name)

    # 设置保存图片的文件夹
    def slot_save_images_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, '保存文件夹', os.getcwd())
        self.save_images_directory_ledit.setText(dir_name)

    # 开始导出图片
    def slot_start_download_images(self):
        # 获取图片链接列表
        # pandas处理excel文件
        df = pd.read_excel(self.get_images_excel_ledit.text())
        df = df.loc[df.iloc[:, self.get_images_sheet_urls_combox.currentIndex()].fillna('').apply(
            self.apply_get_urls) != '']
        urls = df.iloc[:, self.get_images_sheet_urls_combox.currentIndex()].fillna('').apply(
            self.apply_get_urls).tolist()
        num_list = df.iloc[:, self.get_images_sheet_nums_combox.currentIndex()].fillna(0).astype(int).tolist()
        index_list = df.index.astype(int).tolist()
        image_names = None
        self.download_progressbar.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(20,20,20);  background-color: "
            "#FFFFFF; text-align: center;}QProgressBar::chunk {background-color: rgb(100,200,200); border-radius: "
            "10px; margin: 0.1px;  width: 1px;}")
        for text in self.add_col_name_label.text().split('+'):
            i = self.get_images_sheet_headers_combox.findText(text)
            if type(image_names) == type(None):
                image_names = df.iloc[:, i].fillna('').astype(str).apply(lambda x: re.sub(r'"|\n|/|\*|\?|\\', '', x))
            else:
                sep = self.get_images_split_ledit.text()
                image_names = image_names.str.cat(
                    [df.iloc[:, i].fillna('').astype(str).apply(lambda x: re.sub(r'"|\n|/|\*|\?|\\', '', x))], sep=sep)
        dir_name = self.save_images_directory_ledit.text()
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        path_list = [dir_name + '/' + image_name + '.png' for image_name in image_names]
        # 创建QThread对象并启动线程
        self.item_model = QStandardItemModel()
        url_list = urls  # 所有的URL列表
        num_threads = self.downloading_thread_nums_spinBox.value()  # 线程数量
        # 将所有的URL列表分成num_threads份，分别传给num_threads个ImageDownloadThread实例
        url_list_per_thread = [url_list[i::num_threads] for i in range(num_threads)]
        path_list_pre_thread = [path_list[i::num_threads] for i in range(num_threads)]
        num_list_pre_thread = [num_list[i::num_threads] for i in range(num_threads)]
        index_list_pre_thread = [index_list[i::num_threads] for i in range(num_threads)]
        self.threads = []
        self.img_nums = sum(num_list)
        self.img_num = len(url_list)
        for i in range(num_threads):
            thread = DownloadTask(url_list_per_thread[i], path_list_pre_thread[i], num_list_pre_thread[i],
                                  index_list_pre_thread[i])
            thread.write_log.connect(self.update_list_view)
            self.threads.append(thread)
        # 启动所有的DownloadThread线程
        for thread in self.threads:
            thread.start()
        self.start_download_button.setEnabled(False)
        self.resume_download_button.setEnabled(False)
        self.pause_download_button.setEnabled(True)
        self.stop_download_button.setEnabled(True)
        self.pause_download_button.clicked.connect(self.do_wait)
        self.resume_download_button.clicked.connect(self.do_wake)
        self.stop_download_button.clicked.connect(self.do_end)

    def apply_get_urls(self, x):
        match = re.search(r'(https?://\S+|(\.?:png|jpe?g|gif)|(\?v=\n+))|(\?ph_image=\S+)', x)
        if match:
            x = match.group()
        else:
            x = ''
        if 'ph_image' in x:
            x = 'https://uploadly-files.com/' + \
                x.split('ph_image=')[1].split('&')[0] + '.' + x.split('extension=')[1].split('&')[0].replace('=', '')
        if 'download.html' in x:
            url_query = urlparse(x).query
            fi = parse_qs(url_query).get('fi')[0]
            id = parse_qs(url_query).get('id')[0]
            uuid = parse_qs(url_query).get('uu')[0]
            modifiers = parse_qs(url_query).get('mo')[0]
            decodedFilename = base64.b64decode(fi).decode()
            x = "https://files.getuploadkit.com/" + id + "/" + uuid + "/" + modifiers + decodedFilename + "?dl=1"
        print(x)
        return x

    def update_list_view(self, row, log):
        item = QStandardItem(log)
        self.item_model.setItem(row, item)
        progress = len(os.listdir(self.save_images_directory_ledit.text())) / self.img_nums * 100
        self.download_progressbar.setValue(int(progress))
        if int(progress) == 100:
            item = QStandardItem('图片爬取完成！')
            self.item_model.setItem(self.img_num, item)
        self.downlaod_images_log_listView.setModel(self.item_model)

    def do_wait(self):
        for t in self.threads:
            t.pause()
        self.start_download_button.setEnabled(False)
        self.resume_download_button.setEnabled(True)
        self.pause_download_button.setEnabled(False)
        self.stop_download_button.setEnabled(False)

    def do_wake(self):
        for t in self.threads:
            t.resume()
        self.start_download_button.setEnabled(False)
        self.resume_download_button.setEnabled(False)
        self.pause_download_button.setEnabled(True)
        self.stop_download_button.setEnabled(True)

    def do_end(self):
        for t in self.threads:
            t.stop()
        self.start_download_button.setEnabled(True)
        self.resume_download_button.setEnabled(False)
        self.pause_download_button.setEnabled(False)
        self.stop_download_button.setEnabled(False)

    # 新建背景图片
    def slot_new_color_bg(self):
        self.new_bg_widget = NewBackground()
        self.new_bg_widget.show()
        self.new_bg_widget.select_white_label.select_signal.connect(self.slot_select_color_label)
        self.new_bg_widget.select_transparen_label.select_signal.connect(self.slot_select_color_label)
        self.new_bg_widget.define_color_label.select_signal.connect(self.slot_select_color_label)
        self.new_bg_widget.ensure_bg_button.clicked.connect(
            lambda: self.bg_image_widget.setStyleSheet(f'background-color: {self.new_bg_widget.selected_color};')
        )
        self.new_bg_widget.ensure_bg_button.clicked.connect(self.new_bg_widget.close)
        self.new_bg_widget.cancel_bg_button.clicked.connect(self.new_bg_widget.close)

    def slot_select_color_label(self, is_select, object_name):
        if 'white' in object_name:
            self.new_bg_widget.select_white_label.selected = is_select
            self.new_bg_widget.select_transparen_label.setPixmap(QPixmap())
            self.new_bg_widget.define_color_label.setPixmap(QPixmap())
        if 'transparen' in object_name:
            self.new_bg_widget.select_transparen_label.selected = is_select
            self.new_bg_widget.select_white_label.setPixmap(QPixmap())
            self.new_bg_widget.define_color_label.setPixmap(QPixmap())
        if 'define' in object_name:
            self.new_bg_widget.define_color_label.selected = is_select
            self.new_bg_widget.select_transparen_label.setPixmap(QPixmap())
            self.new_bg_widget.select_white_label.setPixmap(QPixmap())


class ShowProgressWidget(QWidget, Ui_show_repeat_progress_form):
    def __init__(self, parent=None):
        super(ShowProgressWidget, self).__init__(parent)
        self.setupUi(self)


class PreviewShopifyWidget(QWidget, ShopifyPreviewOrderUi):
    def __init__(self, parent=None):
        super(PreviewShopifyWidget, self).__init__(parent)
        self.setupUi(self)


class NewBackground(QWidget, Ui_NewBackground):
    def __init__(self, parent=None):
        super(NewBackground, self).__init__(parent)
        self.selected_color = 'white'
        self.setupUi(self)
        qstyle = 'border-color: green;'
        s_sheet1 = self.select_white_label.styleSheet()
        geometry1 = self.select_white_label.geometry()
        s_sheet2 = self.select_transparen_label.styleSheet()
        geometry2 = self.select_transparen_label.geometry()
        s_sheet3 = self.define_color_label.styleSheet()
        geometry3 = self.define_color_label.geometry()
        self.select_white_label = SelectColorLabel(
            qstyle=qstyle, object_name=self.select_white_label.objectName(), parent=self
        )
        self.select_white_label.setStyleSheet(s_sheet1)
        self.select_white_label.setGeometry(geometry1)
        self.select_transparen_label = SelectColorLabel(
            qstyle=qstyle, object_name=self.select_transparen_label.objectName(), color='rgba(0, 0, 0, 0)', parent=self
        )
        self.select_transparen_label.setStyleSheet(s_sheet2)
        self.select_transparen_label.setGeometry(geometry2)
        self.define_color_label = SelectColorLabel(
            qstyle=qstyle, object_name=self.define_color_label.objectName(), parent=self
        )
        self.define_color_label.setStyleSheet(s_sheet3)
        self.define_color_label.setGeometry(geometry3)
        self.select_white_label.setPixmap(QPixmap(':/pic/images/right-tick.png'))
        self.select_white_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    index = Index()
    index.show()
    sys.exit(app.exec_())
