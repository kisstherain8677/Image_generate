import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,QDialog
from PyQt5.QtGui import QIcon


class ChoiceDiaStyle(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'choose a style'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.type = 'none'  # monet/..
        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.getChoice()

        #self.show()

    def getChoice(self):
        items = ("cezanne", "monet","ukiyoe","vangogh")
        item, okPressed = QInputDialog.getItem(self, "Get item", "object type:", items, 0, False)
        if okPressed and item:
            self.type=item
            print(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = generateDia()
    sys.exit(app.exec_())
