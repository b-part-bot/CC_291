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
        audio_channel_count = 2,
        #sample_rate_hertz=speech.RecognitionConfig.AudioEncoding.SAMPLE_RATE_UNSPECIFIED,
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Number of speakers (change accordingly)
        language_code="en-US",
    )

    # Perform the transcription with speaker diarization
    response = client.recognize(config=config, audio=audio)
    print(response.results)
    # Parse the response and extract the transcriptions
    current_speaker = 1
    conversation = []
    for result in response.results:
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        confidence = alternative.confidence
        speaker_tag = alternative.words[0].speaker_tag

        if speaker_tag != current_speaker:
            conversation.append(f"Speaker {speaker_tag}: {transcript}")
            current_speaker = speaker_tag
        else:
            conversation.append(transcript)

    conversation_text = "\n".join(conversation)
    print(conversation_text)

if __name__ == "__main__":
    audio_file_path = "C:/Users/bhara/OneDrive - scu.edu/Code Projects/CC/CC_291/Audio/dialog1.mp3"
    transcribe_audio_with_speaker_diarization(audio_file_path)
