import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,QDialog
from PyQt5.QtGui import QIcon


class ChoiceDiaGen(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'generate picture'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.type = 'none'  # bird/flower/..
        self.attrList=[]
        self.initUI()



    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.getChoice()
        self.getAttr()

        #self.show()

    def getChoice(self):
        items = ("birds", "flowers")
        item, okPressed = QInputDialog.getItem(self, "choose type", "object type:", items, 0, False)
        if okPressed and item:
            self.type=item
            print(item)

    def getAttr(self):
        attrs, ok = QInputDialog.getText(self, "指定属性", "指定3-5个属性,用逗号分隔:",
                                        QLineEdit.Normal,"")
        if ok and (len(attrs) != 0):
            self.attrList=attrs.split(',')
            print(self.attrList)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = generateDia()
    sys.exit(app.exec_())
