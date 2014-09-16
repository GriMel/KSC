from PyQt4 import QtGui, QtCore
from PIL import Image, ImageDraw, ImageFont, ImageQt
import sys
import re

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
    
LABEL = "/home/grimel/Desktop/label.png"
SAVE_PATH = "/output/"
FONT = "/home/grimel/Desktop/resources/DroidSerif-Bold.ttf"

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.im = ""
        self.initUI()
        self.retranslateUi()
        self.setState(False)
        self.initActions()
        self.initVariables()
        
    def initVariables(self):
        
        self.text_x = 10
        self.text_y = 10
        self.max_x = 600
        self.max_y = 800
        self.text_color = None
        self.is_label = True
        self.is_text = False
        self.pic = None
        self.clear_pic = None
        self.label = Image.open(LABEL).convert("RGBA")
        self.file_path = None
        self.default_coord = {"Left Upper" : (10, 10),
                              "Left Lower" : (10, 650),
                              "Right Upper" : (500, 10),
                              "Right Lower" : (500, 650)}
        self.default_move = {"ᐃ"  : (0, -10),
                                                          "ᐊ" : (-10, 0),
                                                          "ᐅ" : (10, 0),
                                                          "ᐁ": (0, 10)}
    def initUI(self):
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        
        self.MainLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.MainLayout.setObjectName("MainLayout")
        
        self.LeftVertLayout = QtGui.QVBoxLayout()
        self.LeftVertLayout.setObjectName("LeftVertLayout")
        
        self.open_HorLayout = QtGui.QHBoxLayout()
        self.open_HorLayout.setObjectName("open_HorLayout")
        self.open_path = QtGui.QLineEdit(self.centralWidget)
        self.open_path.setMinimumSize(QtCore.QSize(0, 20))
        self.open_path.setReadOnly(True)
        self.open_path.setObjectName("open_path")
        self.button_open = QtGui.QPushButton(self.centralWidget)
        self.button_open.setMinimumSize(QtCore.QSize(0, 20))
        self.button_open.setObjectName("button_open")
        
        self.open_HorLayout.addWidget(self.open_path)
        self.open_HorLayout.addWidget(self.button_open)
        self.LeftVertLayout.addLayout(self.open_HorLayout)
        
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.LeftVertLayout.addItem(spacerItem)
        
        self.line_1 = QtGui.QFrame(self.centralWidget)
        self.line_1.setFrameShape(QtGui.QFrame.HLine)
        self.line_1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.LeftVertLayout.addWidget(self.line_1)
        
        self.name_Grid = QtGui.QGridLayout()
        self.name_Grid.setObjectName(_fromUtf8("name_Grid"))
        self.label_name = QtGui.QLabel(self.centralWidget)
        self.label_name.setObjectName(_fromUtf8("label_name"))
        self.name_Grid.addWidget(self.label_name, 0, 0, 1, 1)
        
        self.label_surname = QtGui.QLabel(self.centralWidget)
        self.label_surname.setObjectName(_fromUtf8("label_surname"))
        self.name_Grid.addWidget(self.label_surname, 1, 0, 1, 1)
        self.name = QtGui.QLineEdit(self.centralWidget)
        #self.name.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Russia))
        self.name.setObjectName(_fromUtf8("name"))
        self.name_Grid.addWidget(self.name, 0, 1, 1, 1)
        
        self.surname = QtGui.QLineEdit(self.centralWidget)
        #self.surname.setLocale(QtCore.QLocale(QtCore.QLocale.Russian, QtCore.QLocale.Russia))
        self.surname.setObjectName(_fromUtf8("surname"))
        self.name_Grid.addWidget(self.surname, 1, 1, 1, 1)
        self.LeftVertLayout.addLayout(self.name_Grid)
        
        self.line_2 = QtGui.QFrame(self.centralWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.LeftVertLayout.addWidget(self.line_2)
        
        self.textcolor_Grid = QtGui.QGridLayout()
        self.textcolor_Grid.setObjectName(_fromUtf8("textcolor_Grid"))
        self.radio_White = QtGui.QRadioButton(self.centralWidget)
        self.radio_White.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_White.setObjectName(_fromUtf8("radio_White"))
        self.buttonGroup_TextColor = QtGui.QButtonGroup(self)
        self.buttonGroup_TextColor.setObjectName(_fromUtf8("buttonGroup_TextColor"))
        
        self.buttonGroup_TextColor.addButton(self.radio_White)
        self.textcolor_Grid.addWidget(self.radio_White, 1, 0, 1, 1)
        
        self.radio_Black = QtGui.QRadioButton(self.centralWidget)
        self.radio_Black.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_Black.setObjectName(_fromUtf8("radio_Black"))
        
        self.buttonGroup_TextColor.addButton(self.radio_Black)
        self.textcolor_Grid.addWidget(self.radio_Black, 2, 0, 1, 1)
        
        self.label_textcolor = QtGui.QLabel(self.centralWidget)
        self.label_textcolor.setMinimumSize(QtCore.QSize(0, 20))
        self.label_textcolor.setObjectName(_fromUtf8("label_textcolor"))
        self.textcolor_Grid.addWidget(self.label_textcolor, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.textcolor_Grid.addItem(spacerItem2, 0, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.textcolor_Grid)
        self.line_3 = QtGui.QFrame(self.centralWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.LeftVertLayout.addWidget(self.line_3)
        self.placetext_Grid = QtGui.QGridLayout()
        self.placetext_Grid.setObjectName(_fromUtf8("placetext_Grid"))
        self.label_wherePlace = QtGui.QLabel(self.centralWidget)
        self.label_wherePlace.setMinimumSize(QtCore.QSize(0, 20))
        self.label_wherePlace.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_wherePlace.setObjectName(_fromUtf8("label_wherePlace"))
        self.placetext_Grid.addWidget(self.label_wherePlace, 2, 0, 1, 1)
        self.grid_radio = QtGui.QGridLayout()
        self.grid_radio.setObjectName(_fromUtf8("grid_radio"))
        self.radio_leftupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftupper.setChecked(True)
        self.radio_leftupper.setObjectName(_fromUtf8("radio_leftupper"))
        self.buttonGroup_PlaceText = QtGui.QButtonGroup(self)
        self.buttonGroup_PlaceText.setObjectName(_fromUtf8("buttonGroup_PlaceText"))
        self.buttonGroup_PlaceText.addButton(self.radio_leftupper)
        self.grid_radio.addWidget(self.radio_leftupper, 0, 0, 1, 1)
        self.radio_rightlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightlower.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightlower.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_rightlower.setObjectName(_fromUtf8("radio_rightlower"))
        self.buttonGroup_PlaceText.addButton(self.radio_rightlower)
        self.grid_radio.addWidget(self.radio_rightlower, 1, 1, 1, 1)
        self.radio_leftlower = QtGui.QRadioButton(self.centralWidget)
        self.radio_leftlower.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_leftlower.setObjectName(_fromUtf8("radio_leftlower"))
        self.buttonGroup_PlaceText.addButton(self.radio_leftlower)
        self.grid_radio.addWidget(self.radio_leftlower, 1, 0, 1, 1)
        self.radio_rightupper = QtGui.QRadioButton(self.centralWidget)
        self.radio_rightupper.setMinimumSize(QtCore.QSize(0, 20))
        self.radio_rightupper.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_rightupper.setObjectName(_fromUtf8("radio_rightupper"))
        self.buttonGroup_PlaceText.addButton(self.radio_rightupper)
        self.grid_radio.addWidget(self.radio_rightupper, 0, 1, 1, 1)
        self.placetext_Grid.addLayout(self.grid_radio, 3, 0, 1, 1)
        self.LeftVertLayout.addLayout(self.placetext_Grid)
        self.line_4 = QtGui.QFrame(self.centralWidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.LeftVertLayout.addWidget(self.line_4)
        self.version_HorLayout = QtGui.QHBoxLayout()
        self.version_HorLayout.setObjectName(_fromUtf8("version_HorLayout"))
        self.label_versionKindle = QtGui.QLabel(self.centralWidget)
        self.label_versionKindle.setMinimumSize(QtCore.QSize(0, 20))
        self.label_versionKindle.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_versionKindle.setObjectName(_fromUtf8("label_versionKindle"))
        self.version_HorLayout.addWidget(self.label_versionKindle)
        self.combo_versionKindle = QtGui.QComboBox(self.centralWidget)
        self.combo_versionKindle.setMinimumSize(QtCore.QSize(0, 20))
        self.combo_versionKindle.setObjectName(_fromUtf8("combo_versionKindle"))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.combo_versionKindle.addItem(_fromUtf8(""))
        self.version_HorLayout.addWidget(self.combo_versionKindle)
        self.LeftVertLayout.addLayout(self.version_HorLayout)
        self.line_5 = QtGui.QFrame(self.centralWidget)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.LeftVertLayout.addWidget(self.line_5)
        self.slide_HorLayout = QtGui.QHBoxLayout()
        self.slide_HorLayout.setObjectName(_fromUtf8("slide_HorLayout"))
        self.check_slide = QtGui.QCheckBox(self.centralWidget)
        self.check_slide.setChecked(True)
        self.check_slide.setObjectName(_fromUtf8("check_slide"))
        self.slide_HorLayout.addWidget(self.check_slide)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.slide_HorLayout.addItem(spacerItem3)
        self.LeftVertLayout.addLayout(self.slide_HorLayout)
        self.button_create = QtGui.QPushButton(self.centralWidget)
        self.button_create.setMinimumSize(QtCore.QSize(0, 20))
        self.button_create.setObjectName(_fromUtf8("button_create"))
        self.LeftVertLayout.addWidget(self.button_create)
        self.MainLayout.addLayout(self.LeftVertLayout)
        self.RightVertLayout = QtGui.QVBoxLayout()
        self.RightVertLayout.setObjectName(_fromUtf8("RightVertLayout"))
        self.picture_label = QtGui.QLabel(self.centralWidget)
        self.picture_label.setMinimumSize(QtCore.QSize(300, 400))
        self.picture_label.setMaximumSize(QtCore.QSize(300, 400))
        self.picture_label.setStyleSheet(_fromUtf8("border-style: solid;\n"
                                                   "border-width: 1px;\n"
                                                   "border-color: white;"))
        self.picture_label.setObjectName(_fromUtf8("picture_label"))
        self.RightVertLayout.addWidget(self.picture_label)
        self.grid_arrows = QtGui.QGridLayout()
        self.grid_arrows.setObjectName(_fromUtf8("grid_arrows"))
        self.button_up = QtGui.QPushButton(self.centralWidget)
        self.button_up.setMinimumSize(QtCore.QSize(35, 35))
        self.button_up.setMaximumSize(QtCore.QSize(35, 35))
        self.button_up.setObjectName(_fromUtf8("button_up"))
        self.grid_arrows.addWidget(self.button_up, 0, 1, 1, 1, QtCore.Qt.AlignBottom)
        self.button_left = QtGui.QPushButton(self.centralWidget)
        self.button_left.setMinimumSize(QtCore.QSize(35, 35))
        self.button_left.setMaximumSize(QtCore.QSize(35, 35))
        self.button_left.setObjectName(_fromUtf8("button_left"))
        self.grid_arrows.addWidget(self.button_left, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.button_right = QtGui.QPushButton(self.centralWidget)
        self.button_right.setMinimumSize(QtCore.QSize(35, 35))
        self.button_right.setMaximumSize(QtCore.QSize(35, 35))
        self.button_right.setObjectName(_fromUtf8("button_right"))
        self.grid_arrows.addWidget(self.button_right, 1, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.button_down = QtGui.QPushButton(self.centralWidget)
        self.button_down.setMinimumSize(QtCore.QSize(35, 35))
        self.button_down.setMaximumSize(QtCore.QSize(35, 35))
        self.button_down.setObjectName(_fromUtf8("button_down"))
        self.grid_arrows.addWidget(self.button_down, 2, 1, 1, 1, QtCore.Qt.AlignTop)
        self.RightVertLayout.addLayout(self.grid_arrows)
        self.MainLayout.addLayout(self.RightVertLayout)
        
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 648, 20))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuMain = QtGui.QMenu(self.menuBar)
        self.menuMain.setObjectName(_fromUtf8("menuMain"))
        self.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.setStatusBar(self.statusBar)
        self.action_Exit = QtGui.QAction(self)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.menuMain.addAction(self.action_Exit)
        self.menuBar.addAction(self.menuMain.menuAction())

        
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle("MainWindow")
        self.button_open.setText("Open...")
        self.label_name.setText("Name")
        self.label_surname.setText("Surname")
        self.radio_White.setText("White")
        self.radio_Black.setText("Black")
        self.label_textcolor.setText("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Text color</span></p></body></html>")
        self.label_wherePlace.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Where to place text</span></p></body></html>")
        self.radio_leftupper.setText("Left Upper")
        self.radio_rightlower.setText("Right Lower")
        self.radio_leftlower.setText("Left Lower")
        self.radio_rightupper.setText("Right Upper")
        self.label_versionKindle.setText("Version of Kindle")
        self.combo_versionKindle.setItemText(0, "Kindle 3, 4, 5, Touch (800 x 600)")
        self.combo_versionKindle.setItemText(1, "Kindle DX (1200 x 824)")
        self.combo_versionKindle.setItemText(2, "Kindle Paperwhite (1024 x 768)")
        
        self.check_slide.setText("Slide and release the power to wake")
        self.button_create.setText("Create")
        self.picture_label.setText("<html><head/><body><p align=\"center\"><br/></p></body></html>")
        self.button_up.setText("ᐃ")
        self.button_up.setShortcut("Up")
        self.button_left.setText("ᐊ")
        self.button_left.setShortcut("Left")
        self.button_right.setText("ᐅ")
        self.button_right.setShortcut("Right")
        self.button_down.setText("ᐁ")
        self.button_down.setShortcut("Down")
        self.menuMain.setTitle("Main")
        self.action_Exit.setText("&Exit")
        
    def setState(self, enabled):
                      
        self.name.setEnabled(enabled)
        self.surname.setEnabled(enabled)
        self.radio_leftlower.setEnabled(enabled)
        self.radio_leftupper.setEnabled(enabled)
        self.radio_rightlower.setEnabled(enabled)
        self.radio_rightupper.setEnabled(enabled)
        self.radio_Black.setEnabled(enabled)
        self.radio_White.setEnabled(enabled)
        self.combo_versionKindle.setEnabled(enabled)
        self.check_slide.setEnabled(enabled)
        self.button_left.setEnabled(enabled)
        self.button_right.setEnabled(enabled)
        self.button_up.setEnabled(enabled)
        self.button_down.setEnabled(enabled)

    def putImage(self):
        
        pixmap = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.pic))
        pixmap = pixmap.scaled(self.picture_label.size())
        self.picture_label.setPixmap(pixmap)
    
    def openImage(self):
        try:
            self.file_path = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        except:
            self.statusBar.showMessage('Wrong file name')
        
        self.setState(enabled=True)
        self.redraw()
        
        self.open_path.setText(self.file_path)
        self.statusBar.showMessage("Opened file")
    
    def redraw(self):
        
        self.is_label = self.check_slide.isChecked()
        self.is_text = bool(self.name.text() or self.surname.text())
        self.pic = Image.open(self.file_path)
        self.pic = self.pic.convert("RGBA")
        self.pic = self.pic.resize((600, 800))
        if self.is_label:
            self.pic.paste(self.label, (0, 746), mask= self.label)
        
        if self.is_text:
            if self.radio_Black.isChecked():
                self.text_color = "Black"
            else:
                self.text_color = "White"
            draw = ImageDraw.Draw(self.pic)
            font = ImageFont.truetype('/home/grimel/Desktop/resources/DroidSerif-Bold.ttf', 30)
            
            
            #----------block for text, which goes within frame
            if len(self.name.text()) > len(self.surname.text()):
                dx = font.getsize(self.name.text())[0]
            else:
                dx = font.getsize(self.surname.text())[0]
            print(self.text_x, dx, self.pic.size[0])
            if self.text_x + dx > self.pic.size[0]:
                self.text_x = self.text_x - (self.pic.size[0]-self.text_x + dx)
            #--------------------------------------------------------
            
            #draw name
            draw.text((self.text_x, self.text_y), self.name.text(), self.text_color, font=font)
            #draw surname
            draw.text((self.text_x, self.text_y + 30), self.surname.text(), self.text_color, font=font)
        
        self.putImage()
        
    def moveText(self):
        
        self.text_x += self.default_move[self.sender().text()][0]
        self.text_y += self.default_move[self.sender().text()][1]
        self.redraw()
    
    def placeText(self, corner):
        
        self.text_x, self.text_y = self.default_coord[self.sender().text()]
        self.redraw()
        
    def saveImage(self):
        
        self.resizeImage()
        self.pic.save("/home/grimel/Desktop/Some.png")
        self.statusBar.showMessage("File created!")
    
    def resizeImage(self):
        s = self.combo_versionKindle.currentText()
        pattern = re.compile(r"(\d*).x.(\d*)")
        height = int(re.search(pattern, s).group(1))
        width = int(re.search(pattern, s).group(2))
        self.pic = self.pic.convert("RGB")
        if height > self.pic.size[1]:
            self.pic = self.pic.resize((width, height), Image.BICUBIC)
        else:
            self.pic = self.pic.resize((width, height), Image.ANTIALIAS)
        self.pic = self.pic.convert("RGBA")
            
    def initActions(self):
        
        self.check_slide.stateChanged.connect(self.redraw)
        self.button_open.clicked.connect(self.openImage)
        self.button_create.clicked.connect(self.saveImage)
        self.name.textChanged.connect(self.redraw)
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
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
    
def test():
    pass
    
if __name__ == '__main__':
    main()
    #test()
