#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#--------------------LICENSE STUFF
#
from PyQt4 import QtGui, QtCore
from PIL import Image, ImageDraw, ImageFont, ImageQt, ImageStat
from math import floor, ceil
import sys
import re
from os import path

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

LABEL_DX = "src/slide_1200x824.png"
LABEL_3 = "src/slide_800x600.png"
LABEL_PAPER_1 = "src/click_1024x758.png"
LABEL_1024 = "src/click_1024x768.png"
LABEL_800 = "src/click_800x600.png"
SAVE_PATH = "output/"
FONT = "src/Caecilia Regular.ttf"
FONT_SIZE = 40
ICON = "src/Kindle.png"
IMAGE_FORMATS = ['bmp', 'dcx', 'eps', 'ps', 'gif', 'im', 'jpg', 'jpeg',
                 'jpe', 'pcd', 'pcx', 'pdf', 'png', 'pbm', 'pgm', 'ppm',
                 'psd', 'tif', 'tiff', 'xmb', 'xpm']

KINDLE_VERSIONS = ("Kindle DX (1200 x 824)",
                   "Kindle 3 (800 x 600)",
                   "Kindle 4, 5, Touch (800 x 600)",
                   "Kindle Paperwhite 1 (1024 x 758)",
                   "Kindle Paperwhite 2 (1024 x 768)")

#EXPERIMENTAL FEATURES
#Selector and SpecialLabel
'''
class Selector (QtGui.QRubberBand):
    
    def __init__(self, *arg, **kwargs):
        super(Selector, self).__init__(*arg, **kwargs)
        
    def paintEvent(self, event):
        
        #set pen
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 4))
        
        #set brush
        color = QtGui.QColor(QtCore.Qt.blue)
        painter.setBrush(QtGui.QBrush(color))
        painter.setOpacity(0.3)
        #painter.fillRect(event.rect(), QtGui.QBrush(color))
        
        #draw rect
        painter.drawRect(event.rect())
        
class SpecialLabel(QtGui.QLabel):
    
    def __init__(self, parent):
        super(SpecialLabel, self).__init__()
        #QtGui.QLabel.__init__(self, parent)
        self.rubberBand = Selector(Selector.Rectangle, self)
        self.origin = QtCore.QPoint()
        self.im_width = 0
        self.im_height = 0
        
    def mousePressEvent(self, event):
        self.origin = QtCore.QPoint(event.pos())
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberBand.show()
        
    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        
        min_x = self.origin.x()+20
        min_y = self.origin.y()+20
        
        if x > self.width() : x = self.width() -1
        if y > self.height() : y = self.height() -1
        print(self.width(), self.height())
        if x < min_x : x = min_x
        if y < min_y : y = min_y
        #print(x,y)
        pos = QtCore.QPoint(x,y)
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, pos).normalized())
'''

