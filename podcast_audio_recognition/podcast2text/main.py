#!/usr/bin/env python3

import p2t_functions as p2t
import logging 



def main():
    folder_path ="/Users/Potzenhotz/data/podcast_data/"
    file_name ="Mobber_sind_Opfer.mp3"
    mp3_file = folder_path + file_name
    #wav_file = p2t.convert_mp3_to_wav(mp3_file)

    #ONLY FOR DEVELOPMENT
    wav_file = "/Users/Potzenhotz/data/podcast_data/Mobber_sind_Opfer.wav"

    audio_object = p2t.read_audio(wav_file)
    speech = p2t.recognize_speech(audio_object)
    
    output_file_name = "google_Mobber_sind_Opfer.txt"
    output_file_path = folder_path + output_file_name
    p2t.write_to_file(speech, output_file_path)







if __name__ == '__main__':
    from logging.config import fileConfig
    fileConfig('logging_config.ini', disable_existing_loggers=False)
    logger = logging.getLogger()
    main()

