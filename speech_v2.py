import io

import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="CC_291\coen291-332f3d95e6a4.json"

from google.cloud import speech_v1p1beta1 as speech
from tqdm import tqdm
client = speech.SpeechClient()

conversation = list()
audio_file = "C:/Users/bhara/OneDrive - scu.edu/Code Projects/CC/CC_291/Audio/dialog1.mp3"
with io.open(audio_file, "rb") as audio_data:
    content = audio_data.read()
audio = speech.types.RecognitionAudio(content=content)

config = speech.types.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    sample_rate_hertz=16000,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=2)

response = client.recognize(config=config, audio=audio)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words
current = words_info[0].speaker_tag
# Printing out the output:
ongoing = {words_info[0].speaker_tag:[]}
for word_info in words_info:
    #print("word: '{}', speaker_tag: {}".format(word_info.word,word_info.speaker_tag))
    if word_info.speaker_tag != current:
        conversation.append(ongoing)
        ongoing = { word_info.speaker_tag :[] }
        current = word_info.speaker_tag
        ongoing[word_info.speaker_tag].append(word_info.word)
    else:
        ongoing[word_info.speaker_tag].append(word_info.word)
conversation.append(ongoing)
for converse in conversation:
    print( "Speaker {} : {}".format( list(converse.keys())[0], " ".join(converse[list(converse.keys())[0]]) ) )