from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QLabel, \
    QWidget, \
    QApplication, \
    QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import sys


class ClickableLabel(QLabel):
    def __init__(self, callable):
        super().__init__()
        self.callable = callable

    def mouseReleaseEvent(self, QMouseEvent):
        self.callable(QMouseEvent.x(), QMouseEvent.y())


class PicWindow(QWidget):
    def __init__(self):
        super().__init__()

        image_path = self.getfilename()
        self.image = Image.open(image_path)
        self.lbl = ClickableLabel(self.clicked)
        self.show_image()

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.lbl)
        self.setLayout(hbox)

        self.move(100, 100)
        self.setWindowTitle('Pict-Qt')
        self.show()

    def getfilename(self):
        filename, _filter = QFileDialog.getOpenFileName \
            (parent=self,
             caption='Choose an image',
             filter='Image files (*.jpg)')
        return filename

    def clicked(self, x, y):
        click_x = x
        click_y = y

        max_x = self.image.width
        max_y = self.image.height

        side = 10
        averaging_side = 10

        for bi in range(-side, side + 1):
            for bj in range(-side, side + 1):
                mixel_center_x = click_x + bi * averaging_side
                mixel_center_y = click_y + bj * averaging_side
                if mixel_center_x + averaging_side > max_x or \
                                        mixel_center_x - averaging_side < 0 or \
                                        mixel_center_y + averaging_side > max_y or \
                                        mixel_center_y - averaging_side < 0:
                    continue

                mixel_width = range(mixel_center_x - averaging_side,
                                    mixel_center_x + averaging_side)
                mixel_height = range(mixel_center_y - averaging_side,
                                     mixel_center_y + averaging_side)
                area = len(mixel_width) * len(mixel_height)

                r = 0
                g = 0
                b = 0
                pix = self.image.load()
                for i in mixel_width:
                    for j in mixel_height:
                        r = r + pix[i, j][0]
                        g = g + pix[i, j][1]
                        b = b + pix[i, j][2]
                new_r = r // area
                new_g = g // area
                new_b = b // area

                draw = ImageDraw.Draw(self.image)
                for i in mixel_width:
                    for j in mixel_height:
                        draw.point((i, j), (new_r, new_g, new_b))

        self.show_image()

    def show_image(self):
        img_tmp = ImageQt(self.image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)
        self.lbl.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    newform = PicWindow()
    sys.exit(app.exec_())
