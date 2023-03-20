import requests
import json
import os
import subprocess
import sys

def call_openai_api(prompt):
    api_key = "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"
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
      "prompt": f"Please provide a Python script that {prompt}:\n\n```python\n{{CODE}}\n```\n",
        "n": 1,
        "stop": None,
        "temperature": 0.7,
        "max_tokens": 100
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["text"]

def create_client_py(code):
    with open("client.py", "w") as f:
        f.write(code)

def create_and_activate_venv():
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    if os.name == "nt":
        return "venv\\Scripts\\activate"
    else:
        return ". venv/bin/activate"

def run_client_py():
    result = subprocess.run(["python", "client.py"], capture_output=True, text=True)
    if result.stderr:
        error = result.stderr.strip()
        return False, error
    else:
        return True, None

def main():
    user_prompt = input("What do you need an app to do? ")
    code = call_openai_api(user_prompt)
    create_client_py(code)

    activate_command = create_and_activate_venv()
    print(f"Run the following command to activate the virtual environment:\n{activate_command}")

    success, error = run_client_py()
    while not success:
        print(f"Error found: {error}\nPlease fix the error in 'client.py' and press ENTER to continue.")
        input()
        success, error = run_client_py()

if __name__ == "__main__":
    main()