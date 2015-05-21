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
TEXT_FRAME = 20
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
        for _ in KINDLE_VERSIONS: self.version_combo.addItem("")
        self.version_ver_layout.addWidget(self.version_check)
        self.version_ver_layout.addWidget(self.version_combo)
        self.button_hor_layout.addLayout(self.version_ver_layout)
        
        self.ok_ver_layout = QtGui.QVBoxLayout()
        self.crop_button = QtGui.QPushButton(self)
        
        self.crop_button.setObjectName("crop_button")
        self.ok_button = QtGui.QPushButton(self)
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setEnabled(False)
        self.ok_ver_layout.addWidget(self.crop_button)
        self.ok_ver_layout.addWidget(self.ok_button)
        
        self.button_hor_layout.addLayout(self.ok_ver_layout)
        self.main_layout.addLayout(self.button_hor_layout)
        self.image_hor_layout = QtGui.QHBoxLayout()
        self.image_hor_layout.setObjectName(_fromUtf8("image_hor_layout"))
        self.left_button = QtGui.QPushButton(self)
        
        self.left_button.setObjectName("left_button")
        self.image_hor_layout.addWidget(self.left_button)
        self.image_label = QtGui.QLabel(self)
        
        self.image_label.setStyleSheet(_fromUtf8("border-width: 1px;\n"
                                                 "border-style: solid"))
        self.image_label.setObjectName("image_label")
        self.image_hor_layout.addWidget(self.image_label)
        self.right_button = QtGui.QPushButton(self)
        self.right_button.setObjectName("right_button")
        self.image_hor_layout.addWidget(self.right_button)
        self.main_layout.addLayout(self.image_hor_layout)

        self.retranslateUI()
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)
    
    
    def setSizeUI(self):
        '''make cropdialog having the same size'''
        h = 25
        lab_w = self.fontMetrics().boundingRect(self.choose_label.text()).width() + 7
        self.choose_label.setFixedSize(QtCore.QSize(lab_w, h))
        
        combo_w = self.fontMetrics().boundingRect(self.version_combo.itemText(4)).width() + 7
        self.version_combo.setFixedSize(QtCore.QSize(combo_w, h))
        
        self.crop_button.setFixedSize(QtCore.QSize(100, h))
        self.ok_button.setFixedSize(QtCore.QSize(100, h))
        self.left_button.setFixedSize(QtCore.QSize(50, 400))
        self.right_button.setFixedSize(QtCore.QSize(50, 400))
        self.image_label.setFixedSize(QtCore.QSize(300, 400))
    
    def retranslateUI(self):
        '''filling in label/button text'''
        self.setWindowTitle(self.tr("Crop Image"))
        self.choose_label.setText(self.tr("Choose version of Kindle"))
        self.version_check.setText(self.tr("Default"))
        for index, i in enumerate(KINDLE_VERSIONS):
            self.version_combo.setItemText(index, i)
        self.version_combo.setCurrentIndex(self.version)
        self.crop_button.setText(self.tr("Crop"))
        self.ok_button.setText(self.tr("OK"))
        self.left_button.setText("<")
        self.right_button.setText(">")
        self.setSizeUI()        
        
    def centerUI(self):
        '''place at the center of screen'''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def openImage(self):
        '''clear image - first init and for final applying'''
        self.clear_im = Image.open(self.im_path)
        self.setGrayscaleImage()
        self.resizeImage()
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        self.blackImage(True)
        self.putImage()
        self.changeSize()
        self.checkActive()
        
    def pasteImage(self):
        '''creating copy of image for working'''
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        self.blackImage(False)
        self.putImage()
        self.changeSize()
        self.checkActive()
        
    def putImage(self):
        '''put image at the label'''
        screen_width = QtGui.QDesktopWidget().availableGeometry().width()
        height = self.im.size[1]/self.screen_coeff
        width = self.im.size[0]/self.screen_coeff
        while screen_width < width + self.left_button.width()*2:            
            self.screen_coeff = self.screen_coeff*2
            height = height/2
            width = width/2
            screen_width = QtGui.QDesktopWidget().availableGeometry().width()
            
        self.image_label.setFixedHeight(height)
        self.image_label.setFixedWidth(width)
        self.left_button.setFixedHeight(height)
        self.right_button.setFixedHeight(height)

        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.image_label.size())
        self.image_label.setPixmap(pixmap)
    
    def resizeImage(self):
        '''resize image after changing version'''
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
        '''black rectangles left-right'''
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
    
    def changeCropImage(self):
        '''image change cropping area'''
        if self.sender().objectName() == "right_button":
            self.delta_left +=10
            self.delta_right -=10
        else:
            self.delta_left -=10
            self.delta_right +=10
        
        #bound to the edge
        if self.delta_left < 0: self.delta_left = 0; self.delta_right = self.im.size[0] - self.width_need
        if self.delta_right < 0: self.delta_right = 0; self.delta_left = self.im.size[0] - self.width_need
        
        self.pasteImage()
        
    def cropImage(self):
        '''image crop'''
        height = self.clear_im.size[1]
        self.clear_im = self.clear_im.crop((floor(self.delta_left), 0, floor(self.delta_left) + self.width_need, height))
        self.pasteImage()
    
    def setGrayscaleImage(self):
        '''image - grayscale'''
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
        '''make some elements inactive after cropping'''
        state = self.im.size[0] == self.width_need
        self.crop_button.setEnabled(not state)
        self.ok_button.setEnabled(state)
        self.left_button.setEnabled(not state)
        self.right_button.setEnabled(not state)
        
        if self.version == self.version_combo.currentIndex():
            self.version_check.setEnabled(False)
        else:
            self.version_check.setEnabled(True)
            self.version_check.setChecked(False)
    
    def changeVersion(self):
        '''version combo is triggered'''
        self.version = self.version_combo.currentIndex()
        self.checkActive()
    
    def initActions(self):
        
        self.left_button.clicked.connect(self.changeCropImage)
        self.right_button.clicked.connect(self.changeCropImage)
        self.crop_button.clicked.connect(self.cropImage)
        self.version_combo.currentIndexChanged.connect(self.openImage)
        self.ok_button.clicked.connect(self.close)
        self.version_check.stateChanged.connect(self.changeVersion)
    
