import openai
import matplotlib.pyplot as plt

# Set up OpenAI API credentials
openai.api_key = "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"

# Ask the user for the prompt text
prompt_text = input("What do you want to visualize? ")

# Generate the Matplotlib code for the visual metaphor using GPT-3-Turbo
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt_text + "\nGenerate Matplotlib code for the visualization:\n",
    max_tokens=512,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated Matplotlib code from the response
matplotlib_code = response.choices[0].text.strip()

# Clean up the code by removing any string literals and non-Python code
python_code = ""
for line in matplotlib_code.split("\n"):
    if '"' in line:
        line = line.split('"')[0]
    if line.startswith("#") or line.startswith(" "):
        continue
    python_code += line + "\n"

# Render the visualization using Matplotlib
exec(python_code)

plt.show()

