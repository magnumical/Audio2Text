# -*- coding: utf-8 -*-
"""
Created in 2024

@author: reza.amini
reza.aminigougeh@mail.mcgill.ca
"""



import sys, os

import os
import sys
model_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname("./medium.pt")))
path_to_model = os.path.abspath(os.path.join(model_dir, 'medium.pt'))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



import wave, contextlib, math, time
import speech_recognition as sr

model_path= resource_path("medium.pt")

print("[info] Starting applicaiton ...")
print(f"[info] whisper model: {model_path}")

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_normalize import audio_normalize

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QButtonGroup  
import whisper


model = whisper.load_model(f"{model_path}")#("./small.pt")
print("[info] Model successfully loaded ...")

class Ui_MainWindow(object):
    """Main window GUI."""
    def __init__(self):
        """Initialisation function."""
        self.mp4_file_name = ""
        self.output_file = ""
        self.audio_file = "speech.wav"
        
    def setupUi(self, MainWindow):
        """Define visual components and positions."""
        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(653, 836)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 161, 41))
        
        
        
        self.select_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_file_button.setGeometry(QtCore.QRect(250,10, 150, 30))  # Adjust the position and size
        font = QtGui.QFont()
        font.setPointSize(10)
        self.select_file_button.setFont(font)
        self.select_file_button.setObjectName("select_file_button")
        self.select_file_button.setText("Select File")
        self.select_file_button.clicked.connect(self.open_audio_file)
        
        # Selected video file label
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.selected_video_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_video_label.setGeometry(QtCore.QRect(230, 50, 371, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.selected_video_label.setFont(font)
        self.selected_video_label.setFrameShape(QtWidgets.QFrame.Box)
        self.selected_video_label.setText("")
        self.selected_video_label.setObjectName("selected_video_label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 90, 161, 41))
        # Transcribed text box
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.transcribed_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.transcribed_text.setGeometry(QtCore.QRect(70, 320, 520, 431))
        self.transcribed_text.setObjectName("transcribed_text")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 280, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.transcribe_button = QtWidgets.QPushButton(self.centralwidget)
        self.transcribe_button.setEnabled(False)
        self.transcribe_button.setGeometry(QtCore.QRect(230, 150, 221, 81))
        # Transcribe button
        font = QtGui.QFont()
        font.setPointSize(14)
        self.transcribe_button.setFont(font)
        self.transcribe_button.setObjectName("transcribe_button")
        self.transcribe_button.clicked.connect(self.process_and_transcribe_audio)
        # progeress bar
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(230, 250, 381, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(0, 760, 651, 21))
        # Message label (for errors and warnings)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.message_label.setFont(font)
        self.message_label.setFrameShape(QtWidgets.QFrame.Box)
        self.message_label.setText("")
        self.message_label.setObjectName("message_label")
        self.output_file_name = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.output_file_name.setGeometry(QtCore.QRect(230, 90, 371, 41))
        # Output file name
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_file_name.setFont(font)
        self.output_file_name.setObjectName("output_file_name")
        
        self.language_group = QButtonGroup(self.centralwidget)

        # Checkbox for English
        self.checkbox_en = QtWidgets.QCheckBox("English", self.centralwidget)
        self.checkbox_en.setGeometry(QtCore.QRect(40, 170, 100, 20))
        self.checkbox_en.setChecked(True)  # English is checked by default
        self.language_group.addButton(self.checkbox_en)  # Add checkbox to the group

        # Checkbox for French (Canada)
        self.checkbox_fr_CA = QtWidgets.QCheckBox("French (Canada)", self.centralwidget)
        self.checkbox_fr_CA.setGeometry(QtCore.QRect(40, 190, 150, 20))
        self.language_group.addButton(self.checkbox_fr_CA)  # Add checkbox to the group

        # Checkbox for English (Canada)
        self.checkbox_en_CA = QtWidgets.QCheckBox("English (Canada)", self.centralwidget)
        self.checkbox_en_CA.setGeometry(QtCore.QRect(40, 210, 150, 20))
        self.language_group.addButton(self.checkbox_en_CA)  # Add checkbox to the group

        # Checkbox for French (France)
        self.checkbox_fr_FR = QtWidgets.QCheckBox("French (France)", self.centralwidget)
        self.checkbox_fr_FR.setGeometry(QtCore.QRect(40, 230, 150, 20))
        self.language_group.addButton(self.checkbox_fr_FR)  # Add checkbox to the group

                # Transcription method selection dropdown
        self.transcription_method_combo = QtWidgets.QComboBox(self.centralwidget)
        self.transcription_method_combo.setGeometry(QtCore.QRect(480, 170, 150, 30))  # Adjust position and size as needed
        self.transcription_method_combo.addItems([
            "Whisper", "Google Speech Recognition", "Google Cloud Speech API",
            "Wit.ai", "Microsoft Bing Voice Recognition", 
            "Houndify API", "IBM Speech to Text", "Sphinx (offline)",
        ])   
        # Menubar options
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 653, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_mp4_video_recording = QtWidgets.QAction(MainWindow)
        self.actionOpen_mp4_video_recording.setObjectName("actionOpen_mp4_video_recording")
        self.actionOpen_mp4_video_recording.triggered.connect(self.open_audio_file)
        self.actionAbout_vid2text = QtWidgets.QAction(MainWindow)
        self.actionAbout_vid2text.setObjectName("actionAbout_vid2text")
        self.actionAbout_vid2text.triggered.connect(self.show_about)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.new_project)
        self.menuFile.addAction(self.actionOpen_mp4_video_recording)
        self.menuFile.addAction(self.actionNew)
        self.menuAbout.addAction(self.actionAbout_vid2text)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        """Translate UI method."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Transciber!", "Transciber!"))
        self.label.setText(_translate("MainWindow", "Selected file:"))
        self.label_3.setText(_translate("MainWindow", "Output file name:"))
        self.label_5.setText(_translate("MainWindow", "Transcribed text:"))
        self.transcribe_button.setText(_translate("MainWindow", "Transcribe"))
        self.output_file_name.setPlaceholderText(_translate("MainWindow", "interview1.txt"))
        
        #self.select_lang.setPlaceholderText(_translate("MainWindow", "fr-CA en-CA en-US fr-FR?"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen_mp4_video_recording.setText(_translate("MainWindow", "Open a recording"))
        self.actionAbout_vid2text.setText(_translate("MainWindow", "About"))
        self.actionNew.setText(_translate("MainWindow", "New project"))
    
    def open_audio_file(self):
        """Open the audio (*.mp3) file."""
        file_name, _ = QFileDialog.getOpenFileName()  # _ for ignoring the filter
        if file_name:
            self.transcribe_button.setEnabled(True)
            self.mp4_file_name = file_name
            self.selected_video_label.setText(file_name)
    
            # Extract base name and set the default output file name as .txt
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            self.output_file = f"{base_name}.txt"
            
            # Display the default output file name in the UI
            self.output_file_name.setPlainText(self.output_file)
        else:
            self.message_label.setText("Please select a file")
        
    
    def open_audio_fileXX(self):
        """Open the audio (*.mp3) file."""
        file_name = QFileDialog.getOpenFileName()
        #if file_name[0][-3:] == "mp4":
        self.transcribe_button.setEnabled(True)
        self.mp4_file_name = file_name[0]
        self.message_label.setText("")
        self.selected_video_label.setText(file_name[0])
       # else:
       #     self.message_label.setText("Please select an *.mp3 file")
    def convert_mp4_to_wav(self):
        """Convert the mp4 video file into an audio file."""
        self.message_label.setText("Converting to *.wav ...")
        print("[info] Converting to *.wav ...")

        self.convert_thread = convertVideoToAudioThread(self.mp4_file_name, self.audio_file)
        self.convert_thread.finished.connect(self.finished_converting)
        self.convert_thread.start()
    def get_audio_duration(self, audio_file):
        """Determine the length of the audio file."""
        with contextlib.closing(wave.open(audio_file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
        
    def transcribe_audio(self, audio_file):
        """Transcribe the audio file."""
        total_duration = self.get_audio_duration(audio_file) / 10 #REZA
        total_duration = math.ceil(total_duration)
        self.td = total_duration
        if len(self.output_file_name.toPlainText()) > 0:
            self.output_file = self.output_file_name.toPlainText()
        else:
            self.output_file = "my_speech_file.txt"
    
        # Determine selected language based on checkboxes
        if self.checkbox_en.isChecked():
            self.selected_lang = "en-US"
        elif self.checkbox_fr_CA.isChecked():
            self.selected_lang = "fr-CA"
        elif self.checkbox_en_CA.isChecked():
            self.selected_lang = "en-CA"
        elif self.checkbox_fr_FR.isChecked():
            self.selected_lang = "fr-FR"
        else:
            self.selected_lang = "en-US"  # Default to English if no checkbox is selected
    
        # Get the selected transcription method from the combo box
        selected_transcription_method = self.transcription_method_combo.currentText()
    
        # Use thread to process in the background and avoid freezing the GUI
        self.thread = transcriptionThread(
            total_duration, audio_file, self.output_file, 
            self.selected_lang, selected_transcription_method
        )
        self.thread.finished.connect(self.finished_transcribing)
        self.thread.change_value.connect(self.set_progress_value)
        self.thread.start()

   

    def finished_converting(self):
        """Reset message text when conversion is finished."""
        self.message_label.setText("Transcribing file...")
        self.transcribe_audio(self.audio_file)
    def finished_transcribing(self):
        """This run when transcription finished to tidy up UI."""
        print("[info] Transcription finished ...")

        self.progress_bar.setValue(100)
        self.transcribe_button.setEnabled(True)
        self.message_label.setText("")
        self.update_text_output()
    def set_progress_value(self, val):
        """Update progress bar value."""
        increment = int(math.floor(100*(float(val)/self.td)))
        self.progress_bar.setValue(increment)
    def process_and_transcribe_audio(self):
        """Process the audio into a textual transcription."""
        self.transcribe_button.setEnabled(False)
        self.message_label.setText("Converting mp4 to audio (*.wav)...")
        self.convert_mp4_to_wav()
        

          
    def update_text_output(self):
    # Ensure the output file path is not empty or null
        if not self.output_file:
            self.output_file = "default_output.txt"  # Set a default file name if none is provided
    
        # Check if the file exists; if not, create it
        if not os.path.isfile(self.output_file):
            with open(self.output_file, "w") as f:
                f.write("")  # Create an empty file if it does not exist
            self.message_label.setText(f"Created new file: {self.output_file}")
            print(f"Created new file: {self.output_file}")
    
        # Now, read and display the content
        with open(self.output_file, "r") as f:
            self.transcribed_text.setText(f.read())
        
        
    def new_project(self):
        """Clear existing fields of data."""
        self.message_label.setText("")
        self.transcribed_text.setText("")
        self.selected_video_label.setText("")
        self.output_file_name.document().setPlainText("")
        self.progress_bar.setValue(0)
    def show_about(self):
        """Show about message box."""
        msg = QMessageBox()
        msg.setWindowTitle("About")
        msg.setText(" Oh there is nothing to say ... \n you aready know")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()



class convertVideoToAudioThread(QThread):
    """Thread to convert various audio/video files to wav format."""
    def __init__(self, input_file_name, output_audio_file):
        """Initialization function."""
        QThread.__init__(self)
        self.input_file_name = input_file_name
        self.output_audio_file = output_audio_file

    def __del__(self):
        """Destructor."""
        self.wait()

    def run(self):
        """Run file conversion task."""
        # Determine the file extension
        file_extension = os.path.splitext(self.input_file_name)[1].lower()

        try:
            if file_extension in ['.mp4', '.mov', '.mkv', '.avi']:  # Video files
                with VideoFileClip(self.input_file_name) as video:
                    audio = video.audio
                    audio.write_audiofile(self.output_audio_file, codec='pcm_s16le')
            elif file_extension in ['.mp3', '.ogg', '.m4a', '.wav']:  # Audio files
                with AudioFileClip(self.input_file_name) as audio:
                    audio.write_audiofile(self.output_audio_file, codec='pcm_s16le')
            else:
                print(f"Unsupported file format: {file_extension}")
        except Exception as e:
            print(f"Error in converting file: {e}")


class transcriptionThread(QThread):
    """Thread to transcribe file from audio to text."""
    change_value = pyqtSignal(int)
    def __init__(self, total_duration, audio_file, output_file, selected_lang, transcription_method):
        """Initialization function."""
        QThread.__init__(self)
        self.total_duration = total_duration
        self.audio_file = audio_file
        self.output_file = output_file
        self.selected_lang = selected_lang
        self.transcription_method = transcription_method
        
    def __del__(self):
        """Destructor."""
        self.wait()

    
    def run(self):
        r = sr.Recognizer()
        print("[info] Starting Transcription ...")

        if self.transcription_method == "Whisper":
            try:
                # Transcribe using the file path with timestamps
                result = model.transcribe(self.audio_file)
                segments = result["segments"]
    
                # Open the file in append mode, which creates the file if it doesn't exist
                with open(self.output_file, "a") as f:
                    for segment in segments:
                        start_time = segment["start"]
                        end_time = segment["end"]
                        text = segment["text"]
                        f.write(f"{start_time}-{end_time}: {text}\n")
    
                # Emit signal for completion
                self.change_value.emit(self.total_duration)
    
            except Exception as e:
                print(f"An error occurred during Whisper transcription: {e}.")
                
        # Other transcription methods...

    

        else:
            with sr.AudioFile(self.audio_file) as source:
                for i in range(0, self.total_duration):
                    try:
                        audio = r.record(source, offset=i*10, duration=10)
                         
                        text = ""  # Initialize text variable
        
                        if self.transcription_method == "Google Speech Recognition":
                            text = r.recognize_google(audio, language=self.selected_lang)
        
                        elif self.transcription_method == "Google Cloud Speech API":
                            # Replace 'YOUR_GOOGLE_CLOUD_SPEECH_API_KEY' with your actual API key
                            text = r.recognize_google_cloud(audio, language=self.selected_lang, credentials_json='YOUR_GOOGLE_CLOUD_SPEECH_API_KEY')
                            
                        elif self.transcription_method == "Wit.ai":
                            # Replace 'YOUR_WIT_AI_API_KEY' with your actual API key
                            text = r.recognize_wit(audio, key='YOUR_WIT_AI_API_KEY')
                            
                        elif self.transcription_method == "Microsoft Bing Voice Recognition":
                            # Replace 'YOUR_BING_VOICE_API_KEY' with your actual API key
                            text = r.recognize_bing(audio, key='YOUR_BING_VOICE_API_KEY', language=self.selected_lang)
        
                        elif self.transcription_method == "Houndify API":
                            # Replace 'YOUR_HOUNDIFY_CLIENT_ID' and 'YOUR_HOUNDIFY_CLIENT_KEY' with your actual client ID and key
                            text = r.recognize_houndify(audio, client_id='YOUR_HOUNDIFY_CLIENT_ID', client_key='YOUR_HOUNDIFY_CLIENT_KEY')
        
                        elif self.transcription_method == "IBM Speech to Text":
                            # Replace 'YOUR_IBM_USERNAME' and 'YOUR_IBM_PASSWORD' with your actual username and password
                            text = r.recognize_ibm(audio, username='YOUR_IBM_USERNAME', password='YOUR_IBM_PASSWORD', language=self.selected_lang)
        
                        elif self.transcription_method == "Sphinx (offline)":
                            text = r.recognize_sphinx(audio, language=self.selected_lang)
        
        
                        else:
                            text = "Unknown transcription method selected."
        
                        # Write the recognized text to the output file
                        with open(self.output_file, "a") as f:
                            f.write(text + " ")
        
                        self.change_value.emit(i)
        
                    except sr.UnknownValueError:
                        print(f"No speech could be recognized in chunk {i}.")
                        continue
                    except sr.RequestError as e:
                        print(f"Could not request results from the speech recognition service; {e}.")
                        continue
                    except Exception as e:
                        print(f"An error occurred in chunk {i}: {e}.")
                        continue

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
    
    
