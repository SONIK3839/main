from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog 

import os 
from PIL import Image, ImageFilter 
from PyQt5.QtGui import QPixmap

app = QApplication([])

'''Создание окнв'''
win = QWidget()
win.resize(900, 600)
win.setWindowTitle('Easy Editor')

''' Создание кнопок редактирования'''
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_bw = QPushButton('Черно-белое')
btn_sharp = QPushButton('Резскость')
btn_flip = QPushButton('Зеркало')

'''Создание виджетов'''
btn_dir = QPushButton('Папка')
lb_image = QLabel('Картинка')
lw_files = QListWidget()

'''Направляющие'''
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_flip)

col2 = QVBoxLayout()
col2.addWidget(lb_image)
col2.addLayout(row_tools)

col1 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

row = QHBoxLayout()
row.addLayout(col1, 20)
row.addLayout(col2, 80)

'''Отображение слоя на главном окне'''
win.setLayout(row)

'''Фильтр для разрешеных расширений'''
def filter(fiels: list, extentions: list):
    resualt = []
    for filename in fiels:
        for ext in extentions:
        
        
            if filename.endswith(ext):
                resualt.append(filename)
    return resualt

'''Выбор директории'''
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

'''Показ файлов картинок'''
def showFilenamesList():
    extentions = ['.jpg', '.png', '.gif', '.bmp', 'jpeg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extentions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)






class imageProcesor():
    def __init__(self):
        self.immage = None
        self.filename = None
        self.dir = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        self.image = Image.open(os.path.join(self.dir, self.filename))

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()



    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        self.showImage(os.path.join(self.dir, self.save_dir, self.filename))



    
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path)) or not(os.path.isdir(path)):
            os.mkdir(path)
        self.image.save(os.path.join(path, self.filename))

'''Класс для работы с картинкой'''
workimage = imageProcesor()

'''Подключение функций к кнопкам'''
btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)


'''Функция дляклтка по выбраной катинки'''
def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        workimage.showImage(os.path.join(workdir, filename))


'''dvms fj pjf dpjf'''
lw_files.currentRowChanged.connect(showChosenImage)

'''Отображение окна и зауск приложения'''
win.show()
app.exec_()
