import os
import core.RAG as RAG
import core.audioprocessing as audioprocessing
import core.file_reader as file_reader



from PyQt5.QtWidgets import QApplication, QWidget,  QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QDialog, QProgressBar, QDialogButtonBox, QTextEdit
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtCore import QProcess
import sys
import tempfile

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'



# Create a QWidget-based class to represent the application window
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.p = None  

        # Set window properties such as title, size, and icon
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        # Set window background color
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        # Initialize the user interface
        self.init_ui()
        self.vectordb = None
        self.chromadbdir = None



        # Display the window
        self.show()

    # Initialize the user interface components
    def init_ui(self):


        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create a QVideoWidget object to display video
        videowidget = QVideoWidget()

        openBtn = QPushButton('Load Files')
        openBtn.clicked.connect(self.open_file)



        # Create a QPushButton to play or pause the video
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Create a QSlider for seeking within the video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create a QLabel to display video information or errors
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.infoLabel = QLabel("No Video Loaded")
        self.infoLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        font = self.infoLabel.font()
        font.setPointSize(30)
        self.infoLabel.setFont(font)
        self.infoLabel.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('red'))
        self.infoLabel.setPalette(palette)

        

        # Create a QHBoxLayout for arranging widgets horizontally
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

      

        # Add widgets to the QHBoxLayout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
   

        # Create a QVBoxLayout for arranging widgets vertically
        vboxLayout = QVBoxLayout()

        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout.addWidget(self.infoLabel)

        # Set the layout of the window
        self.setLayout(vboxLayout)

        # Set the video output for the media player
        self.mediaPlayer.setVideoOutput(videowidget)

        # Connect media player signals to their respective slots
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    #Method to open a video file
    def open_file(self,filename):

        filename, _ = QFileDialog.getOpenFileName(self, "Open Video", filter='Video files (*.mp4l)', initialFilter='Video files (*.mp4l)')
        temp_dir = tempfile.mkdtemp()
        mediafile= file_reader.read_mp4l_file(filename, temp_dir)
        self.chromadbdir = temp_dir + "/chroma_db"
        print(self.chromadbdir)
        print(self.mediaPlayer)
        if filename != '':
            if mediafile:
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(mediafile)))
                self.playBtn.setEnabled(True)
                self.infoLabel.setText(filename)
                self.start_process()


    # Method to play or pause the video
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # Method to handle changes in media player state (playing or paused)
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    # Method to handle changes in video position
    def position_changed(self, position):
        self.slider.setValue(position)

    # Method to handle changes in video duration
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # Method to set the video position
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    # Method to handle errors in media playback
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def message(self, s):
        try:
            hands_raised = int(s)
            if(hands_raised > 0):
                self.mediaPlayer.pause()
                audioprocessing.text_to_speech('You have a question, how may I help you')
                questionAudioData = audioprocessing.record_audio()
                questionText = audioprocessing.recognize_speech(questionAudioData)
                if(questionText != ''):
                    print(questionText)
                    response = RAG.answer_query(self.chromadbdir, questionText)
                    audioprocessing.text_to_speech(response)
        except ValueError:
            print(s)


    def start_process(self):
        if self.p is None:  # No process running.
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.finished.connect(self.process_finished)
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            #self.p.stateChanged.connect(self.handle_state)
            self.p.start("python", ['./core/handtracker.py'])
            strated = self.p.waitForStarted()
    
    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")
            

    def process_finished(self):   
        self.p = None

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = Window()
window.show()

# Run the application event loop
app.exec()



# question = "Which company created the Game boy"

# print(result)
