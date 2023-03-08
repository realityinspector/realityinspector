import openai, os

openai.api_key = os.environ["API_KEY"]
if openai.api_key == "SET_ME":
  raise Exception("Please set your OpenAI API key in the Secrets tab")


def summarize(text, max_tokens, prompt):
  try:
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=text + "\n\n" + prompt,
                                        max_tokens=max_tokens,
                                        temperature=0)
    to_return = {}
    to_return["text"] = response["choices"][0]["text"]
    to_return["token_usage"] = response["usage"]["total_tokens"]
    to_return["success"] = True
    #  for t in text.split() if t.strip() != ""
    to_return["word_count"] = len([text.split()])
    return to_return
  except:
    print("Prompt too long, decreasing response tokens by 150")
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=text + "\n\n" + prompt,
                                        max_tokens=max_tokens - 150,
                                        temperature=0)
    to_return = {}
    to_return["text"] = response["choices"][0]["text"]
    to_return["token_usage"] = response["usage"]["total_tokens"]
    to_return["success"] = True
    to_return["word_count"] = len([text.split()])
    return to_return

def token_count(text):
  # a rough estimage of tokens
  return round(len(text.replace(" ", "").replace(",", "").replace(".", "").replace(":", "")) / 4, 2)