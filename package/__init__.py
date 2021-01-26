import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

import glob
import os.path


def get_large_audio_transcription(path_to_file):
    """
    Splitting the audio file into portions
    and apply speech recognition on each of those
    """
    file_sound: AudioSegment = AudioSegment.from_wav(path_to_file)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    portions = split_on_silence(file_sound,
                                # experiment with this value for your target audio file
                                min_silence_len=500,
                                # adjust this per requirement
                                silence_thresh=file_sound.dBFS - 14,
                                # keep the silence for 1 second, adjustable as well
                                keep_silence=500,
                                )
    folder_name = "portions"

    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    for i, portions in enumerate(portions, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        portion_filename = os.path.join(folder_name, f"portion{i}.wav")
        portions.export(portion_filename, format="wav")

        with sr.AudioFile(portion_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError:
                print()
            else:
                text = f"{text.capitalize()}. "
                whole_text += text

    return whole_text


directory = '.'
files = glob.glob(os.path.join("C:\\Users\\Costel\\Desktop\\testing", '*.mp4'))
files.sort(key=os.path.getctime, reverse=True)

text_file = open("Output.txt", "w")
text_file.write("Salut! \n")

for file in files:
    path = os.path.splitext(file)[0]
    mp3File = "ffmpeg -i " + file + " " + path + ".mp3"
    wavFile = "ffmpeg -i " + path + ".mp3 " + path + ".wav"
    os.system(mp3File)
    os.system(wavFile)

    r = sr.Recognizer()

    text_file = open("Output.txt", "a")
    text_file.write(get_large_audio_transcription(path + ".wav"))

text_file.close()

# mp3File = "ffmpeg -i C:\\Users\\Costel\\IdeaProjects\\SpeechToText\\Spatial_Enumeration.mp4 " \
#          "C:\\Users\\Costel\\IdeaProjects\\SpeechToText\\Spatial_Enumeration.mp3 "
# wavFile = "ffmpeg -i C:\\Users\\Costel\\IdeaProjects\\SpeechToText\\Spatial_Enumeration.mp3 " \
#         "C:\\Users\\Costel\\IdeaProjects\\SpeechToText\\Spatial_Enumeration.wav "