class CropDialog(QtGui.QDialog):
    
    def __init__(self, image_path, language, version=0):
        super(CropDialog, self).__init__()
        
        self.language = language
        self.version = version
        self.initUi()
        self.im_path = image_path
        self.initVariables()
        self.translateUI()
        self.openImage()
        self.initActions()
        self.checkActive()
            
    def changeSize(self):
        self.setFixedWidth(self.sizeHint().width())
        self.setFixedHeight(self.sizeHint().height())
        self.centerUI()
        
    def initVariables(self):
        
        self.delta_left = None
        self.delta_right = None
        self.screen_coeff = 2
                
    def initUi(self):
        
        self.main_layout = QtGui.QVBoxLayout(self)
        self.button_hor_layout = QtGui.QHBoxLayout()
        self.choose_label = QtGui.QLabel(self)
        self.choose_label.setObjectName("choose_label")
        
        self.choose_ver_layout = QtGui.QVBoxLayout()
        self.choose_ver_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.choose_ver_layout.addWidget(self.choose_label)
        
        self.button_hor_layout.addLayout(self.choose_ver_layout)
        
        self.version_ver_layout = QtGui.QVBoxLayout()
        self.version_check = QtGui.QCheckBox(self)
        self.version_combo = QtGui.QComboBox(self)
        self.version_combo.setObjectName("version_combo")
        for _ in KINDLE_VERSIONS:
            self.version_combo.addItem("")
        self.version_ver_layout.addWidget(self.version_check)
        self.version_ver_layout.addWidget(self.version_combo)
        self.button_hor_layout.addLayout(self.version_ver_layout)
        
        self.OkCropVerLayout = QtGui.QVBoxLayout()
        self.push_crop = QtGui.QPushButton(self)
        
        self.push_crop.setObjectName("push_crop")
        self.push_ok = QtGui.QPushButton(self)
        self.push_ok.setObjectName("push_ok")
        self.push_ok.setEnabled(False)
        self.OkCropVerLayout.addWidget(self.push_crop)
        self.OkCropVerLayout.addWidget(self.push_ok)
        
        self.button_hor_layout.addLayout(self.OkCropVerLayout)
        self.main_layout.addLayout(self.button_hor_layout)
        self.ImHorLayout = QtGui.QHBoxLayout()
        self.ImHorLayout.setObjectName(_fromUtf8("ImHorLayout"))
        self.push_left = QtGui.QPushButton(self)
        
        self.push_left.setObjectName("push_left")
        self.ImHorLayout.addWidget(self.push_left)
        self.label_image = QtGui.QLabel(self)
        #self.label_image = SpecialLabel(self)    #EXPERIMENTAL
        self.label_image.setStyleSheet(_fromUtf8("border-width: 1px;\n"
                                                 "border-style: solid"))
        self.label_image.setObjectName("label_image")
        self.ImHorLayout.addWidget(self.label_image)
        self.push_right = QtGui.QPushButton(self)
        self.push_right.setObjectName("push_right")
        self.ImHorLayout.addWidget(self.push_right)
        self.main_layout.addLayout(self.ImHorLayout)

        self.retranslateUI()
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)
    
    
    def setSizeUI(self):
        
        h = 25
        lab_w = self.fontMetrics().boundingRect(self.choose_label.text()).width() + 7
        self.choose_label.setFixedSize(QtCore.QSize(lab_w, h))
        
        combo_w = self.fontMetrics().boundingRect(self.version_combo.itemText(4)).width() + 7
        self.version_combo.setFixedSize(QtCore.QSize(combo_w, h))
        
        self.push_crop.setFixedSize(QtCore.QSize(100, h))
        self.push_ok.setFixedSize(QtCore.QSize(100, h))
        self.push_left.setFixedSize(QtCore.QSize(50, 400))
        self.push_right.setFixedSize(QtCore.QSize(50, 400))
        self.label_image.setFixedSize(QtCore.QSize(300, 400))
        
    
    def retranslateUI(self):
        
        self.setWindowTitle(self.tr("Crop Image"))
        self.choose_label.setText(self.tr("Choose version of Kindle"))
        self.version_check.setText(self.tr("Default"))
        for index, i in enumerate(KINDLE_VERSIONS):
            self.version_combo.setItemText(index, i)
        self.version_combo.setCurrentIndex(self.version)
        self.push_crop.setText(self.tr("Crop"))
        self.push_ok.setText(self.tr("OK"))
        self.push_left.setText("<")
        self.push_right.setText(">")
        
        self.setSizeUI()        
        
    def translateUI(self):
        
        app = QtGui.QApplication.instance()
        self.language_translator = QtCore.QTranslator()
        if "en" in self.language:
            pass
        else:
            path = self.language + ".qm"
            self.language_translator.load(path)
        app.installTranslator(self.language_translator)
        self.retranslateUI()
        
    def centerUI(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def openImage(self):
        
        self.clear_im = Image.open(self.im_path)
        self.setgrayscaleImage()
        self.resizeImage()
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        self.blackImage(True)
        self.putImage()
        self.changeSize()
        self.checkActive()
        
    def pasteImage(self):
        
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        self.blackImage(False)
        self.putImage()
        self.changeSize()
        self.checkActive()
        
    def putImage(self):
        
        screen_width = QtGui.QDesktopWidget().availableGeometry().width()
        height = self.im.size[1]/self.screen_coeff
        width = self.im.size[0]/self.screen_coeff
        while screen_width < width + self.push_left.width()*2:            
            self.screen_coeff = self.screen_coeff*2
            height = height/2
            width = width/2
            screen_width = QtGui.QDesktopWidget().availableGeometry().width()
            
        self.label_image.setFixedHeight(height)
        self.label_image.setFixedWidth(width)
        self.push_left.setFixedHeight(height)
        self.push_right.setFixedHeight(height)

        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.label_image.size())
        self.label_image.setPixmap(pixmap)
    
    def resizeImage(self):
        s = self.version_combo.currentText()
        pattern = re.compile(r"(\d*).x.(\d*)")
        self.height_need = int(re.search(pattern, s).group(1))
        self.width_need = int(re.search(pattern, s).group(2))
        self.clear_im = self.clear_im.convert("RGB")
        
        new_height = self.height_need
        ratio = new_height/self.clear_im.size[1]
        new_width = ceil(ratio*self.clear_im.size[0])
        
        if ratio != 1.0:
            if self.clear_im.size > (self.width_need, self.height_need):
                self.clear_im = self.clear_im.resize((new_width, new_height), Image.ANTIALIAS)      #downscaling
            else:
                self.clear_im = self.clear_im.resize((new_width, new_height), Image.BICUBIC)        #upscaling
        
        if new_width < self.width_need:
            #resize with needed width and crop upper and lower line
            ratio = self.width_need/new_width
            new_width = self.width_need
            new_height = ceil(ratio*new_height)
            delta = (new_height-self.height_need)/2
            self.clear_im = self.clear_im.resize((new_width, new_height))
            self.clear_im = self.clear_im.crop((0, ceil(delta), new_width, ceil(delta) + self.height_need))
            
        self.clear_im = self.clear_im.convert("RGBA")
    
    def blackImage(self, default=True):
        
        im_width = self.im.size[0]
        im_height = self.im.size[1]
        if im_width > self.width_need:
            if default:
                self.delta_left = self.delta_right = (im_width - self.width_need)/2
            draw = ImageDraw.Draw(self.im)
            draw.rectangle([0, 0, self.delta_left, self.height_need], fill="Black")
            draw.rectangle([im_width-self.delta_right, 0, im_width, im_height], fill="Black") 
        else:
            return
    
    def changeBlack(self):
        
        if self.sender().objectName() == "push_right":
            self.delta_left +=10
            self.delta_right -=10
        else:
            self.delta_left -=10
            self.delta_right +=10
        
        if self.delta_left < 0: self.delta_left = 0; self.delta_right = self.im.size[0] - self.width_need
        if self.delta_right < 0: self.delta_right = 0; self.delta_left = self.im.size[0] - self.width_need
        
        self.pasteImage()
        
    def cropImage(self):
        
        height = self.clear_im.size[1]
        self.clear_im = self.clear_im.crop((floor(self.delta_left), 0, floor(self.delta_left) + self.width_need, height))
        self.pasteImage()
    
    def setgrayscaleImage(self):
        
        stat = ImageStat.Stat(self.clear_im)
        if sum(stat.sum)/3 != stat.sum[0]:
            self.clear_im = self.clear_im.convert("LA")
            self.clear_im = self.clear_im.convert("RGBA")
    
    def closeEvent(self, event):
        
        if 'ok' in self.sender().objectName():
            return
        else:
            self.im = None
    
    def checkActive(self):
        
        state = self.im.size[0] == self.width_need
        self.push_crop.setEnabled(not state)
        self.push_ok.setEnabled(state)
        self.push_left.setEnabled(not state)
        self.push_right.setEnabled(not state)
        
        if self.version == self.version_combo.currentIndex():
            self.version_check.setEnabled(False)
        else:
            self.version_check.setEnabled(True)
            self.version_check.setChecked(False)
    
    def changeVersion(self):
        
        self.version = self.version_combo.currentIndex()
        self.checkActive()
    
    def initActions(self):
        
        self.push_left.clicked.connect(self.changeBlack)
        self.push_right.clicked.connect(self.changeBlack)
        self.push_crop.clicked.connect(self.cropImage)
        self.version_combo.currentIndexChanged.connect(self.openImage)
        self.push_ok.clicked.connect(self.close)
        self.version_check.stateChanged.connect(self.changeVersion)
    
