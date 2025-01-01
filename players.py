from PyQt6.QtWidgets import QMessageBox, QDialog, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPixmap
import os
import shutil

class PyVideoPlayer(QDialog):
    def __init__(self, root, fname=None):
        super().__init__(root)
        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Видеоплеер')
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.videowidget = QVideoWidget()
        self.player.setVideoOutput(self.videowidget)
        self.player.setAudioOutput(self.audio)
        self.cur = False  # текущее состояние ролика
        self.load_UI()
        self.root = root
        self.default_name = fname

    def load_UI(self):
        self.openBtn = QPushButton("Открыть")
        self.openBtn.clicked.connect(self.open)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        hbox = QHBoxLayout()
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)
        vbox = QVBoxLayout()
        vbox.addWidget(self.videowidget)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def open(self):
        '''
        запуск видео
        '''
        if self.default_name is None:
            file, _ = QFileDialog.getOpenFileName(self, 'c:\\', '', " Video files (*.mp4 *.mpeg *.mov *.avi)")
            filename = f'media/{self.root.root.fname}/{os.path.basename(file)}'
            shutil.copy2(os.path.abspath(file),filename)
        else:
            filename = self.default_name
        try:
            self.player.setSource(QUrl.fromLocalFile(filename))
            self.playBtn.setEnabled(True)
            self.root.fname = filename
        except Exception:
            self.root.fname = ''
            mb = QMessageBox()
            mb.setText('Недопустимое имя файла! Возможно, он удален или перемещен.')

    def play(self):
        '''
        пауза
        '''
        self.cur = True if not self.cur else False
        if self.cur:
            self.player.play()
        else:
            self.player.pause()

    # обработка слайдера
    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)


class PyAudioPlayer(QDialog):
    def __init__(self, root, fname=None):
        super().__init__(root)
        self.setWindowTitle('Аудиоплеер')
        self.setGeometry(200, 200, 700, 400)
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.cur = False
        self.load_UI()
        self.root = root
        self.default_name = fname

    def load_UI(self):
        self.openBtn = QPushButton("Открыть")
        self.openBtn.clicked.connect(self.open)
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        hbox = QHBoxLayout()
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)
        self.setLayout(hbox)

    def open(self):
        '''
        запуск аудио
        '''
        if self.default_name is None:
            file, _ = QFileDialog.getOpenFileName(self, 'c:\\', '', " Audio files (*.mp3)")
            filename = f'media/{self.root.root.fname}/{os.path.basename(file)}'
            shutil.copy2(os.path.abspath(file),filename)
        else:
            filename = self.default_name
        try:
            self.player.setSource(QUrl.fromLocalFile(filename))
            self.playBtn.setEnabled(True)
            self.root.fname = filename
        except Exception:
            self.root.fname = ''
            mb = QMessageBox()
            mb.setText('Недопустимое имя файла! Возможно, он удален или перемещен.')
    def play(self):
        '''
        пауза
        '''
        self.cur = True if not self.cur else False
        if self.cur:
            self.player.play()
        else:
            self.player.pause()

    # обработка слайдера
    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

class PyImagePlayer(QDialog):
    def __init__(self, root, fname=None):
        super().__init__(root)
        self.setWindowTitle('Просмотр изображений')
        self.setGeometry(200, 200, 700, 400)
        self.img_btn = QPushButton("Открыть картинку")
        self.img_btn.clicked.connect(self.open)
        self.fname = ''
        self.label = QLabel()
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.img_btn)
        self.setLayout(vbox)
        self.root = root
        self.default_name = fname
    def open(self):
        '''
        открытие картинки
        '''
        if self.default_name is None:
            file, _ = QFileDialog.getOpenFileName(self, 'c:\\', '', "Image files (*.jpg *.jpeg *.gif *.png)")
            filename = f'media/{self.root.root.fname}/{os.path.basename(file)}'
            shutil.copy2(os.path.abspath(file), filename)
        else:
            filename = self.default_name
        try:
            self.im = QPixmap(filename).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
            self.root.fname = filename
            self.label.setPixmap(self.im)
        except Exception:
            self.root.fname = ''
            mb = QMessageBox()
            mb.setText('Недопустимое имя файла! Возможно, он удален или перемещен.')