import io
import os
from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio_with_speaker_diarization(audio_file):
    # Set up Google Cloud credentials
    credentials_path = "C:/Users/bhara/OneDrive - scu.edu/Code Projects/CC/CC_291/coen291-332f3d95e6a4.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    # Instantiates a client
    client = speech.SpeechClient()

    # Read audio file
    with io.open(audio_file, "rb") as audio_data:
        content = audio_data.read()

    # Configure the audio settings
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Number of speakers (change accordingly)
        language_code="en-US",
    )

    # Perform the transcription with speaker diarization
    response = client.recognize(config=config, audio=audio)

    # Parse the response and extract the transcriptions
    results = response.results
    for result in results:
        alternative = result.alternatives[0]
        print(f"Transcript: {alternative.transcript}")
        print(f"Confidence: {alternative.confidence}")
        if alternative.words:
            for word in alternative.words:
                speaker_tag = word.speaker_tag
                print(f"Word: {word.word}")
                print(f"Speaker Tag: {speaker_tag}")

if __name__ == "__main__":
    audio_file_path = "C:/Users/bhara/OneDrive - scu.edu/Code Projects/CC/CC_291/mc56.mp3"
    transcribe_audio_with_speaker_diarization(audio_file_path)
