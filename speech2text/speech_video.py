import os
from google.cloud import speech

def transcribe_model_selection_gcs(gcs_uri, model):
    """Transcribe the given audio file asynchronously with
    the selected model."""
    credentials_path = "C:/Users/bhara/OneDrive - scu.edu/Code Projects/CC/CC_291/coen291-332f3d95e6a4.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
        model=model,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=10
        )
    )
    conversation = list()

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    for word_info in words_info:
        print(
            f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}"
        )


if __name__ == "__main__":
    # Provide the necessary arguments when calling the function
    gcs_uri = "gs://cc_291/audio-files/The Big Bang Theory Active Listening - english sub.mp3"
    model = "latest_long"
    transcribe_model_selection_gcs(gcs_uri, model)
