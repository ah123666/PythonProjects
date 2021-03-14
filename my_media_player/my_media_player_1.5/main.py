from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os

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
        if not os.path.exists('./history'):
            os.makedirs('./history')
        self.list_file = './history/list.txt'
        self.song_bg = './images/song_bg.jpg'
        self.music_types = ['default', 'mp3', 'flac', 'ogg', 'wav', 'm4a']
        self.video_types = ['mp4', 'flv']
        self.file_types = self.music_types + self.video_types
        self.current_file_type = 'default'
        self.initUI()
        self.change_show_layout()
        self.change_theme()
        self.update_list()

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, '消息', '确定退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def initUI(self):
        self.setWindowTitle('媒体播放器')
        self.setWindowIcon(QIcon('./images/icon.ico'))
        self.resize(1000, 750)

        self.status = self.statusBar()
        self.status.showMessage('欢迎来到媒体播放器！')
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        setting_menu = menubar.addMenu('设置')
        file_act = QAction('添加文件', self)
        folder_act = QAction('添加文件夹', self)
        theme_act = QAction('切换主题', self)
        clear_act = QAction('清空列表', self)

        file_act.setShortcut('Ctrl+O')
        folder_act.setShortcut('Ctrl+D')
        theme_act.setShortcut('Ctrl+T')
        clear_act.setShortcut('Ctrl+Shift+C')

        file_menu.addAction(file_act)
        file_menu.addAction(folder_act)
        setting_menu.addAction(theme_act)
        setting_menu.addAction(clear_act)

        file_act.triggered.connect(self.open_file)
        folder_act.triggered.connect(self.open_folder)
        theme_act.triggered.connect(self.change_theme)
        clear_act.triggered.connect(self.clear_list)

        self.player = QMediaPlayer()
        self.play_list = QMediaPlaylist()
        self.play_list.setPlaybackMode(3)
        self.video_widget = myVideoWidget()
        self.video_widget.setStyleSheet('background-color: gray')
        self.picture_widget = QLabel()
        self.picture_widget.setScaledContents(True)
        self.player.setVideoOutput(self.video_widget)
        self.player.setPlaylist(self.play_list)
        self.play_button = QPushButton('播放')
        self.pause_button = QPushButton('暂停')
        self.next_button = QPushButton('下一个')
        self.last_button = QPushButton('上一个')
        self.play_mode_button = QComboBox()
        self.play_mode_button.addItem('单曲播放')
        self.play_mode_button.addItem('单曲循环')
        self.play_mode_button.addItem('列表播放')
        self.play_mode_button.addItem('列表循环')
        self.play_mode_button.addItem('列表随机')
        self.play_mode_button.setCurrentIndex(3)
        self.full_screen_button = QPushButton('全屏')
        self.delete_button = QPushButton('删除')
        self.quit_button = QPushButton('退出')

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
        self.volume_text = QLabel('音量')

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
        layout_h_2.addWidget(self.play_mode_button)
        layout_h_2.addWidget(self.full_screen_button)
        layout_h_2.addWidget(self.delete_button)
        layout_h_2.addWidget(self.quit_button)
        layout_h_2.addWidget(self.volume_text)
        layout_h_2.addWidget(self.volume_slider)
        layout_h_2.addWidget(self.volume_label)
        layout_h_2.setStretch(0, 2)
        layout_h_2.setStretch(1, 2)
        layout_h_2.setStretch(2, 2)
        layout_h_2.setStretch(3, 2)
        layout_h_2.setStretch(4, 2)
        layout_h_2.setStretch(5, 2)
        layout_h_2.setStretch(6, 2)
        layout_h_2.setStretch(7, 2)
        layout_h_2.setStretch(9, 3)

        layout_h_3.addLayout(self.show_layout)
        layout_h_3.addWidget(self.list_widget)
        layout_h_3.setStretch(0, 5)
        layout_h_3.setStretch(1, 2)
        layout_v.addLayout(layout_h_3)
        layout_v.addLayout(layout_h_2)
        layout_v.addLayout(layout_h_1)

        self.play_list.currentMediaChanged.connect(self.change_play_file)
        self.list_widget.itemDoubleClicked.connect(self.quickly_play)
        self.video_widget.doubleClickedItem.connect(self.video_double_clicked)
        self.video_widget.singleClickedItem.connect(self.video_single_clicked)
        self.last_button.clicked.connect(self.play_last)
        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.next_button.clicked.connect(self.play_next)
        self.play_mode_button.currentIndexChanged.connect(self.change_play_mode)
        self.full_screen_button.clicked.connect(self.full_screen)
        self.delete_button.clicked.connect(self.delete_current_file)
        self.quit_button.clicked.connect(self.quit)
        self.player.durationChanged.connect(self.chage_slider_range)
        self.play_slider.sliderMoved.connect(self.change_play_position)
        self.player.positionChanged.connect(self.change_slider_value)
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.main_widget.setLayout(layout_v)

    def change_show_layout(self):
        if self.current_file_type in self.music_types:
            self.show_layout.removeWidget(self.video_widget)
            self.show_layout.addWidget(self.picture_widget)
            self.picture_widget.setVisible(True)
            self.picture_widget.setEnabled(True)
            self.picture_widget.setPixmap(QPixmap(self.song_bg))
            self.video_widget.setVisible(False)
            self.video_widget.setEnabled(False)
        else:
            self.show_layout.removeWidget(self.picture_widget)
            self.show_layout.addWidget(self.video_widget)
            self.video_widget.setVisible(True)
            self.picture_widget.setVisible(False)
            self.video_widget.setEnabled(True)
            self.picture_widget.setEnabled(False)

    def update_list(self):
        try:
            read_file = open(self.list_file, 'r', encoding='utf-8')
            all_file_paths = read_file.readlines()
            read_file.close()
        except:
            return
        write_file = open(self.list_file, 'w', encoding='utf-8')
        for file_path in all_file_paths:
            file_path = file_path[:-1]
            if os.path.exists(file_path):
                self.list_widget.addItem(file_path.split('/')[-1])
                self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                write_file.write(file_path + '\n')
        write_file.close()

    def clear_list(self):
        reply = QMessageBox.question(self, '消息', '确定清空播放列表吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.current_file_type = 'default'
            self.change_show_layout()
            self.play_list.clear()
            self.list_widget.clear()
            if os.path.exists(self.list_file):
                with open(self.list_file, 'w', encoding='utf-8') as write_file:
                    pass

    def delete_current_file(self):
        if self.play_list.mediaCount() == 0:
            QMessageBox.warning(self, '警告', '没有待删除的文件！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '消息', '确定删除选中文件吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.play_list.removeMedia(self.list_widget.currentRow())
            self.list_widget.takeItem(self.list_widget.currentRow())
            if os.path.exists(self.list_file):
                all_files = []
                for i in range(self.list_widget.count()):
                    all_files.append(self.list_widget.item(i).text())
                with open(self.list_file, 'r', encoding='utf-8') as read_file:
                    all_file_paths = read_file.readlines()
                with open(self.list_file, 'w', encoding='utf-8') as write_file:
                    for i in range(len(all_file_paths)):
                        if all_file_paths[i][:-1].split('/')[-1] in all_files:
                            write_file.write(all_file_paths[i])

    def full_screen(self):
        if self.current_file_type in self.video_types:
            self.video_widget.setFullScreen(True)

    def video_double_clicked(self):
        if self.video_widget.isFullScreen():
            self.video_widget.setFullScreen(False)
        else:
            self.video_widget.setFullScreen(True)
        self.play()

    def video_single_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, '打开文件', '.', '媒体文件(*.' + ' *.'.join(self.file_types) + ')')[0]
        if file_path == '':
            self.status.showMessage('未选择文件！', 5000)
            return
        if os.path.exists(self.list_file):
            with open(self.list_file, 'r', encoding='utf-8') as read_file:
                all_file_paths = read_file.readlines()
                if file_path + '\n' in all_file_paths:
                    self.status.showMessage('已存在相同文件！', 5000)
                    return
            with open(self.list_file, 'a', encoding='utf-8') as write_file:
                write_file.write(file_path + '\n')
        else:
            with open(self.list_file, 'w', encoding='utf-8') as write_file:
                write_file.write(file_path + '\n')

        self.list_widget.addItem(file_path.split('/')[-1])
        self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.status.showMessage('成功添加至播放列表！', 5000)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '打开文件夹')
        if not os.path.exists(folder):
            self.status.showMessage('未选择文件夹！', 5000)
            return
        if os.path.exists(self.list_file):
            with open(self.list_file, 'r', encoding='utf-8') as read_file:
                all_file_paths = read_file.readlines()
            write_file = open(self.list_file, 'a', encoding='utf-8')
        else:
            write_file = open(self.list_file, 'w', encoding='utf-8')
            all_file_paths = []

        it = QDirIterator(folder)
        it.next()
        while it.hasNext():
            if it.fileInfo().suffix() in self.file_types:
                file_path = it.filePath()
                if file_path + '\n' in all_file_paths:
                    it.next()
                    continue
                write_file.write(file_path + '\n')
                self.list_widget.addItem(it.fileInfo().fileName())
                self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
                self.status.showMessage('成功添加至播放列表！', 5000)
            it.next()
        if it.fileInfo().suffix() in self.file_types:
            file_path = it.filePath()
            if file_path + '\n' in all_file_paths:
                return
            write_file.write(file_path + '\n')
            self.list_widget.addItem(it.fileInfo().fileName())
            self.play_list.addMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.status.showMessage('成功添加至播放列表！', 5000)

        write_file.close()

    def play_last(self):
        self.play_list.previous()
        self.play()

    def play(self):
        if self.play_list.mediaCount() == 0:
            QMessageBox.warning(self, '警告', '没有待播放的文件！', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        self.play_list.setCurrentIndex(self.list_widget.currentRow())
        self.player.play()

    def pause(self):
        self.player.pause()

    def play_next(self):
        self.play_list.next()
        self.play()

    def quit(self):
        reply = QMessageBox.question(self, '消息', '确定退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()  # 退出应用程序

    def quickly_play(self):
        if self.play_list.mediaCount() == 0:
            return
        else:
            self.play()

    def change_play_mode(self, index):
        self.play_list.setPlaybackMode(index)

    def change_play_file(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.current_file_type = url.path().split('.')[-1]
            self.change_show_layout()
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
