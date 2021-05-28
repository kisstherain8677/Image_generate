from birdDialog import BirdDialog
from flowerDialog import FlowerDialog
import os
import sys

class Generator(object):
    def __init__(self, genType,attrList):
        self.type = genType
        self.attrList=attrList

    # 生成图片
    def generate(self):
        # 用命令行执行GAN操作
        # 清空文件内容
        with open(r'custom.txt', 'a+') as test:
            test.truncate(0)
        if self.type == 'birds':

            dia = BirdDialog("birds",self.attrList)
            dia.exec()
            lines = []
            with open("custom.txt", "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                    lines.append(line)
            if len(lines) == 2:
                if lines[0] == self.type:
                    with open("StackGAN/data/birds/example_captions.txt", "w") as f:
                        f.write(lines[1])  # 覆盖原文件
                else:
                    print('unknown error!')
                    return
            else:
                print('you have not the caption!')
                return

        elif self.type == 'flowers':
            dia = BirdDialog("flowers",self.attrList)
            dia.exec()
            lines = []
            with open("custom.txt", "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                    lines.append(line)
            if len(lines) == 2:
                if lines[0] == self.type:
                    with open("StackGAN/data/flowers/example_captions.txt", "w") as f:
                        f.write(lines[1])  # 覆盖原文件
                else:
                    print('unknown error!')
                    return
            else:
                print('you have not input the caption!')
                return
        else:
            print("choose a type first!")
            return

        path = 'StackGAN/code'
        os.system('python ' + path + '/main.py --cfg ' + path + '/cfg/eval_' + self.type + '.yml --gpu 0')
