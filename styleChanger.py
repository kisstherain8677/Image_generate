import os
import sys
import shutil


class StyleChanger(object):

    # source_path为用户输入的原始图片地址
    def __init__(self, style, source_path):
        self.style = style
        self.source_path = source_path

    def changeStyle(self):
        if self.style is "" or self.style is None or self.source_path is None:
            print("load a source picture and choose a style first!")
            return

        target_dir = 'CycleGAN/sourceImg'
        # 因为只处理一张,先清空文件夹
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        shutil.rmtree(target_dir)
        os.mkdir(target_dir)
        # 将原始图片移动到CycleGAN项目中
        try:
            shutil.copy(self.source_path,target_dir)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:",sys.exc_info())

        # generate picture of other style
        path = "CycleGAN/"
        os.system('python ' + path + 'test.py --dataroot ' + target_dir +
                  ' --name ' + 'style_' + self.style + '_pretrained' + ' --model test --no_dropout')
