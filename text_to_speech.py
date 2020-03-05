# Import the required module for text  
# to speech conversion 
from gtts import gTTS
import time
  
# This module is imported so that we can  
# play the converted audio 
import os
# 
# def tts():
# # The text that you want to convert to audio 
#     mytext = "Enrollment completed... "
#       
#     # Language in which you want to convert 
#     language = 'en-GB'
#       
#     # Passing the text and language to the engine,  
#     # here we have marked slow=False. Which tells  
#     # the module that the converted audio should  
#     # have a high speed 
#     myobj = gTTS(text=mytext, lang=language, slow=False) 
#       
#     # Saving the converted audio in a mp3 file named 
#     # welcome
#     myobj.save("ttsfiles/EnrollmentSuccess.mp3") 
#       
#     # Playing the converted file 
#     os.system("mpg321 ttsfiles/EnrollmentSuccess.mp3")
# 
# tts()
def tts(s, filename, c = 0):
# The text that you want to convert to audio
    uid_length = 36
    position = s.index("usr")
    uid = s[position: position + uid_length]
    new_s = s.replace(uid, "")
    if c == 0:
        mytext = new_s
    else:
        mytext = new_s + "... attempt {0}".format(c)
      
    # Language in which you want to convert 
    language = 'en-GB'
      
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=mytext, lang=language, slow=False) 
      
    # Saving the converted audio in a mp3 file named 
    # welcome
    fs = filename+".mp3"
    myobj.save("ttsfiles/fs") 
      
    # Playing the converted file 
    os.system("mpg321 ttsfiles/fs") 

