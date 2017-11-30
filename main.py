from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import \
    QHBoxLayout, \
    QLabel, \
    QWidget, \
    QApplication, \
    QFileDialog, \
    QMessageBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import sys


class ClickableLabel(QLabel):
    def __init__(self):
        super().__init__()

    def mouseReleaseEvent(self, QMouseEvent):
        QMessageBox.question(self, 'Message',
                             'PyQt5 message',
                             QMessageBox.Yes,
                             QMessageBox.No)
        return QMouseEvent.pos()


class PicWindow(QWidget):
    def __init__(self):
        super().__init__()

        image_path = self.getfilename()
        image = Image.open(image_path)
        img_tmp = ImageQt(image.convert('RGBA'))
        pixmap = QPixmap.fromImage(img_tmp)

        lbl = ClickableLabel()
        lbl.setPixmap(pixmap)

        hbox = QHBoxLayout(self)
        hbox.addWidget(lbl)
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

    def pixelize(self):
        reply = QMessageBox.question(self, 'Message',
                                     'PyQt5 message',
                                     QtGui.QMessageBox.Yes,
                                     QtGui.QMessageBox.No)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    newform = PicWindow()
    sys.exit(app.exec_())
