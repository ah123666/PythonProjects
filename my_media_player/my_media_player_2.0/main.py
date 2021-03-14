from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class myVideoWidget(QVideoWidget):

    doubleClickedItem = pyqtSignal(str)  # 创建双击信号
    singleClickedItem = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, QMouseEvent):  # 双击事件
        self.doubleClickedItem.emit("double clicked")

    def mousePressEvent(self, QMouseEvent):
        self.singleClickedItem.emit("single clicked")


class My_widget(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.font = QFont('Microsoft YaHei', 8)
        self.theme = 0
        self.initUI()
        self.change_theme()

    def initUI(self):
        self.setWindowTitle('media_player')
        self.resize(800, 600)

        self.status = self.statusBar()
        self.status.showMessage('welcome to this media player!')
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        setting_menu = menubar.addMenu('Setting')
        file_act = QAction('Add File', self)
        folder_act = QAction('Add Folder', self)
        theme_act = QAction('Change Theme', self)

        file_act.setShortcut('Ctrl+O')
        folder_act.setShortcut('Ctrl+D')
        theme_act.setShortcut('Ctrl+T')

        file_menu.addAction(file_act)
        file_menu.addAction(folder_act)
        setting_menu.addAction(theme_act)

        file_act.triggered.connect(self.open_file)
        folder_act.triggered.connect(self.open_folder)
        theme_act.triggered.connect(self.change_theme)

        self.player = QMediaPlayer()
        self.play_list = QMediaPlaylist()
        self.play_list.setPlaybackMode(2)
        self.video_widget = myVideoWidget()
        self.video_widget.setStyleSheet('background-color: gray')
        # self.video_widget.setStyleSheet('border-image : url(2.png)')
        self.picture_widget = QLabel()
        self.picture_widget.setScaledContents(True)
        self.picture_widget.setPixmap(QPixmap('2.png').scaled(self.picture_widget.width(), self.picture_widget.height()))
        self.player.setVideoOutput(self.video_widget)
        self.player.setPlaylist(self.play_list)
        self.play_button = QPushButton('play')
        self.pause_button = QPushButton('pause')
        self.next_button = QPushButton('next')
        self.last_button = QPushButton('last')
        self.quit_button = QPushButton('quit')

        self.play_slider = QSlider(Qt.Horizontal, self)
        self.play_slider.setRange(0, 0)
        self.play_slider.setSingleStep(1)

        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setSingleStep(1)

        self.list_widget = QListWidget()
        self.list_widget.setFont(self.font)

        self.play_label_1 = QLabel('00:00:00')
        self.play_label_2 = QLabel('00:00:00')
        self.volume_label = QLabel(' 50')
        self.volume_text = QLabel('volume')

        layout_h_1 = QHBoxLayout()
        layout_h_2 = QHBoxLayout()
        layout_h_3 = QHBoxLayout()
        layout_v = QVBoxLayout()
        self.show_layout = QHBoxLayout()
        self.show_layout.addWidget(self.picture_widget)

        layout_h_1.addWidget(self.play_label_1)
        layout_h_1.addWidget(self.play_slider)
        layout_h_1.addWidget(self.play_label_2)

        layout_h_2.addWidget(self.last_button)
        layout_h_2.addWidget(self.play_button)
        layout_h_2.addWidget(self.pause_button)
        layout_h_2.addWidget(self.next_button)
        layout_h_2.addWidget(self.quit_button)
        layout_h_2.addWidget(self.volume_text)
        layout_h_2.addWidget(self.volume_slider)
        layout_h_2.addWidget(self.volume_label)
        layout_h_2.setStretch(0, 2)
        layout_h_2.setStretch(1, 2)
        layout_h_2.setStretch(2, 2)
        layout_h_2.setStretch(3, 2)
        layout_h_2.setStretch(4, 2)
        layout_h_2.setStretch(6, 3)

        layout_h_3.addLayout(self.show_layout)
        layout_h_3.addWidget(self.list_widget)
        layout_h_3.setStretch(0, 3)
        layout_h_3.setStretch(1, 1)
        layout_v.addLayout(layout_h_3)
        layout_v.addLayout(layout_h_2)
        layout_v.addLayout(layout_h_1)

        self.play_list.currentMediaChanged.connect(self.change_play_file)
        self.list_widget.itemDoubleClicked.connect(self.quickly_play)
        self.video_widget.doubleClickedItem.connect(self.screen_double_clicked)
        self.video_widget.singleClickedItem.connect(self.screen_single_clicked)
        self.last_button.clicked.connect(self.play_last)
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.next_button.clicked.connect(self.play_next)
        self.quit_button.clicked.connect(self.quit)
        self.player.durationChanged.connect(self.chage_slider_range)
        self.play_slider.sliderMoved.connect(self.change_play_position)
        self.player.positionChanged.connect(self.change_slider_value)
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.main_widget.setLayout(layout_v)

    def screen_double_clicked(self):
        if self.play_list.mediaCount() == 0:
            return
        self.play()
        if self.video_widget.isFullScreen():
            self.video_widget.setFullScreen(False)
        else:
            self.video_widget.setFullScreen(True)

    def screen_single_clicked(self):
        if self.play_list.mediaCount() == 0:
            return
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', '.', 'media files (*.mp3 *.flac *.ogg *.wav *.m4a *.mp4)')[0]
        if file_path == '':
            return
        file = QMediaContent(QUrl.fromLocalFile(file_path))
        self.list_widget.addItem(file_path.split('/')[-1])
        self.play_list.addMedia(file)
        self.status.showMessage("loading complete!", 5000)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'open folder')
        if folder is None:
            return
        it = QDirIterator(folder)
        it.next()
        while it.hasNext():
            if it.fileInfo().suffix() in ['mp3', 'flac', 'ogg', 'wav', 'm4a', 'mp4']:
                self.list_widget.addItem(it.fileInfo().fileName())
                self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
            it.next()
        if it.fileInfo().suffix() in ['mp3', 'flac', 'ogg', 'wav', 'm4a', 'mp4']:
            self.list_widget.addItem(it.fileInfo().fileName())
            self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))

    def play_last(self):
        if self.play_list.currentIndex() == 0:
            self.play_list.setCurrentIndex(self.play_list.mediaCount() - 1)
        else:
            self.play_list.previous()

    def play(self):
        if self.play_list.mediaCount() == 0:
            QMessageBox.warning(self, 'warning', 'No file to play!', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        self.play_list.setCurrentIndex(self.list_widget.currentRow())
        self.player.play()

    def pause(self):
        self.player.pause()

    def play_next(self):
        if self.play_list.currentIndex() == self.play_list.mediaCount() - 1:
            self.play_list.setCurrentIndex(0)
        else:
            self.play_list.next()

    def quit(self):
        reply = QMessageBox.question(self, 'message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()  # 退出应用程序
        else:
            return

    def quickly_play(self):
        if self.play_list.mediaCount() == 0:
            return
        else:
            self.play()

    def change_play_file(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            file_type = url.path().split('.')[-1]
            if file_type not in ['mp4']:
                self.show_layout.removeWidget(self.video_widget)
                self.video_widget.setVisible(False)
                self.picture_widget.setVisible(True)
                self.video_widget.setEnabled(False)
                self.picture_widget.setEnabled(True)
                self.show_layout.addWidget(self.picture_widget)
                self.picture_widget.setPixmap(QPixmap('2.png').scaled(self.picture_widget.width(), self.picture_widget.height()))
            else:
                self.show_layout.removeWidget(self.picture_widget)
                self.video_widget.setVisible(True)
                self.picture_widget.setVisible(False)
                self.video_widget.setEnabled(True)
                self.picture_widget.setEnabled(False)
                self.show_layout.addWidget(self.video_widget)
            self.status.showMessage(url.fileName())
            self.list_widget.setCurrentRow(self.play_list.currentIndex())

    def change_theme(self):
        app.setStyle("Fusion")
        palette = QPalette()
        # 黑暗主题
        if self.theme == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(235, 101, 54))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.theme = 1
        # 明亮主题
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.theme = 0

    def change_volume(self, value):
        self.volume_label.setText(str(value) if value == 100 else '{: 3}'.format(value))
        self.player.setVolume(value)

    def chage_slider_range(self, duration):
        self.play_slider.setRange(0, duration)
        total_time_s = int(duration / 1000)
        hour = total_time_s // 3600
        minute = total_time_s % 3600 // 60
        second = total_time_s % 3600 % 60
        time = [hour, minute, second]
        for i in range(len(time)):
            time[i] = '{:02}'.format(time[i])
        self.play_label_2.setText(':'.join(time))

    def change_slider_value(self, position):
        self.play_slider.setValue(position)
        total_time_s = int(position / 1000)
        hour = total_time_s // 3600
        minute = total_time_s % 3600 // 60
        second = total_time_s % 3600 % 60
        time = [hour, minute, second]
        for i in range(len(time)):
            time[i] = '{:02}'.format(time[i])
        self.play_label_1.setText(':'.join(time))

    def change_play_position(self, position):
        self.player.setPosition(position)  # 改变播放时刻


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = My_widget()
    main_win.show()
    sys.exit(app.exec_())
