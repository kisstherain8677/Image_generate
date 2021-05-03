# -*- coding:utf-8 -*-
'''
inputDialog
'''
__author__ = 'Tony Zhu'

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QInputDialog, \
    QGridLayout, QLabel, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QDialog


class FlowerDialog(QDialog):
    def __init__(self):
        super(FlowerDialog, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("输入花朵信息")
        self.setGeometry(400, 400, 300, 260)

        example_sentence = "请输入描述的句子，描述花朵的花瓣颜色、形状大小、花蕊颜色等，可参考以下示例：\n" + \
                           "this flower has large rounded pink petals with a yellow center."
        label0 = QLabel(example_sentence)
        label1 = QLabel("花瓣颜色:")
        label2 = QLabel("花瓣大小:")
        label3 = QLabel("花蕊颜色:")
        # label4 = QLabel("翅膀颜色:")
        # label5 = QLabel("喙长度:")
        label6 = QLabel("编辑描述句子")

        self.petalColorLabel = QLabel("red")
        self.petalColorLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.petalSizeLabel = QLabel("small")
        self.petalSizeLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.centerColorLabel = QLabel("white")
        self.centerColorLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.wingsColorLabel = QLabel("yellow")
        # self.wingsColorLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.beakSizeLabel = QLabel("short")
        # self.beakSizeLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.captionLabel = QLabel("This flower has overlapping pink pointed petals "
                                   "surrounding a ring of short yellow filaments")
        self.captionLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # buttons
        petalColorButton = QPushButton("edit")
        petalSizeButton = QPushButton("edit")
        centerColorButton = QPushButton("edit")
        # wingsColorButton = QPushButton("edit")
        # beakSizeButton = QPushButton("edit")
        showDisButton = QPushButton("edit")
        checkButton = QPushButton("save caption")
        cancelButton = QPushButton("generate image")
        generateCaptionButton = QPushButton("generate caption")

        # button click
        petalColorButton.clicked.connect(lambda: self.editOne(self.petalColorLabel))
        petalSizeButton.clicked.connect(lambda: self.editOne(self.petalSizeLabel))
        centerColorButton.clicked.connect(lambda: self.editOne(self.centerColorLabel))
        # wingsColorButton.clicked.connect(lambda: self.editOne(self.wingsColorLabel))
        # beakSizeButton.clicked.connect(lambda: self.editOne(self.beakSizeLabel))
        showDisButton.clicked.connect(lambda: self.editCaption(self.captionLabel))
        checkButton.clicked.connect(self.submitCaption)
        cancelButton.clicked.connect(self.close)
        generateCaptionButton.clicked.connect(self.generateCaption)

        # layout
        mainLayout = QVBoxLayout()

        gridLayout = QGridLayout()
        gridLayout.addWidget(label1, 0, 0)
        gridLayout.addWidget(self.petalColorLabel, 0, 1)
        gridLayout.addWidget(petalColorButton, 0, 2)
        gridLayout.addWidget(label2, 1, 0)
        gridLayout.addWidget(self.petalSizeLabel, 1, 1)
        gridLayout.addWidget(petalSizeButton, 1, 2)
        gridLayout.addWidget(label3, 2, 0)
        gridLayout.addWidget(self.centerColorLabel, 2, 1)
        gridLayout.addWidget(centerColorButton, 2, 2)
        # gridLayout.addWidget(label4, 3, 0)
        # gridLayout.addWidget(self.wingsColorLabel, 3, 1)
        # gridLayout.addWidget(wingsColorButton, 3, 2)
        #
        # gridLayout.addWidget(label5, 4, 0)
        # gridLayout.addWidget(self.beakSizeLabel, 4, 1)
        # gridLayout.addWidget(beakSizeButton, 4, 2)

        gridLayout2 = QGridLayout()
        gridLayout2.addWidget(label6, 0, 0)
        gridLayout2.addWidget(self.captionLabel, 0, 1)
        gridLayout2.addWidget(showDisButton, 0, 2)

        genCaptionLayout = QHBoxLayout()
        genCaptionLayout.addStretch(1)
        genCaptionLayout.addWidget(generateCaptionButton)
        genCaptionLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(checkButton)
        bottomLayout.addWidget(cancelButton)

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
        petalColor = self.petalColorLabel.text()
        petalSize = self.petalSizeLabel.text()
        centerColor = self.centerColorLabel.text()
        # wingsColor = self.wingsColorLabel.text()
        # beakSize = self.beakSizeLabel.text()
        attributeList = ['petalColor', 'petalSize', 'centerColor']
        valueList = [petalColor, petalSize, centerColor]
        attDict = dict(zip(attributeList, valueList))
        caption="this flower has %s %s petals and a %s center" % (petalSize,petalColor,centerColor)
        # keyindex = 0
        # for key in iter(attDict.keys()):
        #     if (attDict[key] != ''):
        #         cap = " %s %s," % (attDict[key], key)
        #         caption = caption + cap

        self.captionLabel.setText(caption)

    # 写入生成的句子,并生成图片
    def submitCaption(self):
        caption = self.captionLabel.text()
        with open("custom.txt", "w") as f:
            f.write("flowers" + '\n' + caption)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myshow = InputDialog()
    myshow.show()
    sys.exit(app.exec_())
