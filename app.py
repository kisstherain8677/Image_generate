import os
import sys
from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from toolBar import ToolBar
from Canvas.canvas import Canvas

import cv2

from grab_cut import Grab_cut
from choiceDia import ChoiceDia
from zoomWidget import ZoomWidget
from birdDialog import BirdDialog

from generator import Generator

__appname__ = 'grab_cut'


class ResizesQWidget(QWidget):
    def sizeHint(self):
        return QSize(100, 150)


class struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# 菜单栏和工具栏
class WindowMixin(object):

    # 根据名字和action列表创建一个菜单，比如File,[new,edit]
    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu

    def toolbar(self, title, actions=None):
        toolbar = ToolBar(title)
        toolbar.setObjectName('{}ToolBar'.format(title))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        if actions:
            addActions(toolbar, actions)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)  # 加到布局左侧
        return toolbar


# 创建一个新Action
def newAction(parent, text, slot=None, shortcut=None,
              tip=None, icon=None, checkable=False,
              enable=True):
    a = QAction(text, parent)
    if icon is not None:
        a.setIcon(QIcon(icon))
    if shortcut is not None:
        a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setChecked(True)
    a.setEnabled(enable)
    return a


# 讲actions加入到父控件
def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        widget.addAction(action)  # weidget is toolBar or menu