class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.initUi()
        self.retranslateUI()
        self.initStateUI()
        self.initVariables()
        self.loadUI()
        self.initActions()
        
    def initVariables(self):
        '''main variables'''
        self.language_translator = QtCore.QTranslator()
        self.text_frame = TEXT_FRAME
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
        
        self.central_widget = QtGui.QWidget(self)
        self.main_layout = QtGui.QHBoxLayout(self.central_widget)
        #------------------------------------------
        self.left_ver_layout = QtGui.QVBoxLayout()
        
        self.open_hor_layout = QtGui.QHBoxLayout()
        
        self.open_edit = QtGui.QLineEdit(self.central_widget)
        self.open_edit.setReadOnly(True)                                            #field for open path is not editable
        self.open_button = QtGui.QPushButton(self.central_widget)
        
        self.open_hor_layout.addWidget(self.open_edit)
        self.open_hor_layout.addWidget(self.open_button)
        self.left_ver_layout.addLayout(self.open_hor_layout)
        self.left_ver_layout.addStretch(1)
        #------------------------------------------
        self.line_1 = QtGui.QFrame(self.central_widget)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_ver_layout.addWidget(self.line_1)
        #------------------------------------------
        self.txt_grid = QtGui.QGridLayout()
        self.txt_label = QtGui.QLabel()
        self.name_label = QtGui.QLabel(self.central_widget)
        self.surname_label = QtGui.QLabel(self.central_widget)
        self.name_edit = QtGui.QLineEdit(self.central_widget)
        self.surname_edit = QtGui.QLineEdit(self.central_widget)
        self.txt_grid.addWidget(self.name_label, 0, 0, 1, 1)     
        self.txt_grid.addWidget(self.surname_label, 1, 0, 1, 1)
        self.txt_grid.addWidget(self.name_edit, 0, 1, 1, 1)
        self.txt_grid.addWidget(self.surname_edit, 1, 1, 1, 1)
        self.left_ver_layout.addWidget(self.txt_label)
        self.left_ver_layout.addLayout(self.txt_grid)
        #------------------------------------------
        self.line_2 = QtGui.QFrame(self.central_widget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_ver_layout.addWidget(self.line_2)
        #------------------------------------------
        self.txtcolor_label = QtGui.QLabel()
        self.white_radio = QtGui.QRadioButton()
        self.white_radio.setChecked(True)
        self.black_radio = QtGui.QRadioButton()
        
        self.left_ver_layout.addWidget(self.txtcolor_label)
        self.left_ver_layout.addWidget(self.white_radio)
        self.left_ver_layout.addWidget(self.black_radio)
        #------------------------------------------
        self.line_3 = QtGui.QFrame(self.central_widget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_ver_layout.addWidget(self.line_3)
        #------------------------------------------
        self.txtplace_label = QtGui.QLabel()
        self.txtplace_grid = QtGui.QGridLayout()
        self.leftupper_radio = QtGui.QRadioButton()
        self.leftupper_radio.setObjectName("left_upper")
        self.leftlower_radio = QtGui.QRadioButton()
        self.leftlower_radio.setObjectName("left_lower")
        self.rightupper_radio = QtGui.QRadioButton()
        self.rightupper_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rightupper_radio.setObjectName("right_upper")
        self.rightlower_radio = QtGui.QRadioButton()
        self.rightlower_radio.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rightlower_radio.setObjectName("right_lower")
        
        self.txtplace_group = QtGui.QButtonGroup()
        self.txtplace_group.addButton(self.leftupper_radio)
        self.txtplace_group.addButton(self.leftlower_radio)
        self.txtplace_group.addButton(self.rightupper_radio)
        self.txtplace_group.addButton(self.rightlower_radio)
        self.leftupper_radio.setChecked(True)
        
        self.txtplace_grid.addWidget(self.leftupper_radio, 0, 0, 1, 1)
        self.txtplace_grid.addWidget(self.leftlower_radio, 1, 0, 1, 1)
        self.txtplace_grid.addWidget(self.rightupper_radio, 0, 1, 1, 1)
        self.txtplace_grid.addWidget(self.rightlower_radio, 1, 1, 1, 1)
        
        self.left_ver_layout.addWidget(self.txtplace_label)
        self.left_ver_layout.addLayout(self.txtplace_grid)
        
        #------------------------------------------
        self.line_4 = QtGui.QFrame(self.central_widget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.left_ver_layout.addWidget(self.line_4)
        #------------------------------------------
        self.slide_check = QtGui.QCheckBox(self.central_widget)
        self.create_button = QtGui.QPushButton(self.central_widget)
        
        self.left_ver_layout.addWidget(self.slide_check)
        self.left_ver_layout.addWidget(self.create_button)
        #------------------------------------------
        self.main_layout.addLayout(self.left_ver_layout)
        self.right_ver_layout = QtGui.QVBoxLayout()
        
        self.image_label = QtGui.QLabel(self.central_widget)
        self.image_label.setStyleSheet(_fromUtf8("border-style: solid;\n"
                                                 "border-width: 1px;\n"
                                                 "border-color: white;"))
        self.right_ver_layout.addWidget(self.image_label)
        #------------------------------------------
        self.arrows_grid = QtGui.QGridLayout()
        self.up_button = QtGui.QPushButton()
        self.up_button.setObjectName("up_button")
        self.button_left = QtGui.QPushButton()
        self.button_left.setObjectName("button_left")
        self.button_right = QtGui.QPushButton()
        self.button_right.setObjectName("button_right")
        self.button_down = QtGui.QPushButton(self.central_widget)
        self.button_down.setObjectName("button_down")
        
        self.arrows_grid.addWidget(self.up_button, 0, 1, 1, 1, QtCore.Qt.AlignBottom)
        self.arrows_grid.addWidget(self.button_left, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.arrows_grid.addWidget(self.button_right, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.arrows_grid.addWidget(self.button_down, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.right_ver_layout.addLayout(self.arrows_grid)
        #------------------------------------------
        self.main_layout.addLayout(self.right_ver_layout)
        self.setCentralWidget(self.central_widget)
        self.menu_bar = QtGui.QMenuBar(self)
        self.menu = QtGui.QMenu(self.menu_bar)
        self.setMenuBar(self.menu_bar)
        self.status_bar = QtGui.QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.language_menu = QtGui.QMenu(self.menu)
        self.english_action = QtGui.QAction(self)
        self.english_action.setObjectName("en")
        self.russian_action = QtGui.QAction(self)
        self.russian_action.setObjectName("ru")
        self.ukrainian_action = QtGui.QAction(self)
        self.ukrainian_action.setObjectName("ukr")
        self.language_menu.addAction(self.english_action)
        self.language_menu.addAction(self.russian_action)
        self.language_menu.addAction(self.ukrainian_action)
        self.menu.addAction(self.language_menu.menuAction())
        self.action_Exit = QtGui.QAction(self)
        self.menu.addAction(self.action_Exit)
        self.menu_bar.addAction(self.menu.menuAction())
        
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setSizeUI(self):
        
        self.open_edit.setMinimumSize(QtCore.QSize(0, 20))
        self.open_button.setMinimumSize(QtCore.QSize(0, 20))
        self.white_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.black_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.txtcolor_label.setMinimumSize(QtCore.QSize(0, 20))
        self.txtplace_label.setMinimumSize(QtCore.QSize(0, 20))
        self.leftupper_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.leftlower_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.rightupper_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.rightlower_radio.setMinimumSize(QtCore.QSize(0, 20))
        self.create_button.setMinimumSize(QtCore.QSize(0, 20))
        self.image_label.setMinimumSize(QtCore.QSize(300, 400))
        self.image_label.setMaximumSize(QtCore.QSize(300, 400))
        
        self.up_button.setMinimumSize(QtCore.QSize(35, 35))
        self.up_button.setMaximumSize(QtCore.QSize(35, 35))
        self.button_left.setMinimumSize(QtCore.QSize(35, 35))
        self.button_left.setMaximumSize(QtCore.QSize(35, 35))
        self.button_right.setMinimumSize(QtCore.QSize(35, 35))
        self.button_right.setMaximumSize(QtCore.QSize(35, 35))
        self.button_down.setMinimumSize(QtCore.QSize(35, 35))
        self.button_down.setMaximumSize(QtCore.QSize(35, 35))
        
        #self.menu_bar.setGeometry(QtCore.QRect(0, 0, 648, 20))
        
    def retranslateUI(self):
        self.setWindowTitle("All Kindle ScreenSaver Creator")
        
        #for ico files 
        #im = QtGui.QImageReader(ICON).read()
        #self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(ICON))
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.open_button.setText(self.tr("Open..."))
        self.txt_label.setText(self.tr("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Text</span></p></body></html>"))
        self.name_label.setText(self.tr("Name"))
        self.surname_label.setText(self.tr("Surname"))
        self.white_radio.setText(self.tr("White"))
        self.black_radio.setText(self.tr("Black"))
        self.txtcolor_label.setText(self.tr("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Text color</span></p></body></html>"))
        self.txtplace_label.setText(self.tr("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Where to place text</span></p></body></html>"))
        self.leftupper_radio.setText(self.tr("Left Upper"))
        self.rightlower_radio.setText(self.tr("Right Lower"))
        self.leftlower_radio.setText(self.tr("Left Lower"))
        self.rightupper_radio.setText(self.tr("Right Upper"))
        
        self.slide_check.setText("")
        self.create_button.setText(self.tr("Create"))
        self.up_button.setText("\N{UPWARDS ARROW}")
        self.up_button.setShortcut("Up")
        self.button_left.setText("\N{LEFTWARDS ARROW}")
        self.button_left.setShortcut("Left")
        self.button_right.setText("\N{RIGHTWARDS ARROW}")
        self.button_right.setShortcut("Right")
        self.button_down.setText("\N{DOWNWARDS ARROW}")
        self.button_down.setShortcut("Down")
        self.menu.setTitle(self.tr("Main"))
        self.action_Exit.setText(self.tr("Exit"))
        self.language_menu.setTitle(self.tr("Language"))
        self.english_action.setText("English")
        self.russian_action.setText("Русский")
        self.ukrainian_action.setText("Українська")
        
        self.setSizeUI()
    
    def centerUI(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initStateUI(self):
        
        self.name_edit.setEnabled(False)
        self.surname_edit.setEnabled(False)
        self.leftlower_radio.setEnabled(False)
        self.leftupper_radio.setEnabled(False)
        self.rightlower_radio.setEnabled(False)
        self.rightupper_radio.setEnabled(False)
        self.black_radio.setEnabled(False)
        self.white_radio.setEnabled(False)
        self.slide_check.setEnabled(False)
        self.button_left.setEnabled(False)
        self.button_right.setEnabled(False)
        self.up_button.setEnabled(False)
        self.button_down.setEnabled(False)
        self.create_button.setEnabled(False)
    
    def surnameState(self):
        
        enabled = bool(self.name_edit.text())
        self.surname_edit.setEnabled(enabled)
        self.leftlower_radio.setEnabled(enabled)
        self.leftupper_radio.setEnabled(enabled)
        self.rightlower_radio.setEnabled(enabled)
        self.rightupper_radio.setEnabled(enabled)
        self.black_radio.setEnabled(enabled)
        self.white_radio.setEnabled(enabled)
        self.button_left.setEnabled(enabled)
        self.button_right.setEnabled(enabled)
        self.up_button.setEnabled(enabled)
        self.button_down.setEnabled(enabled)
        self.txtcolor_label.setEnabled(enabled)
        self.txtplace_label.setEnabled(enabled)
        if not enabled:
            self.surname_edit.setText("")
            
    def putImage(self):
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.image_label.size())
        self.image_label.setPixmap(pixmap)
    
    def redrawImage(self):
        
        self.is_label = self.slide_check.isChecked()
        self.is_text = self.name_edit.text() or self.surname_edit.text()
        self.pasteImage()
                
        if self.is_label:
            self.im.paste(self.label, mask = self.label) 
        
        if self.is_text:
            size = FONT_SIZE
            draw = ImageDraw.Draw(self.im)
            font = ImageFont.truetype(FONT, FONT_SIZE)
            text_color = "White"
            if self.black_radio.isChecked():
                text_color = "Black"
            else:
                text_color = "White"
            
            self.correctText(font=font, size=size)
            #draw name_edit
            if self.name_edit.text():
                draw.text((self.text_x, self.text_y), self.name_edit.text(), text_color, font=font)
            #draw surname_edit
            if self.surname_edit.text():
                draw.text((self.text_x, self.text_y + size), self.surname_edit.text(), text_color, font=font)

        self.putImage()

    def moveText(self):
        '''moving text by arrows'''
        default_move = {"up_button"  : (0, -10),
                        "button_left" : (-10, 0),
                        "button_right" : (10, 0),
                        "button_down": (0, 10)}
        self.text_x += default_move[self.sender().objectName()][0]
        self.text_y += default_move[self.sender().objectName()][1]
        self.redrawImage()
    
    def placeText(self, corner):
        '''default place for text - leftupper, leftlower etc'''
        default_coord = {"left_upper" : (self.text_frame, self.text_frame),
                          "left_lower" : (self.text_frame, self.im.size[1]),
                          "right_upper" : (self.im.size[0], self.text_frame),
                          "right_lower" : (self.im.size[0], self.im.size[1])}
        
        self.text_x, self.text_y = default_coord[self.sender().objectName()]
        self.redrawImage()
    
    def correctText(self, font, size):
        '''don't let text to go out of frame'''
        font = font
        size_x = self.im.size[0] - self.text_frame
        size_y = self.im.size[1] - self.text_frame - 50
        text_height = 0
        text_lenght = 0
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        
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
            self.status_bar.showMessage(self.tr('No image'))
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
        if not self.name_edit.isEnabled():
            self.name_edit.setEnabled(True)
        
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
            self.slide_check.setText("Slide and release the power to wake")
            self.text_x = self.text_y = self.text_frame = 10
        else:
            self.slide_check.setText("Press the power switch to wake")
        self.slide_check.setEnabled(True)
        self.slide_check.setChecked(True)
        
        if not self.leftupper_radio.isChecked():
            self.leftupper_radio.setChecked(True)
        if self.name_edit.text():
            self.name_edit.setText("")
        if self.surname_edit.text():
            self.surname_edit.setText("")
        self.image_label.setFixedWidth(self.clear_im.size[0]/2)
        self.image_label.setFixedHeight(self.clear_im.size[1]/2)
        self.surnameState()
        self.create_button.setEnabled(True)
        #self.text_x = 10
        #self.text_y = 10
        self.redrawImage()
        self.centerUI()
        
        self.open_edit.setText(self.file_path)
        self.status_bar.showMessage(self.tr("Opened file"))
    
    def pasteImage(self):
        
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        
    def saveImage(self):
        
        default = self.tr("Sample")
        name = ""
        self.redrawImage()
        if self.name_edit.text():
            name+=self.name_edit.text()
        if self.surname_edit.text():
            name+= ' ' + self.surname_edit.text()
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
        self.status_bar.showMessage(self.tr("File {} created!").format(name))
            
    def initActions(self):
        
        self.action_Exit.triggered.connect(self.close)
        self.slide_check.stateChanged.connect(self.redrawImage)
        self.open_button.clicked.connect(self.openImage)
        self.create_button.clicked.connect(self.saveImage)
        self.name_edit.textChanged.connect(self.redrawImage)
        self.name_edit.textChanged.connect(self.surnameState)
        self.surname_edit.textChanged.connect(self.redrawImage)
        self.black_radio.clicked.connect(self.redrawImage)
        self.white_radio.clicked.connect(self.redrawImage)
        self.leftlower_radio.clicked.connect(self.placeText)
        self.leftupper_radio.clicked.connect(self.placeText)
        self.rightlower_radio.clicked.connect(self.placeText)
        self.rightupper_radio.clicked.connect(self.placeText)
        self.up_button.pressed.connect(self.moveText)
        self.button_down.pressed.connect(self.moveText)
        self.button_left.pressed.connect(self.moveText)
        self.button_right.pressed.connect(self.moveText)
        self.russian_action.triggered.connect(self.translateUI)
        self.english_action.triggered.connect(self.translateUI)
        self.ukrainian_action.triggered.connect(self.translateUI)
    
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
        '''save default version and language'''
        self.settings = QtCore.QSettings("src/src.ini", QtCore.QSettings.IniFormat)
        self.settings.setValue("language", self.language)
        self.settings.setValue("version", self.version)
        
    def loadUI(self):
        '''load saved version and language'''
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
