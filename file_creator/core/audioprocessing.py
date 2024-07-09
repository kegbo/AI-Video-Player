import speech_recognition as sr
from pydub import AudioSegment 
from pydub.silence import split_on_silence
import os
import ffmpeg



#Extract audio from video with URL provided
def extract_audio_from_web_video(Url:str, audioLocation:str):
    pass


#Extract Audio from Video
def extract_audio_from_video(videoLocation:str, audioLocation:str):

    #audio_extract.extract_audio(input_path=videoLocation, output_path=audioLocation,output_format='wav')
    # Load the video file
    input_file = ffmpeg.input(videoLocation)

    # Extract the audio and save it as an MP3 file
    input_file.output(audioLocation, acodec='pcm_s32le').run()


#Transcribe text from audio and save this in a text file
def transcribe_audio_file(audioFileLocation: str) -> str:
    try:
        audioObject = AudioSegment.from_wav(audioFileLocation)
        chunks = split_on_silence(audioObject, min_silence_len=500, silence_thresh=-30, keep_silence=100)
        text = ""
        
        try: 
            os.mkdir('audio_chunks') 
        except(FileExistsError): 
            pass
        
        i = 0
        os.chdir('audio_chunks')

        print(chunks)
        # process each chunk 
        for chunk in chunks: 
            # Create 0.5 seconds silence chunk 
            chunk_silent = AudioSegment.silent(duration=10) 

            # add 0.5 sec silence to beginning and  
            # end of audio chunk. This is done so that 
            # it doesn't seem abruptly sliced. 
            audio_chunk = chunk_silent + chunk + chunk_silent 

            # export audio chunk and save it in  
            # the current directory. 
            print("saving chunk{0}.wav".format(i)) 
            # specify the bitrate to be 192 k 

            audio_chunk.export("./chunk{0}.wav".format(i), bitrate='192k', format="wav") 

            # the name of the newly created chunk 
            filename = 'chunk'+str(i)+'.wav'

            print("Processing chunk "+str(i)) 

            try:
                r = sr.Recognizer()
                # Open the audio file
                with sr.AudioFile(filename) as source:
                    audio_text = r.listen(source)
                    # Recognize the speech in the audio
                    text = text + r.recognize_google(audio_text, language='en-US') + " "
                
            except FileNotFoundError:
                print("AudioFile Not Found")
                raise FileNotFoundError
            
            except sr.UnknownValueError:
                print("Could not understand")

            i += 1
        os.chdir('..') 
        
        return text.strip()
    
    except Exception as e:
        print("Error:", e.args)
        raise Exception


    



