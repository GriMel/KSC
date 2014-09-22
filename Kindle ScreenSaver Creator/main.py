#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#--------------------LICENSE STUFF
#
from PyQt4 import QtGui, QtCore
from PIL import Image, ImageDraw, ImageFont, ImageQt
from math import floor, ceil
import sys
import re
from os import path

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

LABEL = "resources/label.png"
SAVE_PATH = "output/"
FONT = "resources/Caecilia Regular.ttf"
FONT_SIZE = 40
ICON = "resources/Kindle.png"
IMAGE_FORMATS = ['bmp', 'dcx', 'eps', 'ps', 'gif', 'im', 'jpg', 'jpeg',
                 'jpe', 'pcd', 'pcx', 'pdf', 'png', 'pbm', 'pgm', 'ppm',
                 'psd', 'tif', 'tiff', 'xmb', 'xpm']

class CropDialog(QtGui.QDialog):
    
    def __init__(self, im_path):
        super(CropDialog, self).__init__()
        self.initUI()
        self.im_path = im_path
        self.initVariables()
        self.openImage()
        self.initActions()
        self.checkActive()
    
    def initVariables(self):
        
        self.delta_left = None
        self.delta_right = None
                
    def initUI(self):
        
        self.resize(550, 500)
        self.MainLayout = QtGui.QVBoxLayout(self)
        self.ButtonHorLayout = QtGui.QHBoxLayout()
        self.label_version = QtGui.QLabel(self)
        self.label_version.setMinimumSize(QtCore.QSize(0, 20))
        self.label_version.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_version.setObjectName(_fromUtf8("label_version"))
        self.ButtonHorLayout.addWidget(self.label_version)
        
        self.combo_versionKindle = QtGui.QComboBox(self)
        self.combo_versionKindle.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_versionKindle.setObjectName("combo_versionKindle")
        self.combo_versionKindle.addItem("")
        self.combo_versionKindle.addItem("")
        self.combo_versionKindle.addItem("")
        self.combo_versionKindle.addItem("")
        self.ButtonHorLayout.addWidget(self.combo_versionKindle)
        
        self.OkCropVerLayout = QtGui.QVBoxLayout(self)
        self.push_crop = QtGui.QPushButton(self)
        self.push_crop.setMinimumSize(QtCore.QSize(0, 30))
        self.push_crop.setObjectName("push_crop")
        self.push_ok = QtGui.QPushButton(self)
        self.push_ok.setMinimumSize(QtCore.QSize(0, 30))
        self.push_ok.setObjectName("push_ok")
        self.push_ok.setEnabled(False)
        self.OkCropVerLayout.addWidget(self.push_crop)
        self.OkCropVerLayout.addWidget(self.push_ok)
        
        self.ButtonHorLayout.addLayout(self.OkCropVerLayout)
        self.MainLayout.addLayout(self.ButtonHorLayout)
        self.ImHorLayout = QtGui.QHBoxLayout()
        self.ImHorLayout.setObjectName(_fromUtf8("ImHorLayout"))
        self.push_left = QtGui.QPushButton(self)
        self.push_left.setMinimumSize(QtCore.QSize(50, 400))
        self.push_left.setMaximumSize(QtCore.QSize(50, 400))
        self.push_left.setObjectName("push_left")
        self.ImHorLayout.addWidget(self.push_left)
        self.label_image = QtGui.QLabel(self)
        self.label_image.setMinimumSize(QtCore.QSize(300, 400))
        self.label_image.setMaximumSize(QtCore.QSize(300, 400))
        self.label_image.setStyleSheet(_fromUtf8("border-width: 1px;\n"
                                                 "border-style: solid"))
        self.label_image.setObjectName("label_image")
        self.ImHorLayout.addWidget(self.label_image)
        self.push_right = QtGui.QPushButton(self)
        self.push_right.setMinimumSize(QtCore.QSize(50, 400))
        self.push_right.setMaximumSize(QtCore.QSize(50, 400))
        self.push_right.setObjectName("push_right")
        self.ImHorLayout.addWidget(self.push_right)
        self.MainLayout.addLayout(self.ImHorLayout)

        self.retranslateUi()
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        
        self.setWindowTitle(self.tr("Crop Image"))
        self.label_version.setText("Choose version of Kindle")
        self.combo_versionKindle.setItemText(0, "Kindle 3 (800 x 600)")
        self.combo_versionKindle.setItemText(1, "Kindle 4, 5, Touch (800 x 600)")
        self.combo_versionKindle.setItemText(2, "Kindle DX (1024 x 842)")
        self.combo_versionKindle.setItemText(3, "Kindle PaperWhite (1200 x 824)")
        self.push_crop.setText(self.tr("Crop"))
        self.push_ok.setText(self.tr("OK"))
        self.push_left.setText("<")
        self.label_image.setText("<html><head/><body><p align=\"center\"><br/></p></body></html>")
        self.push_right.setText(">")
        
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
        self.checkActive()
        
    def pasteImage(self):
        
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        self.blackImage(False)
        self.putImage()
        self.checkActive()
        
    def putImage(self):
        
        height = self.im.size[1]/2
        width = self.im.size[0]/2
        self.label_image.setFixedHeight(height)
        self.label_image.setFixedWidth(width)
        self.push_left.setFixedHeight(height)
        self.push_right.setFixedHeight(height)

        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.label_image.size())
        self.label_image.setPixmap(pixmap)
    
    def resizeImage(self):
        s = self.combo_versionKindle.currentText()
        pattern = re.compile(r"(\d*).x.(\d*)")
        self.height_need = int(re.search(pattern, s).group(1))
        self.width_need = int(re.search(pattern, s).group(2))
        self.clear_im = self.clear_im.convert("RGB")
        
        new_height = self.height_need
        ratio = new_height/self.clear_im.size[1]
        new_width = ceil(ratio*self.clear_im.size[0])
        
        if ratio != 1.0:
            if self.clear_im.size > (self.width_need, self.height_need):
                #self.im = self.im.resize((width, height), Image.ANTIALIAS) #downscaling
                self.clear_im = self.clear_im.resize((new_width, new_height), Image.ANTIALIAS)
            else:
                #self.im = self.im.resize((width, height), Image.BICUBIC)   #upscaling
                self.clear_im = self.clear_im.resize((new_width, new_height), Image.BICUBIC)
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
        
        width = self.im.size[0]
        height = self.im.size[1]
        print(width - self.delta_right, " crop")
        self.im = self.im.crop((floor(self.delta_left), 0,floor(self.delta_left) + self.width_need,height))
        self.putImage()
        self.checkActive()
    
    def setgrayscaleImage(self):
        
        width,height = self.clear_im.size
        for i in range(width):
            for j in range(height):
                print("Still here")
                r,g,b = self.clear_im.getpixel((i,j))
                if r!= g != b: self.clear_im = self.clear_im.convert("LA"); self.clear_im = self.clear_im.convert("RGBA"); return
    
    def closeEvent(self, event):
        print(self.sender().objectName())
        if 'ok' in self.sender().objectName():
            print("OK clicked")
            return
        else:
            print("X clicked")
            self.im = None
    
    def checkActive(self):
        
        state = self.im.size[0] <= self.width_need
        self.push_crop.setEnabled(not state)
        self.push_ok.setEnabled(state)
        self.push_left.setEnabled(not state)
        self.push_right.setEnabled(not state)
    
    def initActions(self):
        
        self.push_left.clicked.connect(self.changeBlack)
        self.push_right.clicked.connect(self.changeBlack)
        self.push_crop.clicked.connect(self.cropImage)
        self.combo_versionKindle.currentIndexChanged.connect(self.openImage)
        self.push_ok.clicked.connect(self.close)
    
