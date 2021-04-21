import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon


class GenerateDia(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'generate picture'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

        self.type = 'none'  # bird/flower/actor
        self.dis='none' # 文本描述

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.getChoice()
        self.getText()
        self.writeInf()

        #self.show()

    def getChoice(self):
        items = ("bird", "flower", "actor")
        item, okPressed = QInputDialog.getItem(self, "Get item", "object type:", items, 0, False)
        if okPressed and item:
            self.type=item
            print(item)

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text", "input discription:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.dis=text
            print(text)

    def writeInf(self):
        with open("custom.txt", "w") as f:
            f.write(self.type+'\n'+self.dis)  # 自带文件关闭功能，不需要再写f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = generateDia()
    sys.exit(app.exec_())
