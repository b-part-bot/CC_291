from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from creds import constants
import speech2text_youtube as s2t_yt
import openai

openai.api_key = constants.OPENAI_API_KEY
app = Flask(__name__)
app.debug = True
CORS(app)
cors = CORS(app, resources={
		r"/*" : {
			"origins" : "*"
		}
	})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe_audio', methods=['POST'])
def transcribe_audio():
    print('new req')
    data = request.get_json()
    youtube_url = data['youtube_url']
    # Perform the audio transcription process using the YouTube URL
    try:
        transcription = s2t_yt.transcribe_youtube_video(youtube_url)
        # Return the transcription result or redirect to the appropriate page
        print(transcription)
        response={'transcription':transcription, 'status':'200'}
    except:
        response={'status':'202'}
    return jsonify(response)

@app.route('/api/generate_script', methods=['POST'])
def generate_gpt_script():
    print('new req')
    data = request.get_json()
    prompt = data['prompt']
    print(prompt)
    tvshow = data['tvshow']
    print(tvshow)
    customreq = data['customReq']
    print(customreq)
    gpt_messages = [ {"role": "system", "content": "You are designed to generate a short and good script for a comic strip based on the transcript input by the user"} ]

    try:
        gpt_messages.append(
            {"role": "user", "content": "Generate a script for a comic strip in the style of the TV show "+tvshow+". It should also be "+customreq+". "+prompt},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=gpt_messages
        )
        if(chat.choices[0].message.content):
            reply = chat.choices[0].message.content
            response = {'script': reply, 'status':'200'}
            return jsonify(response)
        else:
            return jsonify({'status':'202'})
    except Exception as e:
        return jsonify({'status':'204', 'e':e})

if __name__ == "__main__":
    app.run(debug=True)