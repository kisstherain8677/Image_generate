# -*- coding:utf-8 -*-
'''
inputDialog
'''
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, \
    QGridLayout, QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QDialog


class BirdDialog(QDialog):
    def __init__(self, type, attrList):
        super(BirdDialog, self).__init__()
        self.attrList = attrList
        self.type = type
        self.initUi()

    # attrList:string[] about attr
    def initUi(self):
        self.setWindowTitle("输入生成图像的信息")
        self.setGeometry(400, 400, 300, 260)

        example_sentence = "请输入描述的句子，描述花、鸟的相关属性，可参考以下示例：\n" + \
                           "this bird is red with white and has a very short beak\n" + \
                           "the bird has a yellow crown and a black eyering that is round"
        self.labelEx = QLabel(example_sentence)
        self.labelEdit = QLabel("编辑描述句子")

        self.attrLabelList = []  # 存放属性名称
        for attr in self.attrList:
            label = QLabel(attr)
            self.attrLabelList.append(label)

        self.valueLabelList = []  # 存放属性值
        for index in range(0, len(self.attrList)):
            label = QLabel("input value of " + self.attrList[index])
            label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.valueLabelList.append(label)

        self.captionLabel = QLabel("this bird is red with white and has a very short beak")
        self.captionLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.buttonList = []  # 存放按钮
        for index in range(0, len(self.attrList)):
            button = QPushButton("edit " + self.attrList[index] + "'s value")
            self.buttonList.append(button)

        # connect
        for index in range(0, len(self.attrList)):
            self.buttonList[index].clicked.connect(partial(self.editOne, self.valueLabelList[index]))

        self.showDisButton = QPushButton("edit")
        self.checkButton = QPushButton("save caption")
        self.cancelButton = QPushButton("generate image")
        self.generateCaptionButton = QPushButton("generate caption")

        self.showDisButton.clicked.connect(lambda: self.editCaption(self.captionLabel))
        self.checkButton.clicked.connect(self.submitCaption)
        self.cancelButton.clicked.connect(self.close)
        self.generateCaptionButton.clicked.connect(self.generateCaption)

        # layout
        mainLayout = QVBoxLayout()

        gridLayout = QGridLayout()

        for i in range(0, len(self.attrList)):
            gridLayout.addWidget(self.attrLabelList[i], i, 0)
            gridLayout.addWidget(self.valueLabelList[i], i, 1)
            gridLayout.addWidget(self.buttonList[i], i, 2)

        gridLayout2 = QGridLayout()
        gridLayout2.addWidget(self.labelEdit, 0, 0)
        gridLayout2.addWidget(self.captionLabel, 0, 1)
        gridLayout2.addWidget(self.showDisButton, 0, 2)

        genCaptionLayout = QHBoxLayout()
        genCaptionLayout.addStretch(1)
        genCaptionLayout.addWidget(self.generateCaptionButton)
        genCaptionLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.checkButton)
        bottomLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(gridLayout)
        mainLayout.addStretch(1)
        mainLayout.addLayout(genCaptionLayout)
        mainLayout.addStretch(1)
        mainLayout.addLayout(gridLayout2)
        mainLayout.addStretch(1)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)

    def editOne(self, label):
        name, ok = QInputDialog.getText(self, "属性输入", "输入该属性描述:",
                                        QLineEdit.Normal, label.text())
        if ok:
            label.setText(name)

    def editCaption(self, label):
        name, ok = QInputDialog.getText(self, "修改句子", "修改该句子:",
                                        QLineEdit.Normal, label.text())
        if ok and (len(name) != 0):
            label.setText(name)

    # 根据属性生成caption
    def generateCaption(self):
        # 获取各个属性
        valueList = []
        for label in self.valueLabelList:
            valueList.append(label.text())
        attDict = dict(zip(self.attrList, valueList))
        caption = ""
        if self.type == "birds":
            caption = "this bird has"
        elif self.type == "flowers":
            caption = "this flower has"
        else:
            print("unknown type")
            return

        keyindex = 0
        for key in iter(attDict.keys()):
            if (attDict[key] != ''):
                cap = " %s %s," % (attDict[key], key)
                caption = caption + cap

        self.captionLabel.setText(caption)

    # 写入生成的句子,并生成图片
    def submitCaption(self):
        caption = self.captionLabel.text()
        with open("custom.txt", "w") as f:
            f.write(self.type + '\n' + caption)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    attrList = ["body", "beak", "wings"]
    myshow = BirdDialog(attrList)
    myshow.show()
    sys.exit(app.exec_())
