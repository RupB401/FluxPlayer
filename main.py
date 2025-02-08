from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider, QWidgetAction, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QUrl, QTimer, QTime, QEvent
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
import sys
import os

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FluxPlayer")
        self.setGeometry(450, 200, 800, 500)
        self.setWindowIcon(QIcon('media player/icons/Windows Media Player.png'))
        self.setStyleSheet("background-color: slate;")

        # Create the menu bar
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet("background-color: #212121; color: white;")

        # Add Menus
        self.media_menu = self.menu_bar.addMenu("Media")
        self.playback_menu = self.menu_bar.addMenu("Playback")
        self.audio_menu = self.menu_bar.addMenu("Audio")
        self.video_menu = self.menu_bar.addMenu("Video")
        self.subtitle_menu = self.menu_bar.addMenu("Subtitle")

        # Load Icons
        open_icon = QIcon("media player/icons/windows-media-player_888881 (1).png")
        play_icon = QIcon("media player/icons/icons8-play-30.png")
        pause_icon = QIcon("media player/icons/icons8-pause-button-30.png")
        stop_icon = QIcon("media player/icons/icons8-stop-30.png")
        previous_icon = QIcon("media player/icons/icons8-previous-32.png")
        next_icon = QIcon("media player/icons/icons8-next-32.png")
        repeat_icon = QIcon("media player/icons/icons8-repeat-32.png")
        folder_icon = QIcon("media player/icons/windows-media-player_888881 (1).png")
        quit_icon = QIcon("media player/icons/icons8-exit-32.png")
        fullscreen_icon = QIcon("media player/icons/icons8-full-screen-32.png")

        # Create Actions
        open_file = QAction(open_icon, "Open File...", self)
        open_file.setStatusTip("Open a file")
        open_file.triggered.connect(self.open_file_dialog)

        open_folder = QAction(folder_icon, "Open Folder...", self)
        open_folder.setStatusTip("Open a folder")
        open_folder.triggered.connect(self.open_folder_dialog)

        quit_action = QAction(quit_icon, "Quit", self)
        quit_action.setStatusTip("Quit the application")
        quit_action.triggered.connect(self.close)

        # Add Actions to Media Menu
        self.media_menu.addAction(open_file)
        self.media_menu.addAction(open_folder)
        self.media_menu.addSeparator()
        self.media_menu.addAction(quit_action)

        # Playback Actions
        play_action = QAction(play_icon, "Play", self)
        play_action.setStatusTip("Play media")
        play_action.triggered.connect(self.play_media)

        pause_action = QAction(pause_icon, "Pause", self)
        pause_action.setStatusTip("Pause media")
        pause_action.triggered.connect(self.pause_media)

        stop_action = QAction(stop_icon, "Stop", self)
        stop_action.setStatusTip("Stop media")
        stop_action.triggered.connect(self.stop_media)

        previous_action = QAction(previous_icon, "Previous", self)
        previous_action.setStatusTip("Play previous media")
        previous_action.triggered.connect(self.previous_media)

        next_action = QAction(next_icon, "Next", self)
        next_action.setStatusTip("Play next media")
        next_action.triggered.connect(self.next_media)

        repeat_action = QAction(repeat_icon, "Repeat", self)
        repeat_action.setStatusTip("Repeat media")
        repeat_action.triggered.connect(self.repeat_media)

        # Add Actions to Playback Menu
        self.playback_menu.addAction(play_action)
        self.playback_menu.addAction(pause_action)
        self.playback_menu.addAction(stop_action)
        self.playback_menu.addAction(previous_action)
        self.playback_menu.addAction(next_action)
        self.playback_menu.addAction(repeat_action)

        # Create Volume Slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setStatusTip("Adjust volume")
        self.volume_slider.valueChanged.connect(self.adjust_volume)

        # Use QWidgetAction for the volume slider
        volume_action = QWidgetAction(self)
        volume_action.setDefaultWidget(self.volume_slider)
        self.audio_menu.addAction(volume_action)

        # Create Vertical Volume Slider
        self.vertical_volume_slider = QSlider(Qt.Orientation.Vertical, self)
        self.vertical_volume_slider.setRange(0, 100)
        self.vertical_volume_slider.setValue(50)
        self.vertical_volume_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.vertical_volume_slider.setTickInterval(10)
        self.vertical_volume_slider.setStatusTip("Adjust volume")
        self.vertical_volume_slider.valueChanged.connect(self.adjust_volume)
        self.vertical_volume_slider.hide()

        # Fullscreen Action
        fullscreen_action = QAction(fullscreen_icon, "Fullscreen", self)
        fullscreen_action.setStatusTip("Toggle fullscreen mode")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)

        # Add Fullscreen Action to Video Menu
        self.video_menu.addAction(fullscreen_action)

        # Subtitle Action
        open_subtitle = QAction(QIcon("media player/icons/subtitle.png"), "Open Subtitle...", self)
        open_subtitle.setStatusTip("Open a subtitle file")
        open_subtitle.triggered.connect(self.open_subtitle_dialog)

        # Add Subtitle Action to Subtitle Menu
        self.subtitle_menu.addAction(open_subtitle)

        # Media Player
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        # Ensure the video widget expands and maintains aspect ratio
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Video Progress Slider
        self.video_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.video_slider.setRange(0, 100)
        self.video_slider.sliderMoved.connect(self.set_position)
        self.video_slider.sliderReleased.connect(self.slider_released)

        # Video Time Labels
        self.current_time_label = QLabel("00:00", self)
        self.current_time_label.setStyleSheet("color: white;")
        self.total_time_label = QLabel("00:00", self)
        self.total_time_label.setStyleSheet("color: white;")

        # Subtitle Label
        self.subtitle_label = QLabel("", self)
        self.subtitle_label.setStyleSheet("color: white; background-color: black; font-size: 30px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Play/Pause Button
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(play_icon)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)

        # Layout
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.play_pause_button)
        slider_layout.addWidget(self.current_time_label)
        slider_layout.addWidget(self.video_slider)
        slider_layout.addWidget(self.total_time_label)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget, 1)  # Ensure the video widget expands
        layout.addWidget(self.subtitle_label)
        layout.addLayout(slider_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer to update the video slider
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_slider)
        self.timer.start()

        # Timer to hide the progress bar
        self.hide_timer = QTimer(self)
        self.hide_timer.setInterval(2000)
        self.hide_timer.timeout.connect(self.hide_progress_bar)

        # Timer to hide the vertical volume slider
        self.hide_volume_timer = QTimer(self)
        self.hide_volume_timer.setInterval(2000)
        self.hide_volume_timer.timeout.connect(self.hide_vertical_volume_slider)

        # Media Player Signals
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

        # Playlist
        self.playlist = []
        self.current_index = -1
        self.repeat = False

        # Mute state
        self.is_muted = False

        # Progress bar visibility state
        self.progress_bar_visible = False

        # Subtitle data
        self.subtitles = []
        self.current_subtitle_index = 0

        # Install event filter to detect mouse movements
        self.installEventFilter(self)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        if file_path:
            self.playlist = [file_path]
            self.current_index = 0
            self.media_player.setSource(QUrl.fromLocalFile(file_path))
            self.play_media()

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.playlist = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.mp3', '.mp4', '.avi', '.mkv', '.hevc', '.webm', '.flv', '.mov', '.wmv'))]               
            self.current_index = 0
            self.media_player.setSource(QUrl.fromLocalFile(self.playlist[self.current_index]))
            self.play_media()
            self.load_subtitle_from_folder(folder_path)

    def load_subtitle_from_folder(self, folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(('.srt', '.sub', '.txt')):
                self.load_subtitles(os.path.join(folder_path, file))
                break

    def open_subtitle_dialog(self):
        subtitle_path, _ = QFileDialog.getOpenFileName(self, "Open Subtitle", "", "Subtitle Files (*.srt *.sub *.txt)")
        if subtitle_path:
            self.load_subtitles(subtitle_path)

    def load_subtitles(self, subtitle_path):
        with open(subtitle_path, encoding='utf-8') as file:
            self.subtitles = []
            for line in file:
                if '-->' in line:
                    times = line.strip().split(' --> ')
                    start_time = self.time_to_milliseconds(times[0])
                    end_time = self.time_to_milliseconds(times[1])
                    text = next(file).strip()
                    self.subtitles.append((start_time, end_time, text))
            self.current_subtitle_index = 0

    def time_to_milliseconds(self, time_str):
        hours, minutes, seconds = time_str.split(':')
        seconds, milliseconds = seconds.split(',')
        return (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)

    def play_media(self):
        self.media_player.play()
        self.play_pause_button.setIcon(QIcon("media player/icons/icons8-pause-button-30.png"))

    def pause_media(self):
        self.media_player.pause()
        self.play_pause_button.setIcon(QIcon("media player/icons/icons8-play-30.png"))

    def stop_media(self):
        self.media_player.stop()
        self.play_pause_button.setIcon(QIcon("media player/icons/icons8-play-30.png"))

    def previous_media(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.media_player.setSource(QUrl.fromLocalFile(self.playlist[self.current_index]))
            self.play_media()
            self.load_subtitle_from_folder(os.path.dirname(self.playlist[self.current_index]))

    def next_media(self):
        if self.current_index < len(self.playlist) - 1:
            self.current_index += 1
            self.media_player.setSource(QUrl.fromLocalFile(self.playlist[self.current_index]))
            self.play_media()
            self.load_subtitle_from_folder(os.path.dirname(self.playlist[self.current_index]))

    def repeat_media(self):
        self.repeat = not self.repeat

    def adjust_volume(self, value):
        self.audio_output.setVolume(value / 100)
        self.volume_slider.setValue(value)
        self.vertical_volume_slider.setValue(value)
        self.show_vertical_volume_slider()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.menu_bar.show()
            self.show_progress_bar()  # Show playback controls
        else:
            self.showFullScreen()
            self.menu_bar.hide()
            self.hide_progress_bar()  # Hide controls for full immersion

    def keyPressEvent(self, event):
        print(f"Key pressed: {event.key()}")  # Debugging statement
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
        elif event.key() == Qt.Key.Key_Right:
            print("Right arrow key pressed")  # Debugging statement
            new_position = self.media_player.position() + 5000
            print(f"New position: {new_position}")  # Debugging statement
            self.media_player.setPosition(new_position)
        elif event.key() == Qt.Key.Key_Left:
            print("Left arrow key pressed")  # Debugging statement
            new_position = self.media_player.position() - 5000
            print(f"New position: {new_position}")  # Debugging statement
            self.media_player.setPosition(new_position)
        elif event.key() == Qt.Key.Key_M:
            self.toggle_mute()
        elif event.key() == Qt.Key.Key_N:
            self.next_media()
        elif event.key() == Qt.Key.Key_B:
            self.previous_media()
        elif event.key() == Qt.Key.Key_Up:
            self.adjust_volume(min(self.volume_slider.value() + 5, 100))
        elif event.key() == Qt.Key.Key_Down:
            self.adjust_volume(max(self.volume_slider.value() - 5, 0))
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.adjust_volume(min(self.volume_slider.value() + 5, 100))
        else:
            self.adjust_volume(max(self.volume_slider.value() - 5, 0))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_play_pause()
        elif event.button() == Qt.MouseButton.RightButton:
            if self.progress_bar_visible:
                self.hide_progress_bar()
            else:
                self.show_progress_bar()
            self.progress_bar_visible = not self.progress_bar_visible

    def toggle_play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause_media()
        else:
            self.play_media()

    def toggle_mute(self):
        if self.is_muted:
            self.audio_output.setMuted(False)
            self.is_muted = False
        else:
            self.audio_output.setMuted(True)
            self.is_muted = True

    def set_position(self, position):
        self.media_player.setPosition(position)

    def slider_released(self):
        self.set_position(self.video_slider.value())

    def update_slider(self):
        self.video_slider.setValue(self.media_player.position())
        self.current_time_label.setText(QTime(0, 0).addMSecs(self.media_player.position()).toString("hh:mm:ss"))
        self.total_time_label.setText(QTime(0, 0).addMSecs(self.media_player.duration()).toString("hh:mm:ss"))
        self.update_subtitle()
        if not self.isFullScreen():
            self.show_progress_bar()

    def position_changed(self, position):
        self.video_slider.setValue(position)
        self.current_time_label.setText(QTime(0, 0).addMSecs(position).toString("mm:ss"))
        self.update_subtitle()

    def duration_changed(self, duration):
        self.video_slider.setRange(0, duration)
        self.total_time_label.setText(QTime(0, 0).addMSecs(duration).toString("mm:ss"))

    def update_subtitle(self):
        current_time = self.media_player.position()
        if self.subtitles and self.current_subtitle_index < len(self.subtitles):
            start_time, end_time, text = self.subtitles[self.current_subtitle_index]
            if start_time <= current_time <= end_time:
                self.subtitle_label.setText(text)
            elif current_time > end_time:
                self.current_subtitle_index += 1
                self.subtitle_label.setText("")
            else:
                self.subtitle_label.setText("")

    def show_progress_bar(self):
        self.video_slider.show()
        self.current_time_label.show()
        self.total_time_label.show()
        self.play_pause_button.show()
        self.hide_timer.start()

    def hide_progress_bar(self):
        self.video_slider.hide()
        self.current_time_label.hide()
        self.total_time_label.hide()
        self.play_pause_button.hide()

    def show_vertical_volume_slider(self):
        self.vertical_volume_slider.show()
        self.hide_volume_timer.start()

    def hide_vertical_volume_slider(self):
        self.vertical_volume_slider.hide()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseMove:
            if self.isFullScreen():
                self.show_progress_bar()
                self.show_vertical_volume_slider()
        return super().eventFilter(source, event)

    def resizeEvent(self, event):
        self.video_widget.resize(self.size())
        super().resizeEvent(event)

# Run the application
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
