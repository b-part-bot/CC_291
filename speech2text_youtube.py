import os
import subprocess
from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
from pydub.utils import mediainfo
from creds import constants

# Google Cloud credentials
cred_path = "creds/coen291-332f3d95e6a4.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

# YouTube Data API key
YOUTUBE_API_KEY = constants.YOUTUBE_API_KEY
def transcribe_youtube_video(url):
    youtube_url = url
    #"https://www.youtube.com/watch?v=3_dAkDsBQyk"

    # Download YT video as audio
    audio_filename = "audio.mp3"
    download_command = f'yt-dlp -x --audio-format mp3 -o "{audio_filename}" {youtube_url}'
    subprocess.call(download_command, shell=True)

    # Converting audio to mono
    audio = AudioSegment.from_mp3(audio_filename)
    audio = audio.set_channels(1)
    mono_audio_filename = "mono_audio.mp3"
    audio.export(mono_audio_filename, format="mp3")
    sample_rate  = int(mediainfo(mono_audio_filename).get('sample_rate'))
    print(sample_rate)

    # Upload mono to Google Cloud Storage
    bucket_name = "cc_291"
    gsutil_upload_command = f"gsutil cp {mono_audio_filename} gs://{bucket_name}/{mono_audio_filename}"
    subprocess.call(gsutil_upload_command, shell=True)

    # Set up the Speech-to-Text client
    client = speech.SpeechClient()

    # set gcs configuration URI
    audio_uri = f"gs://{bucket_name}/{mono_audio_filename}"
    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code="en-US",
        enable_speaker_diarization=True,
        sample_rate_hertz=sample_rate,

    )

    # transcription operation
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)
    # Extract the speaker diarized transcription
    result = response.results[-1]
    conversation = list()
    words_info = result.alternatives[0].words
    current = words_info[0].speaker_tag
    ongoing = {words_info[0].speaker_tag:[]}
    for word_info in words_info:
        if word_info.speaker_tag != current:
            conversation.append(ongoing)
            ongoing = { word_info.speaker_tag :[] }
            current = word_info.speaker_tag
            ongoing[word_info.speaker_tag].append(word_info.word)
        else:
            ongoing[word_info.speaker_tag].append(word_info.word)
    conversation.append(ongoing)
    transcript = ""
    for converse in conversation:
        transcript+= "Speaker {} : {}".format( list(converse.keys())[0], " ".join(converse[list(converse.keys())[0]]) ) + "\n"
    print(transcript)
    # Clean up audio files
    try:
        # Remove local audio files
        os.remove(audio_filename)
        os.remove(mono_audio_filename)
        
        # Delete the audio file from Google Cloud Storage
        gsutil_delete_command = f"gsutil rm gs://{bucket_name}/{mono_audio_filename}"
        subprocess.call(gsutil_delete_command, shell=True)
        
        print("Files deleted successfully.")
        
    except OSError as e:
        print(f"Error occurred while deleting files: {e}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing gsutil command: {e}")