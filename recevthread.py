import io
import json
import shutil
import time
from PIL import Image

import requests
from PyQt5.QtCore import QThread, QMutex, pyqtSignal, QWaitCondition
from playwright.sync_api import sync_playwright

from workFunction import *
import datetime
from dateutil.parser import parse
import sqlite3
from curl_cffi import requests as cffi_requests


class ShowProgressThread(QThread):
    clicked = pyqtSignal(str)

    def __init__(self, widgets):
        super(ShowProgressThread, self).__init__()
        self.image_widgets = widgets

    def run(self) -> None:
        pre_widgets_list = [self.image_widgets[i:i + 2] for i in range(len(self.image_widgets) - 1)]
        for i in range(len(self.image_widgets) - 1):
            similarity_images_finder = SimilarityImagesFinder()
            images = similarity_images_finder.list_images(pre_widgets_list[i])
            images_resized = similarity_images_finder.resize_images(images)
            similar_images = similarity_images_finder.find_similar_images(images_resized)
            similarity_images_finder.rename_similar_images_path(similar_images, images, self.clicked)
            del similarity_images_finder


class DownloadTask(QThread):
    write_log = pyqtSignal(int, str)

    def __init__(self, url_list, path_list, num_list, index_list):
        super(DownloadTask, self).__init__()
        self.url_list = url_list
        self.path_list = path_list
        self.num_list = num_list
        self.index_list = index_list
        self._isPause = False
        self.cond = QWaitCondition()
        self.mutex = QMutex()

    def run(self):
        log = '图片爬取开始：'
        self.write_log.emit(0, log)
        for i, url in enumerate(self.url_list):
            self.mutex.lock()  # 上锁
            if self._isPause:
                self.cond.wait(self.mutex)
            path = os.path.splitext(self.path_list[i])[0] + '-' + str(self.index_list[i]) + \
                   os.path.splitext(self.path_list[i])[1]
            num = self.num_list[i]
            try:
                if os.path.exists(path):
                    log = f'图片 {path.split("/")[-1]} 已存在! '
                else:
                    if url == '':
                        continue
                    auto_download(url, path)
                    log = f'爬取图片 {url} 成功保存为 {path.split("/")[-1]} '
                    if num > 1:
                        for j in range(1, num):
                            shutil.copy(path, os.path.splitext(path)[0] + '-' + str(j) + os.path.splitext(path)[1])
                self.write_log.emit(self.index_list[i], log)
            except Exception as e:
                print(e)
                log = f'爬取图片 {url} 失败！文件名 {path.split("/")[-1]}'
                self.write_log.emit(self.index_list[i], log)
            self.mutex.unlock()  # 解锁

    # 线程暂停
    def pause(self):
        self._isPause = True

    # 线程恢复
    def resume(self):
        self._isPause = False
        self.cond.wakeAll()

    # 线程终止
    def stop(self):
        self._isPause = True


def auto_download(url, filename):
    # urlretrieve(url, filename)
    proxies = {
        'http': 'http://127.0.0.1:7897',
        'https': 'http://127.0.0.1:7897'
    }
    response = requests.get(url, verify=False, proxies=proxies)
    if '.svg' in url:
        filename = filename.strip('.png') + '.svg'
    # print(filename)
    expected_length = response.headers.get('Content-Length')
    if expected_length is not None:
        actual_length = response.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            print('图片不完整')
            auto_download(url, filename)
    with open(filename, 'wb') as fp:
        fp.write(response.content)


class ImageAddTargetThread(QThread):
    completed = pyqtSignal(str)

    def __init__(self, bg_color=(0, 0, 0), img_paths=..., qimages=..., border_color=(255, 255, 255, 0), window=None):
        super(ImageAddTargetThread, self).__init__()
        self.bg_color = bg_color
        self.img_paths = img_paths
        self.qimages = qimages
        self.border_color = border_color
        self.window = window

    def run(self) -> None:
        for i, path in enumerate(self.img_paths):
            dealer = ImageDealer()
            dealer.transfer(bg_color=self.bg_color, img_path=path, qimage=self.qimages[i], window=self.window)
            dealer.crop_border_box()
            dealer.add_single_color_target()
            self.completed.emit(path)


