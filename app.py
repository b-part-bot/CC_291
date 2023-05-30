from flask import Flask, render_template, request
import speech2text_youtube as s2t_yt

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    youtube_url = request.form.get('youtubeURL')
    transcription=""
    # Perform the audio transcription process using the YouTube URL
    transcription = s2t_yt.transcribe_youtube_video(youtube_url)
    # Return the transcription result or redirect to the appropriate page
    print(transcription)
    return render_template('transcribed_text.html', text_transcript=transcription)

if __name__ == "__main__":
    app.run(debug=True)