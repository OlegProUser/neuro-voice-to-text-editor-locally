The program works locally due to ollama, in which you can install a neural network on a computer of your choice for free (gemma4 version is initially installed)

Before launching listener.exe you must install all dependencies and libraries using the command "pip install -r

" in the console. requirements.txt Next, the faster libraries will be installed-whisper, sounddevice, soundfile, keyboard, ollama, numpy

to process sound into text and keyboard, change HOTKEY = "..." or use the default combination "ctrl+alt+r".

You can install or change the desired local version of the neural network using the command

ollama pull gemma4# or other required version

# specify another version in main.py

string example: OLLAMA_MODEL = "gemma4"