class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.im = ""
        self.initUI()
        self.retranslateUi()
        self.initStateUI(False)
        self.initActions()
        self.initVariables()
        
    def initVariables(self):
        
        self.language_translator = QtCore.QTranslator()
        self.text_x = 10
        self.text_y = 10
        self.text_color = None
        self.is_label = True
        self.is_text = False
        
        self.im = None
        self.clear_im = None
        self.label = Image.open(LABEL).convert("RGBA")
        self.file_path = None

    def initUI(self):
        
        self.centralWidget = QtGui.QWidget(self)
        self.MainLayout = QtGui.QHBoxLayout(self.centralWidget)
        #------------------------------------------
        self.LeftVertLayout = QtGui.QVBoxLayout()
        
        self.open_HorLayout = QtGui.QHBoxLayout()
        
        self.open_path = QtGui.QLineEdit(self.centralWidget)
        self.open_path.setMinimumSize(QtCore.QSize(0, 20))
        self.open_path.setReadOnly(True)
        self.button_open = QtGui.QPushButton(self.centralWidget)
        self.button_open.setMinimumSize(QtCore.QSize(0, 20))
        
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
        self.radio_White.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_White.setChecked(True)
        self.radio_Black = QtGui.QRadioButton(self.centralWidget)
        self.radio_Black.setMinimumSize(QtCore.QSize(0, 20))
        
        self.buttonGroup_TextColor.addButton(self.radio_White)
        self.textcolor_Grid.addWidget(self.radio_White, 1, 0, 1, 1)
        self.buttonGroup_TextColor.addButton(self.radio_Black)
        self.textcolor_Grid.addWidget(self.radio_Black, 2, 0, 1, 1)
        
        self.label_textcolor = QtGui.QLabel(self.centralWidget)
        self.label_textcolor.setMinimumSize(QtCore.QSize(0, 20))
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
        self.label_wherePlace.setMinimumSize(QtCore.QSize(0, 20))
        self.label_wherePlace.setMaximumSize(QtCore.QSize(16777215, 20))
        
        self.placetext_Grid.addWidget(self.label_wherePlace, 2, 0, 1, 1)
        
        self.grid_radio_placetext = QtGui.QGridLayout()
        
        self.radio_leftupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftupper.setChecked(True)
        self.radio_leftupper.setObjectName("left_upper")
        self.buttonGroup_PlaceText = QtGui.QButtonGroup(self)
        self.buttonGroup_PlaceText.addButton(self.radio_leftupper)
        self.grid_radio_placetext.addWidget(self.radio_leftupper, 0, 0, 1, 1)
        
        self.radio_leftlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftlower.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftlower.setObjectName("left_lower")
        self.buttonGroup_PlaceText.addButton(self.radio_leftlower)
        self.grid_radio_placetext.addWidget(self.radio_leftlower, 1, 0, 1, 1)   
        
        self.radio_rightupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightupper.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_rightupper.setObjectName("right_upper")
        self.buttonGroup_PlaceText.addButton(self.radio_rightupper)
        self.grid_radio_placetext.addWidget(self.radio_rightupper, 0, 1, 1, 1)
        
        self.radio_rightlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightlower.setMinimumSize(QtCore.QSize(0, 20))
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
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.slide_HorLayout.addItem(spacerItem3)
        self.LeftVertLayout.addLayout(self.slide_HorLayout)
        #------------------------------------------
        self.button_create = QtGui.QPushButton(self.centralWidget)
        self.button_create.setMinimumSize(QtCore.QSize(0, 20))
        self.LeftVertLayout.addWidget(self.button_create)
        #------------------------------------------
        self.MainLayout.addLayout(self.LeftVertLayout)
        self.RightVertLayout = QtGui.QVBoxLayout()
        
        self.label_image = QtGui.QLabel(self.centralWidget)
        self.label_image.setMinimumSize(QtCore.QSize(300, 400))
        self.label_image.setMaximumSize(QtCore.QSize(300, 400))
        self.label_image.setStyleSheet(_fromUtf8("border-style: solid;\n"
                                                 "border-width: 1px;\n"
                                                 "border-color: white;"))
        self.RightVertLayout.addWidget(self.label_image)
        #------------------------------------------
        self.grid_arrows = QtGui.QGridLayout()
        self.button_up = QtGui.QPushButton(self.centralWidget)
        self.button_up.setMinimumSize(QtCore.QSize(35, 35))
        self.button_up.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_up, 0, 1, 1, 1, QtCore.Qt.AlignBottom)
        self.button_left = QtGui.QPushButton(self.centralWidget)
        self.button_left.setMinimumSize(QtCore.QSize(35, 35))
        self.button_left.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_left, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.button_right = QtGui.QPushButton(self.centralWidget)
        self.button_right.setMinimumSize(QtCore.QSize(35, 35))
        self.button_right.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_right, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.button_down = QtGui.QPushButton(self.centralWidget)
        self.button_down.setMinimumSize(QtCore.QSize(35, 35))
        self.button_down.setMaximumSize(QtCore.QSize(35, 35))
        self.grid_arrows.addWidget(self.button_down, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.RightVertLayout.addLayout(self.grid_arrows)
        #------------------------------------------
        self.MainLayout.addLayout(self.RightVertLayout)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 648, 20))
        self.menuMain = QtGui.QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.action_Exit = QtGui.QAction(self)
        self.menuMain.addAction(self.action_Exit)
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
        self.menuBar.addAction(self.menuMain.menuAction())
        
        self.centerUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle("Kindle ScreenSaver Creator")
        
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
        
        self.check_slide.setText("Slide and release the power to wake")
        self.button_create.setText(self.tr("Create"))
        #self.label_image.setText("<html><head/><body><p align=\"center\"><br/></p></body></html>")
        self.button_up.setText("ᐃ")
        self.button_up.setShortcut("Up")
        self.button_left.setText("ᐊ")
        self.button_left.setShortcut("Left")
        self.button_right.setText("ᐅ")
        self.button_right.setShortcut("Right")
        self.button_down.setText("ᐁ")
        self.button_down.setShortcut("Down")
        self.menuMain.setTitle(self.tr("Main"))
        self.action_Exit.setText(self.tr("Exit"))
        self.menuLanguage.setTitle(self.tr("Language"))
        self.actionEnglish.setText("English")
        self.actionRussian.setText("Русский")
        self.actionUkrainian.setText("Українська")
    
    def centerUI(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def initStateUI(self, enabled):
                      
        self.name.setEnabled(enabled)
        self.surname.setEnabled(enabled)
        self.radio_leftlower.setEnabled(enabled)
        self.radio_leftupper.setEnabled(enabled)
        self.radio_rightlower.setEnabled(enabled)
        self.radio_rightupper.setEnabled(enabled)
        self.radio_Black.setEnabled(enabled)
        self.radio_White.setEnabled(enabled)
        self.check_slide.setEnabled(enabled)
        self.button_left.setEnabled(enabled)
        self.button_right.setEnabled(enabled)
        self.button_up.setEnabled(enabled)
        self.button_down.setEnabled(enabled)
        self.button_create.setEnabled(enabled)

    def putImage(self):
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.im))
        pixmap = pixmap.scaled(self.label_image.size())
        self.label_image.setPixmap(pixmap)
    
    
    
    def redraw(self):
        
        self.is_label = self.check_slide.isChecked()
        self.is_text = self.name.text() or self.surname.text()
        self.pasteImage()
        
        
        if self.is_label:
            self.im.paste(self.label, (0, self.im.size[1] - self.label.size[1]), mask= self.label)
        
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
        default_move = {"ᐃ"  : (0, -10),
                                                "ᐊ" : (-10, 0),
                                                "ᐅ" : (10, 0),
                                                "ᐁ": (0, 10)}
        self.text_x += default_move[self.sender().text()][0]
        self.text_y += default_move[self.sender().text()][1]
        self.redraw()
    
    def placeText(self, corner):
        default_coord = {"left_upper" : (10, 10),
                          "left_lower" : (10, self.im.size[1]),
                          "right_upper" : (self.im.size[0], 10),
                          "right_lower" : (self.im.size[0], self.im.size[1])}
        
        self.text_x, self.text_y = default_coord[self.sender().objectName()]
        self.redraw()
    
    def correctText(self, font, size):
        
        font = font
        size_x = self.im.size[0] - 10
        size_y = self.im.size[1] - 10 - self.label.size[1]
        text_height = 0
        text_lenght = 0
        name = self.name.text()
        surname = self.surname.text()
        
        if self.text_x < 10:
            self.text_x = 10
        if self.text_y < 10:
            self.text_y = 10
        
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
        self.file_path = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if self.file_path == '':
            return
        if path.split(self.file_path)[-1].split('.')[1].lower() not in IMAGE_FORMATS:
            self.statusBar.showMessage(self.tr('No image'))
            return
        
        #place for dialog crop
        ui = CropDialog(self.file_path)      
        ui.exec_()
        try:
            self.clear_im = Image.new(size=ui.im.size, mode=ui.im.mode)
            self.clear_im.paste(ui.im)
        except:
            print("Got exception")
            return
        
        #end of place for dialog crop
        if not self.name.isEnabled():
            self.name.setEnabled(True)
        if self.clear_im.size[0] <= 600:
            self.check_slide.setEnabled(True)
            self.check_slide.setChecked(True)
        else:
            if self.check_slide.isEnabled():
                self.check_slide.setEnabled(False)
            if self.check_slide.isChecked():
                self.check_slide.setChecked(False)
        
        
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
        self.text_x = 10
        self.text_y = 10
        self.redraw()
        
        self.open_path.setText(self.file_path)
        self.statusBar.showMessage(self.tr("Opened file"))
    
    def pasteImage(self):
        
        self.im = Image.new(size=self.clear_im.size, mode=self.clear_im.mode)
        self.im.paste(self.clear_im)
        
    def saveImage(self):
        
        default = self.tr(self.tr("Sample"))
        name = ""
        self.redraw()
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
        if not enabled:
            self.surname.setText("")
            
    def initActions(self):
        
        self.action_Exit.triggered.connect(self.close)
        self.check_slide.stateChanged.connect(self.redraw)
        self.button_open.clicked.connect(self.openImage)
        self.button_create.clicked.connect(self.saveImage)
        self.name.textChanged.connect(self.redraw)
        self.name.textChanged.connect(self.surnameState)
        self.surname.textChanged.connect(self.redraw)
        self.radio_Black.clicked.connect(self.redraw)
        self.radio_White.clicked.connect(self.redraw)
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
    
    def translateUI(self):
        
        app = QtGui.QApplication.instance()
        language_translator = QtCore.QTranslator()
        if "en" in self.sender().objectName():
            print("English")
            pass
        else:
            print("Rus or Ukr")
            path = self.sender().objectName() + ".qm"
            language_translator.load(path)
        app.installTranslator(language_translator)
        self.retranslateUi()
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
    
def test():
    r = None
    print(r)
if __name__ == '__main__':
    main()
    #test()
