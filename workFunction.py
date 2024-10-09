import math
import os
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from PIL import ImageQt
from PyQt5.Qt import QLabel
from PyQt5.QtGui import QPixmap


class SimilarityImagesFinder:

    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.images_widgets = None

    def list_images(self, images_widgets):
        images = []
        self.images_widgets = images_widgets
        for widget in images_widgets:
            name = widget.objectName()
            label = widget.findChild(QLabel, name + '_label')
            pixmap = label.pixmap()
            image = self.get_image_metadata(pixmap)
            images.append(image)
        return images

    def resize_images(self, images):
        size = (256, 256)
        mode = "RGB"
        images_resized = []
        for image_path in images:
            image = Image.open(image_path).convert(mode)
            image_resized = image.resize(size)
            images_resized.append(image_resized)
        return images_resized

    def find_similar_images(self, images_resized):
        similar_images = {}
        for i in range(len(images_resized)):
            similar_images[i] = []
            for j in range(i + 1, len(images_resized)):
                diff = ImageChops.difference(images_resized[i], images_resized[j])
                diff_mean = sum([sum(pixel) for pixel in diff.getdata()]) / (256 * 256 * 3)
                if diff_mean < self.threshold:
                    similar_images[i].append(j)
        return similar_images

    def rename_similar_images_path(self, similar_images, images, signal):
        for i in range(len(similar_images)):
            if len(similar_images[i]) > 0:
                if os.path.exists(images[i]):
                    if '多打' not in images[i]:
                        os.rename(images[i], os.path.splitext(images[i])[0] + '-多打' + os.path.splitext(images[i])[1])
                        self.rename_widget_image(images, i)

                for j in similar_images[i]:
                    if os.path.exists(images[j]):
                        if '多打' not in images[j]:
                            os.rename(images[j], os.path.splitext(images[j])[0] + '-多打' + os.path.splitext(images[j])[1])
                            self.rename_widget_image(images, j)
        signal.emit(images[i - 1])

    def get_image_metadata(self, pixmap):
        # 获取当前显示图片的元数据信息
        qimage = pixmap.toImage()
        # 从 QPixmap 中检索图片路径元数据
        file_path = qimage.text("FilePath")
        return file_path

    def rename_widget_image(self, images, index):
        name = self.images_widgets[index].objectName()
        label = self.images_widgets[index].findChild(QLabel, name + '_label')
        pixmap = label.pixmap()
        qimage = pixmap.toImage()
        qimage.setText("FilePath", os.path.splitext(images[index])[0] + '-多打' + os.path.splitext(images[index])[1])
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap)


