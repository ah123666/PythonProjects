from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class myVideoWidget(QVideoWidget):
    doubleClickedItem = pyqtSignal(str)  # 创建双击信号
    singleClickedItem = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QVideoWidget, self).__init__(parent)

    def mouseDoubleClickEvent(self, QMouseEvent):  # 双击事件
        self.doubleClickedItem.emit("double clicked")

    def mousePressEvent(self, QMouseEvent):
        self.singleClickedItem.emit("single clicked")


class My_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('media_player')
        self.resize(800, 600)
        self.player = QMediaPlayer()
        self.video_widget = myVideoWidget()  # 定义视频显示的widget
        self.player.setVideoOutput(self.video_widget)  # 视频播放输出的widget
        layout_h_1 = QHBoxLayout()
        layout_h_2 = QHBoxLayout()
        layout_h_3 = QHBoxLayout()
        layout_v = QVBoxLayout()

        self.play_button = QPushButton()
        self.play_button.setText("play")
        self.pause_button = QPushButton()
        self.pause_button.setText("pause")
        self.open_button = QPushButton()
        self.open_button.setText('open')
        self.quit_button = QPushButton()
        self.quit_button.setText('quit')

        self.play_slider = QSlider(Qt.Horizontal, self)
        self.play_slider.setRange(0, 0)
        self.play_slider.setSingleStep(1)
        self.play_slider.show()

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Microsoft YaHei", 8))

        self.play_label_1 = QLabel('00:00:00')
        self.play_label_2 = QLabel('00:00:00')

        layout_h_1.addWidget(self.play_label_1)
        layout_h_1.addWidget(self.play_slider)
        layout_h_1.addWidget(self.play_label_2)

        layout_h_2.addWidget(self.open_button)
        layout_h_2.addWidget(self.play_button)
        layout_h_2.addWidget(self.pause_button)
        layout_h_2.addWidget(self.quit_button)

        layout_h_3.addWidget(self.video_widget)
        layout_h_3.addWidget(self.list_widget)
        layout_h_3.setStretch(0, 3)
        layout_h_3.setStretch(1, 1)
        layout_v.addLayout(layout_h_3)
        layout_v.addLayout(layout_h_2)
        layout_v.addLayout(layout_h_1)

        self.video_widget.doubleClickedItem.connect(self.screen_double_clicked)
        self.video_widget.singleClickedItem.connect(self.screen_single_clicked)
        self.pause_button.clicked.connect(self.pause)
        self.play_button.clicked.connect(self.play)
        self.open_button.clicked.connect(self.get_video)
        self.quit_button.clicked.connect(self.quit)
        self.player.durationChanged.connect(self.chage_slide_range)
        self.play_slider.sliderMoved.connect(self.change_play_position)
        self.player.positionChanged.connect(self.change_slider_value)

        self.setLayout(layout_v)
        self.file_loaded = False
        self.pause_button.setEnabled(False)

    def screen_double_clicked(self):
        if not self.file_loaded:
            return
        self.play()
        if self.video_widget.isFullScreen():
            self.video_widget.setFullScreen(False)
        else:
            self.video_widget.setFullScreen(True)

    def screen_single_clicked(self):
        if not self.file_loaded:
            return
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def get_video(self):
        file_path = QFileDialog.getOpenFileName()[0]
        if file_path == '':
            return
        frame = QMediaContent(QUrl(file_path))
        self.player.setMedia(frame)
        self.file_loaded = True
        self.player.stop()
        self.pause()
        self.list_widget.addItem(file_path.split('/')[-1])
        QMessageBox.information(self, 'message', 'loading complete!', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def play(self):
        if not self.file_loaded:
            QMessageBox.warning(self, 'warning', 'no file to play!', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        self.player.play()
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)

    def pause(self):
        self.player.pause()
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)

    def quit(self):
        reply = QMessageBox.question(self, 'message', 'are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()  # 退出应用程序
        else:
            return

    def chage_slide_range(self, duration):
        self.play_slider.setRange(0, duration)
        total_time_s = int(duration / 1000)
        hour = total_time_s // 3600
        minute = total_time_s % 3600 // 60
        second = total_time_s % 3600 % 60
        time = [hour, minute, second]
        for i in range(len(time)):
            if time[i] < 10:
                time[i] = '0' + str(time[i])
            else:
                time[i] = str(time[i])
        self.play_label_2.setText(':'.join(time))

    def change_slider_value(self, position):
        self.play_slider.setValue(position)
        total_time_s = int(position / 1000)
        hour = total_time_s // 3600
        minute = total_time_s % 3600 // 60
        second = total_time_s % 3600 % 60
        time = [hour, minute, second]
        for i in range(len(time)):
            if time[i] < 10:
                time[i] = '0' + str(time[i])
            else:
                time[i] = str(time[i])
        self.play_label_1.setText(':'.join(time))

    def change_play_position(self, position):
        self.player.setPosition(position)  # 改变播放时刻


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = My_widget()
    main_win.show()
    sys.exit(app.exec_())
