import os
import torch
from dalle_pytorch import OpenAIDiscreteVAE, DALLE
from PIL import Image
from oai_pass import request_openai_response, write_output_to_file

def generate_image(prompt):
    vae = OpenAIDiscreteVAE()
    dalle = DALLE(vae=vae)

    # Load your DALLE model checkpoint here
    checkpoint_path = "path/to/your/dalle/checkpoint.pt"
    dalle.load_state_dict(torch.load(checkpoint_path))

    # Generate an image using DALLE
    image_tensor = dalle.generate_images(prompt, num_images=1)
    image = Image.fromarray((image_tensor * 255).astype('uint8')[0])

    # Save the generated image
    image.save("generated_image.png")

def main():
    # Replace with the path to your RGB text file
    rgb_text_file = "rgb_colors.txt"
    with open(rgb_text_file, 'r') as file:
        rgb_values = file.read()

    generated_text = request_openai_response(rgb_values)
    write_output_to_file(generated_text)
    print("Generated text:", generated_text)

    generate_image(generated_text)
