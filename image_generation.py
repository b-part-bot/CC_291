import openai
import replicate
import os
import creds.constants as constants
os.environ['REPLICATE_API_TOKEN'] = constants.REPLICATE_API_KEY

openai.api_key = constants.OPENAI_API_KEY

prompt = "Generate a 6 paneled comic strip based on the following transcript"
def generate_dalle_image(prompt):
    try:
        if prompt:
            response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512",
                )
            return response['data'][0]['url']
    except Exception as e: 
        print(e) 
        return "There was an issue in generating the image. Please try again later"

def variation():
    try:
        response = openai.Image.create_variation(
        image=open("out-0.png", "rb"),
        n=1,
        size="1024x1024"
        )
        return response['data'][0]['url']
    except Exception as e: 
        print(e) 
        return "There was an issue in generating the image. Please try again later"

def generate_kandinsky_image(prompt):
    try:
        output = replicate.run(
            "ai-forever/kandinsky-2:601eea49d49003e6ea75a11527209c4f510a93e2112c969d548fbb45b9c4f19f",
            input={"prompt": prompt}
        )
        return output
    except Exception as e: 
        print(e) 
        return "There was an issue in generating the image. Please try again later"

def generate_stableDiffusion_image(prompt):
    try: 
        output = replicate.run(
            "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": prompt}
        )
        return output    
    except Exception as e: 
        print(e) 
        return "There was an issue in generating the image. Please try again later"
    
def generate_midjourney_image(prompt):
    try: 
        output = replicate.run(
            "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b",
            input={"prompt": prompt}
        )
        return output    
    except Exception as e: 
        print(e) 
        return "There was an issue in generating the image. Please try again later"