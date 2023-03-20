import os
import openai

api_key = "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"
openai.api_key = api_key

def request_openai_response(prompt):
    prompt_instruction = (
        "You are a helpful AI who receives colors in RGB values and returns a list of the same colors in very descriptive english words. Here are the rgb values: /n"
        + prompt +
        "."
    )

    
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt_instruction,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.6,
    )

    text = response.choices[0].text.strip()
    return text

def write_output_to_file(output_text):
    with open("output.txt", "w") as output_file:
        output_file.write(output_text)

def main():
    input_file = "rgb_colors.txt"

    with open(input_file, "r") as file:
        rgb_values = file.read()

    response_text = request_openai_response(rgb_values)
    write_output_to_file(response_text)
    print("Generated text:", response_text)

