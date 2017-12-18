from gtts import gTTS
import os


def say(firstname):
    tts = gTTS(text='Salut ' + firstname + ', comment tu vas ?', lang='fr')
    tts.save(firstname + ".mp3")
    os.system("afplay " + firstname + ".mp3")
    # os.remove("firstname.mp3")


def say2(firstname):
    os.system("say -v Thomas " + 'Salut ' + firstname + ', comment tu vas ?')
