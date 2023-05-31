from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from creds import constants
import speech2text_youtube as s2t_yt
import openai
import image_generation
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
def generate_script():
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
            {"role": "user", "content": "Fix this transcript. Generate a 6 panel comic book in the style of the TV show "+tvshow+". Enforce these requirements in the script:"+customreq+". "+prompt},
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
    
def get_setting_from_prompt(prompt, tvshow, customreq):
    gpt_setting_prompt = [ {"role": "system", "content": "Create a one line setting for each panel for a comic book based on this script: "+prompt+" . Do not include dialogues. Take into account that this is based on the TV show "+tvshow+". Describe what each person is doing from the script provided so that stable diffusion can create a comic book. Include these requirements in your description of the image"+customreq} ]
    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=gpt_setting_prompt
        )
        if(chat.choices[0].message.content):
            reply = chat.choices[0].message.content
            print("Setting from prompt = \n"+reply)
            return reply
        else:
            print("Error retrieving setting from prompt!")
    except Exception as e:
        print(e)

@app.route('/api/generate_comic', methods=['POST'])
def generate_comic():
    print('new req')
    data = request.get_json()
    script = data['script']
    print(script)
    imageModel = data['imageModel']
    print(imageModel)
    tvshow = data['tvshow']
    print(tvshow)
    customreq = data['customReq']
    print(customreq)
    negative_prompt = "Negative prompt: ((((big hands, un-detailed skin, extra panels)))), (((ugly mouth, ugly eyes, missing teeth, crooked teeth, close up, cropped, out of frame)))"
    prompt = "Generate a realistic, high-quality, consistent, sequential-art panel of a comic based on the following transcript."+get_setting_from_prompt(script, tvshow, customreq)+", retro comic style artwork, highly detailed, vibrant, vivid-color,"+negative_prompt
    
    print("generate_comic prompt********************************************************************\n" + prompt)
    if imageModel == 'Stable Diffusion':
        url = image_generation.generate_stableDiffusion_image(prompt)
    if imageModel == 'Kandinsky':
        url = image_generation.generate_kandinsky_image(prompt)
    if imageModel == 'Midjourney':
        url = image_generation.generate_midjourney_image(prompt)
    return jsonify({'url':url, 'status':'200'})

if __name__ == "__main__":
    app.run(debug=True)