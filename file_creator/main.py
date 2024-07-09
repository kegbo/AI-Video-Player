import os
import core.RAG as RAG
import core.audioprocessing as audioprocessing
import core.creator as creator
from PyQt5.QtWidgets import QApplication, QWidget,  QPushButton,  QVBoxLayout, QLabel, QFileDialog, QProgressBar,  QTextEdit, QLineEdit
import sys
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt
import sys
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties such as title, size, and icon
        self.setWindowTitle("RobotForge MP4L File creator")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        # Set window background color
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        # Initialize the user interface
        self.init_ui()

        self.videoFileName = ''
        self.memoryBank = []    

    def init_ui(self):

                # Create a QPushButton to open video files
        videoSelectBtn = QPushButton('Select Video')
        videoSelectBtn.clicked.connect(self.open_file)

        memorySelectBtn = QPushButton('Select Supplementary Files')
        memorySelectBtn.clicked.connect(self.load_memory)

        startProcessingBtn = QPushButton('Start Processing')
        startProcessingBtn.clicked.connect(self.start_process)

        self.closeBtn = QPushButton('Close')
        self.closeBtn.clicked.connect(self.close)

  

        self.layout = QVBoxLayout()
        message = QLabel("Select the Video Lecture to play")
        self.layout.addWidget(message)
        self.layout.addWidget(videoSelectBtn)
        self.videoNameTextArea = QTextEdit()
        self.videoNameTextArea.setReadOnly(True)
        self.layout.addWidget(self.videoNameTextArea)

        message2 = QLabel("Select the Supplementary Document")
        self.layout.addWidget(message2)
        self.memoryBankTextArea = QTextEdit()
        self.memoryBankTextArea.setReadOnly(True)
        self.layout.addWidget(self.memoryBankTextArea)
        self.layout.addWidget(memorySelectBtn)


        self.outputFileNameTextArea = QLineEdit()
        self.outputFileNameTextArea.setPlaceholderText("Enter Output File Name")
        self.layout.addWidget(self.outputFileNameTextArea)

        self.fileNameErrorLabel= QLabel("Enter a file name")
        self.fileNameErrorLabel.hide()
        self.layout.addWidget(self.fileNameErrorLabel)

        
        self.layout.addWidget(startProcessingBtn)



        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.layout.addWidget(self.closeBtn)
        
      
        self.complete = QLabel("mp4l file created")
        self.layout.addWidget(self.complete)
        self.complete.hide()
        self.setLayout(self.layout)

    def close(self):
        sys.exit()
        

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Video")
        self.videoFileName = filename
        self.videoNameTextArea.setPlainText(self.videoFileName)

    def load_memory(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, "Load Memory")
        self.memoryBank=filenames
        for name in filenames:
            self.memoryBankTextArea.append(name)
        
    def start_process(self):

        if(self.outputFileNameTextArea.text() == ""):
            self.fileNameErrorLabel.show()
            self.fileNameErrorLabel.setStyleSheet("background-color: red; border: 1px solid black;")
        else:
            self.fileNameErrorLabel.hide()
            self.outputFileNameTextArea.setReadOnly(True)
            self.progress_bar.setValue(10)
            video_location = os.path.join(self.videoFileName)
            audio_location = os.path.join(os.getcwd(),"audio.wav")
            audioprocessing.extract_audio_from_video(video_location, audio_location)
            self.progress_bar.setValue(40)
            audio_transcript = audioprocessing.transcribe_audio_file(audio_location)
            self.progress_bar.setValue(50)
            self.db = RAG.create_vector_db(audio_transcript,self.memoryBank)
            self.progress_bar.setValue(90)

            # List all files and directories within the chroma_db directory
            contents = os.listdir("chroma_db")

            # Filter out directories
            subfolders = [item for item in contents if os.path.isdir(os.path.join("chroma_db", item))]

            # Assuming there is only one subfolder, get its name
            if subfolders:
                subfolder_name = subfolders[0]
                print("Subfolder name:", subfolder_name)
            else:
                print("No subfolder found in the chroma_db directory.")

            sql_file = "chroma_db/chroma.sqlite3"
            bin_folder = "chroma_db/"+subfolder_name
            mp4_file = self.videoFileName
            output_file = self.outputFileNameTextArea.text()+ ".mp4l"
            creator.create_mp4l_file(sql_file, bin_folder, mp4_file, output_file)


            self.progress_bar.setValue(100)
            self.closeBtn.show()
            self.complete.show()

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = Window()
window.show()

# Run the application event loop
app.exec()
