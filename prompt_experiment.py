from flask import jsonify
import openai
import creds.constants as constants
import speech2text_youtube as s2t_yt
import image_generation
openai.api_key = constants.OPENAI_API_KEY

tvshow = "The Office"
customreq = "office show setting, funny, 6 panels"
imageModel = 'Stable Diffusion'

gpt_messages = [ {"role": "system", "content": "You are designed to generate a short and good script for a comic strip based on the transcript input by the user"} ]
def get_transcript(youtube_url):
    try:
        transcription = s2t_yt.transcribe_youtube_video(youtube_url)
    except:
        print("error getting transcript")
    return transcription

def get_script(transcript):

    try:
        gpt_messages.append(
            {"role": "user", "content": "Fix this transcript." +transcript+"Generate a 6 panel comic book in the style of the TV show "+tvshow+". Enforce these requirements in the script:"+customreq},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=gpt_messages
        )
        if(chat.choices[0].message.content):
            reply = chat.choices[0].message.content
            return reply
        else:
            return jsonify({'status':'202'})
    except Exception as e:
        return jsonify({'status':'204', 'e':e})
    
        
def get_panel_script(transcript):
    tvshow = "The Office"
    customreq = "office show setting, funny, 6 panels"
    prompt = get_script(transcript)
    print("script from gpt = \n"+ prompt)

    try:
        gpt_setting_prompt = [{"role": "system", "content": "Create a one line setting for each panel for a comic book based on this script"+prompt+" by the user. Create images based on characters and settings of the TV show" +tvshow+". Create the prompt describing the actions of each person and what they are doing. Include these descriptions of the people "+customreq}]

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=gpt_setting_prompt
        )
        if(chat.choices[0].message.content):
            reply = chat.choices[0].message.content
            return reply
        else:
            print("error getting script from gpt")
    except Exception as e:
        print(e)
        
def generate_comic(request):
    print('new req')
    script = request
    print(script)
    print(imageModel)
    print(tvshow)
    print(customreq)
    negative_prompt = ""
    prompt = "Generate a realistic, high-quality, consistent, sequential-art panel of a comic based on the following transcript."+get_panel_script(script)+negative_prompt
    
    print("generate_comic prompt" + prompt)
    if imageModel == 'Stable Diffusion':
        url = image_generation.generate_stableDiffusion_image(prompt)
    if imageModel == 'Kandinsky':
        url = image_generation.generate_stableDiffusion_image(prompt)
    if imageModel == 'Dall-E':
        url = image_generation.generate_stableDiffusion_image(prompt)
    return url

def main():
    transcript = get_transcript("https://www.youtube.com/watch?v=qHrN5Mf5sgo&ab_channel=Masterou86")
    gpt_panel_script = get_panel_script(transcript)
    print("panel script from gpt = \n"+ gpt_panel_script)
    comic = generate_comic(gpt_panel_script)
    print(comic)
main()