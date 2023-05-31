import openai
import replicate
import os
import creds.constants as constants
os.environ['REPLICATE_API_TOKEN'] = constants.REPLICATE_API_KEY

openai.api_key = constants.OPENAI_API_KEY

prompt = """  Big bang theory. Generate a comic strip with ((3)) panels based on the following transcript. Peanuts comic style. Stick to the setting.
[Setting: Sheldon and Leonard's apartment. Sheldon, Leonard, Howard, and Raj are present.]  Panel 1: [Leonard holds a container of Pad Thai, addressing the group] LEONARD: There you go, Pad Thai, no peanuts.  
[Panel 2: [Howard looks concerned and asks about peanut oil] HOWARD: But does it have peanut oil?  [Leonard responds while gesturing towards Howard] LEONARD: Uh, I'm not sure. Everyone keep an eye on Howard in case he starts to swell up.  
[Panel 3: [Sheldon chimes in, offering his epinephrine] SHELDON: Since it's not bee season, you can have my epinephrine.  
Cartoon style 
Negative prompt: ((((big hands, un-detailed skin, realistic, extra panels)))), (((ugly mouth, ugly eyes, missing teeth, crooked teeth, close up, cropped, out of frame)))
"""

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

# print('Stable Diffusion -\n',generate_stableDiffusion_image(prompt))
# print('\nKandinsky -\n', generate_kandinsky_image(prompt))
# print('\nDallE -\n',generate_dalle_image(prompt))
# print('\nVariation -\n',variation())