class ImageDealer:

    def __init__(self):
        self.bg_color = None
        self.img_path = None
        self.qimage = None
        self.border_color = None
        self.window = None

    # 更新传入参数
    def transfer(self, bg_color='black', img_path=None, qimage=None, border_color=(255, 255, 255, 0), window=None):
        self.bg_color = bg_color
        self.img_path = img_path
        self.border_color = border_color
        self.qimage = qimage
        self.window = window

    # 给原图添加纯色底
    def add_single_color_target(self):
        # 打开原图
        img = Image.open(self.img_path)
        width, height = img.size
        # 获取原图最大边长和最小边长
        max_side = max(width, height)
        min_side = min(width, height)
        # 创建纯色背景正方形图片
        # 如果原图是正方形或者是接近正方形
        if min_side / max_side > 0.8:
            side = int(math.sqrt(math.pow(width / 2, 2) + math.pow(height / 2, 2)) * 2)
            bg_size = (side, side)
            bg = Image.new('RGB', bg_size, self.bg_color)
            bg.paste(img, ((side - width) // 2, (side - height) // 2))
        else:
            bg = Image.new('RGB', (max_side, max_side), self.bg_color)
            bg.paste(img, ((max_side - width) // 2, (max_side - height) // 2))
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg'))
        max_side = max(bg.size)
        w = int(bg.width / (max_side / 140))
        h = int(bg.height / (max_side / 140))
        bg_new = bg.resize((w, h), Image.BICUBIC)
        qimage = ImageQt.ImageQt(bg_new)
        qimage.setText('FilePath', self.qimage.text('FilePath'))
        qimage.setText('Image', self.qimage.text('Image'))
        pixmap = QPixmap.fromImage(qimage)
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg')).setPixmap(pixmap)
        self.qimage = qimage
        bg.save(self.img_path)

    def img_2_circle(self):
        img = Image.open(self.img_path)
        width, height = img.size
        # 创建一个和原图一样大小的透明图片
        mask1 = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        mask2 = Image.new('RGBA', (width, height), self.border_color)
        # 使用ImageDraw模块画一个白色的圆形
        draw = ImageDraw.Draw(mask1)
        draw.ellipse((0, 0, width - 1, height - 1), fill=(0, 0, 0))
        # 使用Image.composite将原图和透明图片合成一张新图片，只保留圆形区域
        result = Image.composite(img, mask2, mask1)
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg'))
        max_side = max(result.size)
        w = int(result.width / (max_side / 140))
        h = int(result.height / (max_side / 140))
        bg_new = result.resize((w, h), Image.BICUBIC)
        qimage = ImageQt.ImageQt(bg_new)
        qimage.setText('FilePath', self.qimage.text('FilePath'))
        qimage.setText('Image', self.qimage.text('Image'))
        pixmap = QPixmap.fromImage(qimage)
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg')).setPixmap(pixmap)
        self.qimage = qimage
        os.remove(self.qimage.text('FilePath'))
        result.save(os.path.splitext(self.qimage.text('FilePath'))[0] + '.png')

    # 去除边缘纯色边框
    def crop_border_box(self):
        img = Image.open(self.img_path).convert('RGB')
        # 获取图片上非纯色部分的矩形边界
        bbox = img.getbbox()
        if bbox[2:] == img.size:
            # 反转颜色
            img = ImageChops.invert(img)
            bbox = img.getbbox()
        else:
            img = ImageChops.invert(img)
        # 根据边界裁剪图片
        result = img.crop(bbox)
        result = ImageChops.invert(result)
        result.save(self.img_path)

    # 去除图片噪点
    def filter_img(self):
        # 打开原图
        img = Image.open(self.img_path).convert('RGB')
        # 去除边缘噪点
        result = img.filter(ImageFilter.EDGE_ENHANCE)
        # 保存或显示处理后的图片
        result.save(self.img_path)

    # 添加特殊背景图片
    def add_special_background(self):
        # 打开背景图和要添加的图片
        background = Image.open("一百种图片.jpg")
        image = Image.open(self.img_path)
        image = image.resize((130, 130), Image.BICUBIC)

        # 获取背景图的尺寸
        bg_width, bg_height = background.size

        # 创建一个新的图像，将背景图作为底部
        result = Image.new('RGBA', (bg_width, bg_height), (255, 255, 255, 0))
        result.paste(background, (0, 0))

        # 计算要添加的图片的位置
        img_width, img_height = image.size
        x = bg_width - img_width - 80  # 10是一个偏移量，可以根据需要进行调整
        y = bg_height - img_height - 190

        # 将要添加的图片粘贴到背景图上
        result.paste(image, (x, y))
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg'))
        max_side = max(result.size)
        w = int(result.width / (max_side / 140))
        h = int(result.height / (max_side / 140))
        bg_new = result.resize((w, h), Image.BICUBIC)
        qimage = ImageQt.ImageQt(bg_new)
        qimage.setText('FilePath', self.qimage.text('FilePath'))
        qimage.setText('Image', self.qimage.text('Image'))
        pixmap = QPixmap.fromImage(qimage)
        self.window.findChild(QLabel, self.qimage.text('Image').strip('_qimg')).setPixmap(pixmap)
        self.qimage = qimage

        # 保存结果图像
        result.save(self.img_path)