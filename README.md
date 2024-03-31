# Transcriber
We created this to transform videos/audio files into .txt file!


To use the app, you need to setup following python environment. First you need to install ffmpeg and set it in environment paths of your system:

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

## Build with pyinstaller
To build .exe app, you can use pyinstaller. For that, you need to load .pt files (whisper models) locally and bind them to .exe file. I used medium/small models so the overall size of program would be below 3GB. You need to place those file in the same directory as app.py (main application UI). Moreover, you need to add whisper assets into your exe file. All can be done through code below (replace the [user] and/or location of anaconda folder) 

``` pyinstaller --noconfirm --onedir --console --add-data "medium.pt;." --add-data "C:/Users/[user]/anaconda3/Lib/site-packages/whisper/assets/gpt2.tiktoken;./whisper/assets" --add-data "C:/Users/[user]/anaconda3/Lib/site-packages/whisper/assets/mel_filters.npz;./whisper/assets" --add-data "C:/Users/[user]/anaconda3/Lib/site-packages/whisper/assets/multilingual.tiktoken;./whisper/assets" --hidden-import "openai-whisper" --recursive-copy-metadata "openai-whisper" --hidden-import "torch"  app.py ```

## Screenshot
![alt text](https://github.com/magnumical/Audio2Text/blob/main/img/img.png?raw=true)

the code is adapted from following article:
![Transcribing interview data from video to text with Python](https://towardsdatascience.com/transcribing-interview-data-from-video-to-text-with-python-5cdb6689eea1)

However, I also added several features to enance its applicablity!
