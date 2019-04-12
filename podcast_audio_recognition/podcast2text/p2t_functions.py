#!/usr/bin/env python3

import logging
import speech_recognition as sr
import os
from pydub import AudioSegment

if __name__ != '__main__':
    logger = logging.getLogger(__name__)

r = sr.Recognizer()

def convert_mp3_to_wav(input_path):
    """Converts mp3 files to wav files"""
    logger.info("Start converting mp3 to wav")
    head, tail = os.path.split(input_path)
    split_tail = os.path.splitext(tail)
    file_name = split_tail[0]
    logger.debug("Following file is read: {}".format(input_path))
    sound = AudioSegment.from_mp3(input_path)
    output_path = head + "/" + file_name + ".wav"
    logger.debug("Following file is written: {}".format(output_path))
    sound.export(output_path, format="wav")
    return output_path

def read_audio(input_path):
    """Read audio file into speech_recogintion audio data object"""
    logger.info("Start reading audio file to audio object")
    input_audio = sr.AudioFile(input_path)
    with input_audio as source:
        #TODO put duration as parameter
        audio = r.record(source, duration=1200)
        #audio = r.record(source)
    return audio

def recognize_speech(audio_object):
    """Turn audio data into text"""
    logger.info("Start recognizing audio object")
    #TODO put language as parameter
    #speech = r.recognize_google(audio_object, language='de')
    speech = r.recognize_sphinx(audio_object, language='de')
    return speech
    
def write_to_file(string, output_path):
    """Writes a string to a txt file"""
    logger.info("Start writing audio string to txt")
    with open(output_path, "w") as text_file:
        text_file.write(string)