# 主界面
class MainWindow(QMainWindow, WindowMixin):
    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = list(range(3))

    def __init__(self, defaultFilename=None):
        super().__init__()

        self.dirty = True  # 文件是否已保存
        self.mImgList = []  # 图片列表
        self.dirname = None  # 文件名
        self._beginner = True  #

        self.image_out_np = None  # 提取结果
        self.default_save_dir = None  # 默认保存路径
        self.filePath = None  # 当前载入的图片路径
        self.mattingFile = None

        # 垂直布局，
        listLayout = QVBoxLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)

        # ---#显示图片的label pic
        matResultShow = ResizesQWidget()  # 返回是是Qwidget
        matResultShow.resize(150, 150)

        self.pic = QLabel(matResultShow)
        self.pic.resize(150, 150)
        self.setGeometry(50, 20, 150, 150)

        matResultShow.setLayout(listLayout)

        # 建一个dockwidget放图片label
        self.resultdock = QDockWidget('分割结果', self)
        self.resultdock.setObjectName('result')

        self.resultdock.setWidget(matResultShow)
        self.resultdock.resize(150, 150)
        # self.resultdock.setFeatures(QDockWidget.DockWidgetFloatable)

        # 建一个fileDoc放文件
        self.fileListWidget = QListWidget()  # 列表布局
        self.fileListWidget.itemDoubleClicked.connect(
            self.fileItemDoubleClicked)
        fileListLayout = QVBoxLayout()
        fileListLayout.setContentsMargins(0, 0, 0, 0)
        fileListLayout.addWidget(self.fileListWidget)
        fileListContainer = QWidget()
        fileListContainer.setLayout(fileListLayout)
        self.filedock = QDockWidget('导入文件列表', self)
        self.filedock.setObjectName('Files')
        self.filedock.setWidget(fileListContainer)

        self.zoomWidget = ZoomWidget()

        self.canvas = Canvas(parent=self)
        scroll = QScrollArea()
        scroll.setWidget(self.canvas)
        scroll.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: scroll.verticalScrollBar(),
            Qt.Horizontal: scroll.horizontalScrollBar()
        }
        self.scrollArea = scroll
        self.canvas.scrollRequest.connect(self.scrollRequest)

        self.setCentralWidget(scroll)
        self.addDockWidget(Qt.RightDockWidgetArea, self.resultdock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
        # self.filedock.setFeatures(QDockWidget.DockWidgetFloatable)

        self.dockFeatures = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable
        self.resultdock.setFeatures(
            self.resultdock.features() ^ self.dockFeatures)

        # Actions
        action = partial(newAction, self)

        open_file = action('导入图片', self.openFile, 'Ctrl+O', '导入图片')
        open_dir = action('导入文件夹', self.openDir,
                          'Ctrl+D', '导入文件夹中的所有图片到列表')
        change_save_dir = action('&更改预设的保存路径', self.changeSavedirDialog)
        # open_next_img = action('&Next Image', self.openNextImg,
        #                        'Ctrl+N', 'Open next image')
        # open_pre_img = action('&Previous Image', self.openPreImg,
        #                        'Ctrl+M', 'Open previous image')
        save = action('保存', self.saveFile, 'Crl+S', '保存输出结果图')
        create = action('指定区域', self.createShape,
                        'w', '框选ROI')
        mark = action('标记微调', self.markDown, None, '左键白色，标记前景；右键黑色，标记后景')
        matting = action('迭代一次', self.grabcutMatting,
                         'e', '用当前标记迭代一次获取前景算法')

        # 用预训练网络生成图片
        generate = action('生成图片', self.generate, None, '输入文字，生成图片素材')
        # 字典，对应一个放缩比
        self.scalers = {
            self.FIT_WINDOW: self.scaleFitWindow,
            self.FIT_WIDTH: self.scaleFitWidth,
            # Set to one to scale to 100% when loading files.
            self.MANUAL_ZOOM: lambda: 1,
        }

        # store actions for further handling
        self.actions = struct(save=save, open_file=open_file,
                              open_dir=open_dir, change_save_dir=change_save_dir,
                              # open_next_img=open_next_img, open_pre_img=open_pre_img,
                              create=create, mark=mark, matting=matting, generate=generate)

        # Auto saving: enable auto saving if pressing next
        # self.autoSaving = QAction('Auto Saving', self)
        # self.autoSaving.setCheckable(True)
        # self.autoSaving.setChecked()

        # set toolbar
        self.tools = self.toolbar('Tools')
        self.actions.all = (save, open_file, open_dir,
                            change_save_dir, create,
                            # open_pre_img, open_next_img,
                            mark, matting, generate)
        addActions(self.tools, self.actions.all)

        # set status
        self.statusBar().showMessage('{} 已就绪.'.format(__appname__))

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self, "Attention",
                                         "you have unsaved changes, proceed anyway?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave
        return True

    def resetState(self):
        self.canvas.resetState()

    def errorMessage(self, title, message):
        return QMessageBox.critical(self, title,
                                    '<p><b>%s</b></p>%s' % (title, message))

    def beginner(self):
        return self._beginner

    def advanced(self):
        return not self.beginner()

    def openFile(self, _value=False):
        path = os.path.dirname(self.filePath) if self.filePath else '.'
        formats = ['*.%s' % fmt.data().decode("ascii").lower()
                   for fmt in QImageReader.supportedImageFormats()]
        filters = "Image (%s)" % ' '.join(formats)
        filename = QFileDialog.getOpenFileName(
            self, '%s - Choose Image or Label file' % __appname__, path, filters)
        if filename:
            if isinstance(filename, (tuple, list)):
                filename = filename[0]
            self.loadFile(filename)

    def openDir(self, dirpath=None):
        defaultOpenDirPath = dirpath if dirpath else '.'
        targetDirPath = QFileDialog.getExistingDirectory(self,
                                                         '%s - Open Directory' % __appname__, defaultOpenDirPath,
                                                         QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.importDirImages(targetDirPath)

    # 将导入图片显示在列表栏
    def importDirImages(self, dirpath):
        self.fileListWidget.clear()
        self.mImgList = self.scanAllImages(dirpath)
        # self.openNextImg()
        for imgPath in self.mImgList:
            item = QListWidgetItem(imgPath)
            self.fileListWidget.addItem(item)

    # 扫描路径下的所有文件，返回图片列表
    def scanAllImages(self, folderPath):
        extensions = ['.%s' % fmt.data().decode("ascii").lower()
                      for fmt in QImageReader.supportedImageFormats()]
        imageList = []

        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    path = os.path.abspath(relativePath)
                    imageList.append(path)
        imageList.sort(key=lambda x: x.lower())
        return imageList

    def fileItemDoubleClicked(self, item=None):
        currIndex = self.mImgList.index(item.text())  # 获取图片列表的index
        if currIndex < len(self.mImgList):
            filename = self.mImgList[currIndex]
            if filename:
                self.loadFile(filename)  # 载入图片列表

    # 读取图片到canvas
    def loadFile(self, filePath=None):
        self.resetState()  # 清理canvas
        self.canvas.setEnabled(False)

        # 高亮选中项
        if filePath and self.fileListWidget.count() > 0:
            index = self.mImgList.index(filePath)
            fileWidgetItem = self.fileListWidget.item(index)
            fileWidgetItem.setSelected(True)

        if filePath and os.path.exists(filePath):
            # load image
            self.ImageData = read(filePath, None)
        else:
            return

        image = QImage.fromData(self.ImageData)
        # 内存中没有图片
        if image.isNull():
            self.errorMessage(u'Error opening file',
                              u'<p>Make sure <i>%s</i> is a valid image file.' % filePath)
            self.status('Error reading %s' % filePath)
            return False
        self.status('Loaded %s' % os.path.basename(filePath))
        self.image = image  # Qimage格式
        self.filePath = filePath  # 当前载入的文件路径
        self.canvas.loadPixmap(QPixmap.fromImage(image))  # canvas中放置图片
        self.canvas.setEnabled(True)
        self.adjustScale(initial=True)
        self.paintCanvas()

    # 显示当前状态
    def status(self, message, delay=5000):
        self.statusBar().showMessage(message, delay)

    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        self.zoomWidget.setValue(int(100 * value))

    def scaleFitWindow(self):
        """Figure out the size of the pixmap in order to fit the main widget."""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.centralWidget().width() - e
        h1 = self.centralWidget().height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def scaleFitWidth(self):
        # The epsilon does not seem to work too well here.
        w = self.centralWidget().width() - 2.0
        return w / self.canvas.pixmap.width()

    def paintCanvas(self):
        assert not self.image.isNull(), "cannot paint null image"
        self.canvas.scale = 0.01 * self.zoomWidget.value()
        self.canvas.adjustSize()
        self.canvas.update()

    def createShape(self):
        assert self.beginner()
        self.canvas.setEditing(False)
        self.actions.create.setEnabled(False)

    # 开始标记,mod换成editting
    def markDown(self):
        self.canvas.setEditing(True)

    def toggleDrawMode(self, edit=True):
        self.canvas.setEditing(edit)
        self.actions.createMode.setEnabled(edit)
        self.actions.editMode.setEnabled(not edit)

    # 生成图片
    def generate(self):
        choiceDia=ChoiceDia()
        choiceDia.show()
        choiceDia.hide()
        gen=Generator(choiceDia.type)
        gen.generate()


    # 提取前景操作
    def grabcutMatting(self):

        if self.mattingFile is None:
            self.mattingFile = Grab_cut()

        def format_shape(s):
            return dict(line_color=s.line_color.getRgb(),
                        fill_color=s.fill_color.getRgb(),
                        points=[(p.x(), p.y()) for p in s.points],
                        backMark=self.canvas.getBackMark(),
                        whiteMark=self.canvas.getForMark())

        # 有四个点（矩形的话）+填充线颜色和边缘线颜色
        shape = format_shape(self.canvas.shapes[-1])
        self.image_out_np = self.mattingFile.image_matting(self.filePath,
                                                           shape, iteration=10)
        self.showResultImg(self.image_out_np)
        self.actions.save.setEnabled(True)

    # 接收opencv矩阵格式
    def showResultImg(self, image_np):
        # resize to pic
        # factor = min(self.pic.width() /
        #              image_np.shape[1], self.pic.height() / image_np.shape[0])
        # image_np = cv2.resize(image_np, None, fx=factor,
        #                       fy=factor, interpolation=cv2.INTER_AREA)
        # image_np = cv2.resize((self.pic.height(), self.pic.width()))
        image = QImage(image_np, image_np.shape[1],
                       image_np.shape[0], QImage.Format_ARGB32)
        matImg = QPixmap(image)
        self.pic.setFixedSize(matImg.size())
        self.pic.setPixmap(matImg)

    def saveFile(self):
        self._saveFile(self.saveFileDialog())

    def _saveFile(self, saved_path):
        print(saved_path)
        if saved_path:
            Grab_cut.resultSave(saved_path, self.image_out_np)
            self.setClean()
            self.statusBar().showMessage('Saved to  %s' % saved_path)
            self.statusBar().show()

    def saveFileDialog(self):
        caption = '%s - Choose File' % __appname__
        filters = 'File (*%s)' % 'png'
        if self.default_save_dir is not None and len(self.default_save_dir):
            openDialogPath = self.default_save_dir
        else:
            openDialogPath = self.currentPath()

        print(openDialogPath)
        dlg = QFileDialog(self, caption, openDialogPath, filters)
        dlg.setDefaultSuffix('png')
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        filenameWithoutExtension = os.path.splitext(self.filePath)[0]
        dlg.selectFile(filenameWithoutExtension)
        dlg.setOption(QFileDialog.DontUseNativeDialog, False)
        if dlg.exec_():
            return dlg.selectedFiles()[0]
        return ''

    def currentPath(self):
        return os.path.dirname(self.filePath) if self.filePath else '.'

    def changeSavedirDialog(self, _value=False):
        if self.default_save_dir is not None:
            path = self.default_save_dir
        else:
            path = '.'

        dirpath = QFileDialog.getExistingDirectory(self,
                                                   '%s - Save annotations to the directory' % __appname__, path,
                                                   QFileDialog.ShowDirsOnly
                                                   | QFileDialog.DontResolveSymlinks)

        if dirpath is not None and len(dirpath) > 1:
            self.default_save_dir = dirpath

        self.statusBar().showMessage('%s . Annotation will be saved to %s' %
                                     ('Change saved folder', self.default_save_dir))
        self.statusBar().show()

    def setClean(self):
        self.dirty = False
        self.actions.save.setEnabled(False)

        self.actions.create.setEnabled(True)

    def openNextImg(self):
        pass

    def openPreImg(self):
        pass

    def scrollRequest(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)


# 读取二进制图片 返回
def read(filename, default=None):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except Exception:
        return default

    def resetState(self):
        self.canvas.resetState()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()

    sys.exit(app.exec_())
