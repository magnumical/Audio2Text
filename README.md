# Transcriber
We created this to transform videos/audio files into .txt file!


To use the app, you need to setup following python environment. First you need to install <ffmpeg> and set it in environment paths of your system:

https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

Then, in anaconda prompt, you need to go to the directory of my app, where app.py and requirements.txt are located. Then:

```
cd <directory>

conda create --name "NewEnv" python=3.9.13

conda activate newenv 

pip install -r requirements.txt

python app.py
```
## How to use
As soon as you open the sotware, you will see several options. [For GUI reference, use screenshot below]. 
First, you can select the file you want to transcribe. Then, software will assign a .txt file name, as same as name of video. However, you can rename this file. NExt step is selecting appropriate language, and then starting transcription by clicking on "Transcribe" button.

## Screenshot
![alt text](https://github.com/magnumical/Audio2Text/blob/main/img/img.png?raw=true)

the code is adapted from following article:
![Transcribing interview data from video to text with Python](https://towardsdatascience.com/transcribing-interview-data-from-video-to-text-with-python-5cdb6689eea1)

However, I also added several features to enance its applicablity!