class ImageCropperThread(QThread):
    completed = pyqtSignal(str)

    def __init__(self, bg_color=(0, 0, 0), img_paths=..., qimages=..., border_color=(255, 255, 255, 0), window=None):
        super(ImageCropperThread, self).__init__()
        self.bg_color = bg_color
        self.img_paths = img_paths
        self.qimages = qimages
        self.border_color = border_color
        self.window = window

    def run(self) -> None:
        for i, path in enumerate(self.img_paths):
            dealer = ImageDealer()
            dealer.transfer(border_color=self.border_color, img_path=path, qimage=self.qimages[i], window=self.window)
            dealer.img_2_circle()
            self.completed.emit(path)


class ImageAddNewBg(QThread):
    completed = pyqtSignal(str)

    def __init__(self, bg_color=(0, 0, 0), img_paths=..., qimages=..., border_color=(255, 255, 255, 0), window=None):
        super(ImageAddNewBg, self).__init__()
        self.bg_color = bg_color
        self.img_paths = img_paths
        self.qimages = qimages
        self.border_color = border_color
        self.window = window

    def run(self) -> None:
        for i, path in enumerate(self.img_paths):
            dealer = ImageDealer()
            dealer.transfer(border_color=self.border_color, img_path=path, qimage=self.qimages[i], window=self.window)
            dealer.add_special_background()
            self.completed.emit(path)