class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.im = ""
        self.initUi()
        self.retranslateUI()
        self.initStateUI()
        self.initVariables()
        self.loadUI()
        self.initActions()
        
    def initVariables(self):
        
        self.language_translator = QtCore.QTranslator()
        self.text_frame = 20
        self.text_x = self.text_frame
        self.text_y = self.text_frame
        self.text_color = None
        self.is_label = True
        self.is_text = False
        
        self.im = None
        self.clear_im = None
        self.label = None
        self.file_path = None

    def initUi(self):
        
        self.centralWidget = QtGui.QWidget(self)
        self.main_layout = QtGui.QHBoxLayout(self.centralWidget)
        #------------------------------------------
        self.LeftVertLayout = QtGui.QVBoxLayout()
        
        self.open_HorLayout = QtGui.QHBoxLayout()
        
        self.open_path = QtGui.QLineEdit(self.centralWidget)
        self.open_path.setReadOnly(True)                                            #field for open path is not editable
        self.button_open = QtGui.QPushButton(self.centralWidget)
        
        self.open_HorLayout.addWidget(self.open_path)
        self.open_HorLayout.addWidget(self.button_open)
        self.LeftVertLayout.addLayout(self.open_HorLayout)
        #------------------------------------------
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.LeftVertLayout.addItem(spacerItem)
        #------------------------------------------
        self.line_1 = QtGui.QFrame(self.centralWidget)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_1)
        #------------------------------------------
        self.name_Grid = QtGui.QGridLayout()
        self.label_name = QtGui.QLabel(self.centralWidget)
        self.label_surname = QtGui.QLabel(self.centralWidget)
        self.name = QtGui.QLineEdit(self.centralWidget)
        self.surname = QtGui.QLineEdit(self.centralWidget)
        
        self.name_Grid.addWidget(self.label_name, 0, 0, 1, 1)     
        self.name_Grid.addWidget(self.label_surname, 1, 0, 1, 1)
        self.name_Grid.addWidget(self.name, 0, 1, 1, 1)
        self.name_Grid.addWidget(self.surname, 1, 1, 1, 1)
        self.LeftVertLayout.addLayout(self.name_Grid)
        #------------------------------------------
        self.line_2 = QtGui.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_2)
        #------------------------------------------
        self.textcolor_Grid = QtGui.QGridLayout()
        self.buttonGroup_TextColor = QtGui.QButtonGroup(self)
        
        self.radio_White = QtGui.QRadioButton(self.centralWidget)
        self.radio_White.setChecked(True)
        self.radio_Black = QtGui.QRadioButton(self.centralWidget)
        
        self.buttonGroup_TextColor.addButton(self.radio_White)
        self.textcolor_Grid.addWidget(self.radio_White, 1, 0, 1, 1)
        self.buttonGroup_TextColor.addButton(self.radio_Black)
        self.textcolor_Grid.addWidget(self.radio_Black, 2, 0, 1, 1)
        
        self.label_textcolor = QtGui.QLabel(self.centralWidget)
        self.textcolor_Grid.addWidget(self.label_textcolor, 0, 1, 1, 1)
        
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem1, 0, 2, 1, 1)
        
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem2, 0, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.textcolor_Grid)
        #------------------------------------------
        self.line_3 = QtGui.QFrame(self.centralWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_3)
        #------------------------------------------
        self.placetext_Grid = QtGui.QGridLayout()
        self.label_wherePlace = QtGui.QLabel(self.centralWidget)
        
        self.placetext_Grid.addWidget(self.label_wherePlace, 2, 0, 1, 1)
        
        self.grid_radio_placetext = QtGui.QGridLayout()
        
        self.radio_leftupper = QtGui.QRadioButton(self.centralWidget)
        
        self.radio_leftupper.setChecked(True)
        self.radio_leftupper.setObjectName("left_upper")
        self.buttonGroup_PlaceText = QtGui.QButtonGroup(self)
        self.buttonGroup_PlaceText.addButton(self.radio_leftupper)
        self.grid_radio_placetext.addWidget(self.radio_leftupper, 0, 0, 1, 1)
        
        self.radio_leftlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftlower.setObjectName("left_lower")
        self.buttonGroup_PlaceText.addButton(self.radio_leftlower)
        self.grid_radio_placetext.addWidget(self.radio_leftlower, 1, 0, 1, 1)   
        
        self.radio_rightupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightupper.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_rightupper.setObjectName("right_upper")
        self.buttonGroup_PlaceText.addButton(self.radio_rightupper)
        self.grid_radio_placetext.addWidget(self.radio_rightupper, 0, 1, 1, 1)
        
        self.radio_rightlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightlower.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_rightlower.setObjectName("right_lower")
        self.buttonGroup_PlaceText.addButton(self.radio_rightlower)
        self.grid_radio_placetext.addWidget(self.radio_rightlower, 1, 1, 1, 1)
        
        self.placetext_Grid.addLayout(self.grid_radio_placetext, 3, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.placetext_Grid)
        #------------------------------------------
        self.line_4 = QtGui.QFrame(self.centralWidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.LeftVertLayout.addWidget(self.line_4)
        #------------------------------------------
        self.slide_HorLayout = QtGui.QHBoxLayout()
        self.check_slide = QtGui.QCheckBox(self.centralWidget)
        
        self.slide_HorLayout.addWidget(self.check_slide)
        #spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #self.slide_HorLayout.addItem(spacerItem3)
        self.LeftVertLayout.addLayout(self.slide_HorLayout)
        #------------------------------------------
        self.button_create = QtGui.QPushButton(self.centralWidget)
        self.LeftVertLayout.addWidget(self.button_create)
        #------------------------------------------
        self.main_layout.addLayout(self.LeftVertLayout)
        self.RightVertLayout = QtGui.QVBoxLayout()
        
        self.label_image = QtGui.QLabel(self.centralWidget)
        self.label_image.setStyleSheet(_fromUtf8("border-style: solid;\n"
                                                 "border-width: 1px;\n"
                                                 "border-color: white;"))
        self.RightVertLayout.addWidget(self.label_image)
        #------------------------------------------
        self.grid_arrows = QtGui.QGridLayout()
        self.button_up = QtGui.QPushButton(self.centralWidget)
        self.button_up.setObjectName("button_up")
        self.grid_arrows.addWidget(self.button_up, 0, 1, 1, 1, QtCore.Qt.AlignBottom)
        self.button_left = QtGui.QPushButton(self.centralWidget)
        self.button_left.setObjectName("button_left")
        self.grid_arrows.addWidget(self.button_left, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.button_right = QtGui.QPushButton(self.centralWidget)
        self.button_right.setObjectName("button_right")
        self.grid_arrows.addWidget(self.button_right, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.button_down = QtGui.QPushButton(self.centralWidget)
        self.button_down.setObjectName("button_down")
        self.grid_arrows.addWidget(self.button_down, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.RightVertLayout.addLayout(self.grid_arrows) 
        #------------------------------------------
        self.main_layout.addLayout(self.RightVertLayout)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(self)
        self.menuMain = QtGui.QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.menuLanguage = QtGui.QMenu(self.menuMain)
        self.actionEnglish = QtGui.QAction(self)
        self.actionEnglish.setObjectName("en")
        self.actionRussian = QtGui.QAction(self)
        self.actionRussian.setObjectName("ru")
        self.actionUkrainian = QtGui.QAction(self)
        self.actionUkrainian.setObjectName("ukr")
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionRussian)
        self.menuLanguage.addAction(self.actionUkrainian)
        self.menuMain.addAction(self.menuLanguage.menuAction())
        self.action_Exit = QtGui.QAction(self)
        self.menuMain.addAction(self.action_Exit)
        self.menuBar.addAction(self.menuMain.menuAction())
        
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setSizeUI(self):
        
        self.open_path.setMinimumSize(QtCore.QSize(0, 20))
        self.button_open.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_White.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_Black.setMinimumSize(QtCore.QSize(0, 20))
        self.label_textcolor.setMinimumSize(QtCore.QSize(0, 20))
        self.label_wherePlace.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftlower.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightlower.setMinimumSize(QtCore.QSize(0, 20))
        self.button_create.setMinimumSize(QtCore.QSize(0, 20))
        self.label_image.setMinimumSize(QtCore.QSize(300, 400))
        self.label_image.setMaximumSize(QtCore.QSize(300, 400))
        
        self.button_up.setMinimumSize(QtCore.QSize(35, 35))
        self.button_up.setMaximumSize(QtCore.QSize(35, 35))
        self.button_left.setMinimumSize(QtCore.QSize(35, 35))
        self.button_left.setMaximumSize(QtCore.QSize(35, 35))
        self.button_right.setMinimumSize(QtCore.QSize(35, 35))
        self.button_right.setMaximumSize(QtCore.QSize(35, 35))
        self.button_down.setMinimumSize(QtCore.QSize(35, 35))
        self.button_down.setMaximumSize(QtCore.QSize(35, 35))
        
        #self.menuBar.setGeometry(QtCore.QRect(0, 0, 648, 20))
        
    def retranslateUI(self):
        self.setWindowTitle("All Kindle ScreenSaver Creator")
        
        #for ico files 
        #im = QtGui.QImageReader(ICON).read()
        #self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(ICON))
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.button_open.setText(self.tr("Open..."))
        self.label_name.setText(self.tr("Name"))
        self.label_surname.setText(self.tr("Surname"))
        self.radio_White.setText(self.tr("White"))
        self.radio_Black.setText(self.tr("Black"))
        self.label_textcolor.setText(self.tr("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Text color</span></p></body></html>"))
        self.label_wherePlace.setText(self.tr("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Where to place text</span></p></body></html>"))
        self.radio_leftupper.setText(self.tr("Left Upper"))
        self.radio_rightlower.setText(self.tr("Right Lower"))
        self.radio_leftlower.setText(self.tr("Left Lower"))
        self.radio_rightupper.setText(self.tr("Right Upper"))
        
        self.check_slide.setText("")
        self.button_create.setText(self.tr("Create"))
        self.button_up.setText("\N{UPWARDS ARROW}")
        self.button_up.setShortcut("Up")
        self.button_left.setText("\N{LEFTWARDS ARROW}")
        self.button_left.setShortcut("Left")
        self.button_right.setText("\N{RIGHTWARDS ARROW}")
        self.button_right.setShortcut("Right")
        self.button_down.setText("\N{DOWNWARDS ARROW}")
        self.button_down.setShortcut("Down")
        self.menuMain.setTitle(self.tr("Main"))
        self.action_Exit.setText(self.tr("Exit"))
        self.menuLanguage.setTitle(self.tr("Language"))
        self.actionEnglish.setText("English")
        self.actionRussian.setText("Русский")
        self.actionUkrainian.setText("Українська")
        
        self.setSizeUI()
    
    def centerUI(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initStateUI(self):
        
        self.name.setEnabled(False)
        self.surname.setEnabled(False)
        self.radio_leftlower.setEnabled(False)
        self.radio_leftupper.setEnabled(False)
        self.radio_rightlower.setEnabled(False)
        self.radio_rightupper.setEnabled(False)
        self.radio_Black.setEnabled(False)
        self.radio_White.setEnabled(False)
        self.check_slide.setEnabled(False)
        self.button_left.setEnabled(False)
        self.button_right.setEnabled(False)
        self.button_up.setEnabled(False)
        self.button_down.setEnabled(False)
        self.button_create.setEnabled(False)
    
    def surnameState(self):
        
        enabled = bool(self.name.text())
        self.surname.setEnabled(enabled)
        self.radio_leftlower.setEnabled(enabled)
        self.radio_leftupper.setEnabled(enabled)
        self.radio_rightlower.setEnabled(enabled)
        self.radio_rightupper.setEnabled(enabled)
        self.radio_Black.setEnabled(enabled)
        self.radio_White.setEnabled(enabled)
        self.button_left.setEnabled(enabled)
        self.button_right.setEnabled(enabled)
        self.button_up.setEnabled(enabled)
        self.button_down.setEnabled(enabled)
        self.label_textcolor.setEnabled(enabled)
        self.label_wherePlace.setEnabled(enabled)
        if not enabled:
            self.surname.setText("")
            
    def putImage(self):
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.label_image.size())
        self.label_image.setPixmap(pixmap)
    
    def redrawImage(self):
        
        self.is_label = self.check_slide.isChecked()
        self.is_text = self.name.text() or self.surname.text()
        self.pasteImage()
                
        if self.is_label:
            self.im.paste(self.label, mask = self.label) 
        
        if self.is_text:
            size = FONT_SIZE
            draw = ImageDraw.Draw(self.im)
            font = ImageFont.truetype(FONT, FONT_SIZE)
            text_color = "White"
            if self.radio_Black.isChecked():
                text_color = "Black"
            else:
                text_color = "White"
            
            self.correctText(font=font, size=size)
            #draw name
            if self.name.text():
                draw.text((self.text_x, self.text_y), self.name.text(), text_color, font=font)
            #draw surname
            if self.surname.text():
                draw.text((self.text_x, self.text_y + size), self.surname.text(), text_color, font=font)

        self.putImage()

    def moveText(self):
        default_move = {"button_up"  : (0, -10),
                        "button_left" : (-10, 0),
                        "button_right" : (10, 0),
                        "button_down": (0, 10)}
        self.text_x += default_move[self.sender().objectName()][0]
        self.text_y += default_move[self.sender().objectName()][1]
        self.redrawImage()
    
    def placeText(self, corner):
        
        default_coord = {"left_upper" : (self.text_frame, self.text_frame),
                          "left_lower" : (self.text_frame, self.im.size[1]),
                          "right_upper" : (self.im.size[0], self.text_frame),
                          "right_lower" : (self.im.size[0], self.im.size[1])}
        
        self.text_x, self.text_y = default_coord[self.sender().objectName()]
        self.redrawImage()
    
    def correctText(self, font, size):
        
        font = font
        size_x = self.im.size[0] - self.text_frame
        size_y = self.im.size[1] - self.text_frame - 50
        text_height = 0
        text_lenght = 0
        name = self.name.text()
        surname = self.surname.text()
        
        if self.text_x < self.text_frame: self.text_x = self.text_frame
        if self.text_y < self.text_frame: self.text_y = self.text_frame
        
        if name and surname:
            text_height = 2*size
        else:
            text_height = size
        
        if len(name) >= len(surname):
            text_lenght = font.getsize(name)[0]
        else:
            text_lenght = font.getsize(surname)[0]
                
        if self.text_x + text_lenght > size_x:
            dx = (self.text_x + text_lenght) - size_x
            self.text_x -= dx
        if self.text_y + text_height > size_y:
            dy = (self.text_y + text_height) - size_y
            self.text_y -= dy        
        
    def openImage(self):
        #filedialog = QtGui.QFileDialog(self)
        #filedialog.setLabelText(filedialog.Accept, self.tr('Open'))
        #filedialog.setLabelText(filedialog.Reject, self.tr('Cancel'))
        #self.file_path = filedialog.getOpenFileName(self, self.tr('Open file'), '/home')
        self.setEnabled(False)
        self.file_path = QtGui.QFileDialog.getOpenFileName(self, self.tr('Open file'), '/home')
        self.setEnabled(True)
        if self.file_path == '':
            return
        if path.split(self.file_path)[-1].split('.')[1].lower() not in IMAGE_FORMATS:
            self.statusBar.showMessage(self.tr('No image'))
            return
        
        #place for dialog crop
        
        ui = CropDialog(self.file_path, language = self.language, version = self.version)
        self.setEnabled(False)      
        ui.exec_()
        self.setEnabled(True)
        try:
            self.clear_im = Image.new(size=ui.im.size, mode=ui.im.mode)
            self.clear_im.paste(ui.im)
            self.version = ui.version
        except:
            return
        
        #end of place for dialog crop
        if not self.name.isEnabled():
            self.name.setEnabled(True)
        
        kindle_version = ui.version_combo.currentText()
        if "Kindle 3" in kindle_version:
            self.label = Image.open(LABEL_3).convert("RGBA")
        elif "DX" in kindle_version:
            self.label = Image.open(LABEL_DX).convert("RGBA")
        elif "Paperwhite 1" in kindle_version:
            self.label = Image.open(LABEL_PAPER_1).convert("RGBA")
        elif "Paperwhite 2" in kindle_version:
            self.label = Image.open(LABEL_1024).convert("RGBA")
        else:
            self.label = Image.open(LABEL_800).convert("RGBA")
        
        if "Kindle 3" in kindle_version or "Kindle DX" in kindle_version:
            self.check_slide.setText("Slide and release the power to wake")
            self.text_x = self.text_y = self.text_frame = 10
        else:
            self.check_slide.setText("Press the power switch to wake")
        self.check_slide.setEnabled(True)
        self.check_slide.setChecked(True)
        
        if not self.radio_leftupper.isChecked():
            self.radio_leftupper.setChecked(True)
        if self.name.text():
            self.name.setText("")
        if self.surname.text():
            self.surname.setText("")
        self.label_image.setFixedWidth(self.clear_im.size[0]/2)
        self.label_image.setFixedHeight(self.clear_im.size[1]/2)
        self.surnameState()
        self.button_create.setEnabled(True)
        #self.text_x = 10
        #self.text_y = 10
        self.redrawImage()
        self.centerUI()
        
        self.open_path.setText(self.file_path)
        self.statusBar.showMessage(self.tr("Opened file"))
    
    def pasteImage(self):
        
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        
    def saveImage(self):
        
        default = self.tr("Sample")
        name = ""
        self.redrawImage()
        if self.name.text():
            name+=self.name.text()
        if self.surname.text():
            name+= ' ' + self.surname.text()
        if not name:
            name = default
        name += ' ' + str(self.im.size[1]) + 'x' + str(self.im.size[0])
              
        if path.isfile(path.join(SAVE_PATH, name + ".png")):
            i = 2
            while path.isfile(path.join(SAVE_PATH, name+'-' + str(i) + '.png')):
                i+=1
            name+= '-' + str(i)
        name +=".png"
        self.im.save(path.join(SAVE_PATH, name))
        self.statusBar.showMessage(self.tr("File {} created!").format(name))
            
    def initActions(self):
        
        self.action_Exit.triggered.connect(self.close)
        self.check_slide.stateChanged.connect(self.redrawImage)
        self.button_open.clicked.connect(self.openImage)
        self.button_create.clicked.connect(self.saveImage)
        self.name.textChanged.connect(self.redrawImage)
        self.name.textChanged.connect(self.surnameState)
        self.surname.textChanged.connect(self.redrawImage)
        self.radio_Black.clicked.connect(self.redrawImage)
        self.radio_White.clicked.connect(self.redrawImage)
        self.radio_leftlower.clicked.connect(self.placeText)
        self.radio_leftupper.clicked.connect(self.placeText)
        self.radio_rightlower.clicked.connect(self.placeText)
        self.radio_rightupper.clicked.connect(self.placeText)
        self.button_up.pressed.connect(self.moveText)
        self.button_down.pressed.connect(self.moveText)
        self.button_left.pressed.connect(self.moveText)
        self.button_right.pressed.connect(self.moveText)
        self.actionRussian.triggered.connect(self.translateUI)
        self.actionEnglish.triggered.connect(self.translateUI)
        self.actionUkrainian.triggered.connect(self.translateUI)
    
    def translateUI(self, no_sent = False):
        
        app = QtGui.QApplication.instance()
        self.language_translator = QtCore.QTranslator()
        if not no_sent:
            self.language = self.sender().objectName()
        
        if "en" in self.language:
            pass
        else:
            path = self.language + ".qm"
            self.language_translator.load(path)
        app.installTranslator(self.language_translator)
        self.retranslateUI()
        
    
    def saveUI(self):
        
        self.settings = QtCore.QSettings("src/src.ini", QtCore.QSettings.IniFormat)
        self.settings.setValue("language", self.language)
        self.settings.setValue("version", self.version)
        
    def loadUI(self):
        
        self.settings = QtCore.QSettings("src/src.ini", QtCore.QSettings.IniFormat)
        self.language = self.settings.value("language")
        self.version = int(self.settings.value("version"))
        if not self.language:
            self.language = "en"
        if not self.version:
            self.version = 0
        self.translateUI(no_sent=True)
        
    def closeEvent(self, event):
        
        self.saveUI()
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
