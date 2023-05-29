from flask import Flask, render_template, request
from app import app
import speech2text_youtube as s2t_yt
@app.route('/generate_comic', methods=['POST'])
def generate_comic():
    youtube_url = request.form.get('youtubeURL')
    text_transcript = request.form.get('textTranscript')
    tv_show = request.form.get('address')
    custom_requirements = request.form.get('customReq')
    gpt_edit_script = request.form.get('gptEditScript')
    model = request.form.get('model')

    # Process the form data and generate the comic
    
    return render_template('result.html')  # Replace 'result.html' with the appropriate template for displaying the comic