class LoadShopifyOrdersThread(QThread):
    loading = pyqtSignal(list)

    def __init__(self, url, cookie):
        super(LoadShopifyOrdersThread, self).__init__()
        self.url = url
        self.orders = {'orders': []}
        self.cookie = cookie

    def run(self) -> None:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': self.cookie,
            'priority': 'u=0, i',
            'referer': 'https://admin.shopify.com/auth/callback?code=dFZEbXNKUHFudFl5VGxCSzdaaytMZTlGRDFweHAwQjlVemhWeG9PUnk3dDBPSmx3WTNrdzZISnRaSFBWeThLNWM5cktkbERUTEEvN3UrUGxVNDlRYldCUXV6czNIYmRSTkpyZXM2Z28yYWp1SnpUTjNDdGIwb2VtNFcxbWJWRnVmenlYMVo1NFJqajlWY0Z5RzhCem40VUtNSlRCMWdIZnNVWTdXdVpSaUxzL1ZlczBwT2xqSzR2dTBjZzg5QVFscVZJd05yWndSTmR3QjdXaEI3NDhsTGUrbXRTSzRMN3RyV1FtbmMwVnQxVWhsdkdsNUY4Ty93TXFWRGFGbHpqY0ZiTVJiMGY2amQ3a1VQT0RINHI5MUNHOTlaRjJ0amdLMjFtV01zakdKa2E5QmRlZHVreXNaRkFITDVjPS0tNWJXMnhkYlhXL0ZEU1NiNC0tM3pRWXVtdmVjRGEvRkhMNjZJVmNqZz09&state=8c27eecaf4ca5e7f28b2ec1672edec15&fwd=country%3DJP',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        }
        try:
            proxies = {
                'http': 'http://127.0.0.1:7897',
                'https': 'http://127.0.0.1:7897'
            }
            r = cffi_requests.get(self.url, headers=headers, proxies=proxies, impersonate='chrome101')
            json_data = r.json()
            orders = json_data['orders']
            # with sync_playwright() as playwright:
            #     browser = playwright.chromium.launch_persistent_context(
            #         # 指定本机用户缓存地址
            #         user_data_dir=r"C:\Users\Administrator\AppData\Local\google\Chrome\User Data",
            #         # 指定本机google客户端exe的路径
            #         channel='chrome',
            #         # # 要想通过这个下载文件这个必然要开  默认是False
            #         # accept_downloads=True,
            #         # 设置不是无头模式
            #         headless=False,
            #     )
            #     page = browser.new_page()
            #     page.goto(self.url)
            #     time.sleep(5)
            #     # print(page.query_selector('pre').inner_text())
            #     orders = json.loads(page.query_selector('pre').inner_text())['orders']
            #     browser.close()
            # with open('orders.json', 'r', encoding='utf-8') as f:
            #     orders = json.loads(f.read())['orders']
            for order in orders:
                order_id = order["name"]
                order_time = order["customer"]["updated_at"]
                order_time = self.translate_date(order_time.split('T')[0]) + ' at ' + \
                             self.translate_time(order_time.split('T')[1].split('-')[0])
                order_customer = order["billing_address"]["name"]
                order_channel = order["source_name"]
                if order_channel == 'web':
                    order_channel = 'Online Store'
                else:
                    order_channel = ''
                order_total = '$ ' + order["subtotal_price"]
                order_payment_status = order["financial_status"]
                order_fulfillment_status = order["fulfillment_status"]
                if not order_fulfillment_status:
                    order_fulfillment_status = 'Unfulfilled'
                else:
                    order_fulfillment_status = 'Fulfilled'
                order_items = str(len(order["line_items"])) + ' items'
                if order['shipping_lines']:
                    order_delivery_method = order["shipping_lines"][0]["code"]
                else:
                    order_delivery_method = ''
                order_tags = order["tags"]
                order_uuid = order['id']
                for item in order['line_items']:
                    if item['properties']:
                        if len(item['properties']) == 1:
                            order_ = (order_id, item['title'], item['variant_title'],
                                      item['quantity'], item['properties'][0]['value'], '')
                        else:
                            for i, p in enumerate(item['properties']):
                                if 'http' in str(p['value']):
                                    break
                            if i == len(item['properties']) - 1:
                                continue
                            else:
                                order_ = (order_id, item['title'], item['variant_title'],
                                          item['quantity'], item['properties'][i]['value'], item['properties'][i + 1]['value'])
                    else:
                        order_ = (order_id, item['title'], item['variant_title'],
                                  0, '', '')
                    self.orders['orders'].append(order_)

                # print([order_id, order_time, order_customer, order_channel, order_total,
                #        order_payment_status, order_fulfillment_status, order_items, order_delivery_method,
                #        order_tags])
                self.loading.emit([order_id, order_time, order_customer, order_channel, order_total,
                                   order_payment_status, order_fulfillment_status, order_items, order_delivery_method,
                                   order_tags, order_uuid])
            self.save_db_file(self.orders)
        except Exception as e:
            print(f'网络错误！{e}{order_id}')
            self.run()

    def translate_date(self, time_str):
        # 输入日期字符串
        input_date_str = time_str

        # 将输入日期字符串转换为datetime对象
        input_date = parse(input_date_str)

        # 计算输入日期的星期几
        weekday = input_date.strftime('%A')

        # 计算输入日期与当前日期的差距
        delta = datetime.date.today() - input_date.date()

        # 判断输入日期是否是yesterday、today或星期几，并打印输出
        if delta == datetime.timedelta(days=0):
            return 'today'
        elif delta == datetime.timedelta(days=1):
            return 'yesterday'
        else:
            return weekday

    def translate_time(self, time_str):
        # 输入时间字符串
        input_time_str = time_str

        # 将输入时间字符串转换为datetime对象
        input_time = datetime.datetime.strptime(input_time_str, '%H:%M:%S')

        # 将datetime对象格式化为输出格式
        output_time_str = input_time.strftime('%I:%M %p').lower()

        # 打印输出结果
        return output_time_str

    def save_db_file(self, data):
        # Connect to database
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        conn.execute('PRAGMA encoding = "UTF-8"')
        if not os.path.exists('orders.db'):
            c.executescript("""CREATE TABLE orders(
              'order_id' VARCHAR(45) NOT NULL,
              'title' VARCHAR(200) NULL,
              'variant_title' VARCHAR(45) NULL,
              'quantity' INT NULL,
              'carga_to_imagen' VARCHAR(200) NULL,
              'thumbnail' VARCHAR(200) NULL
              );""")
            conn.commit()
            c.close()

        # Create a cursor
        c = conn.cursor()
        # Execute an INSERT statement
        for d in data['orders']:
            c.execute("INSERT INTO orders (order_id, title, variant_title, quantity, carga_to_imagen, thumbnail)"
                      " VALUES (?, ?, ?, ?, ?, ?)", d)

        # Commit the transaction
        c.execute("delete from orders where orders.rowid not in (select MAX(orders.rowid) from orders group by "
                  "order_id, title, variant_title, carga_to_imagen);")
        conn.commit()

        # Close the connection
        conn.close()
