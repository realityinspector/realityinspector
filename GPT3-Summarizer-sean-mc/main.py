from functions.Summarizer import summarize
from functions.Splitter import split
from datetime import datetime
import shutil, math, os
"""
OpenAI text summarization tool

To run:
- Set API_KEY in the Secrets tab
- Paste a large block of text into input.txt
- Change the variables below as desired
- Run the repl

Output:
- recursive_summaries contains the iterations of the summary (iter-0 folder being initial summary, everything else after that being a summary of summaries)
- output.txt contains the summary
- There will also be a brief summary of the run at the bottom including time taken to run in seconds and token usage.

Recent changes:
- Changed summary method to a recursive summary
- Added output to recursive_summaries for intermediate steps
- Added test mode for debugging
- Added split_chunks output for text chunks
"""

# prompt sent to GPT3: {text} + prompt
# text ~= WORD_COUNT words
# OpenAI response tokens: MAX_RESPONSE_TOKENS
# 1900 words/1000 tokens seems to work well
WORD_COUNT = 1900
MAX_RESPONSE_TOKENS = 1000
# max loops to summarize text
MAX_ITERATIONS = 3
# paragraphs/bullet points (done by newlines)
DESIRED_LENGTH = 15
# test mode:
TEST_MODE = False
# for summarizing text: {text} +
PROMPT = """Summarize the above into five bullet points:"""
# for summarizing summaries: {block of summaries} +
SUMMARY_PROMPT = """Summarize the above into 5 bullet points:"""


def clear(folder):
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print('Failed to delete %s. Reason: %s' % (file_path, e))


def chunk_(text, words):
  words = text.split()
  chunks = math.floor(len(words) / WORD_COUNT) + 1
  out = ""
  if chunks != 0:
    for i in range(chunks):
      try:
        out += " ".join(words[i * WORD_COUNT:(i + 1) * WORD_COUNT])
        out += "[to_split]"
      except:
        out += " ".join(words[i * WORD_COUNT:])
        out += "[to_split]"
  return out.split("[to_split]")


token_count = 0


def recursive_summary(summaries=[], iter=0):
  global token_count
  if TEST_MODE:
    print("---- TEST MODE ----")
  print("recursive_summaries, iteration %s" % iter)
  print("Word count: " + str(len(("\n".join(summaries)).split())))
  if summaries == []:
    print("Summarizing input.txt...")
    with open("input.txt") as file:
      text = file.read()
    print("input.txt word count: " + str(len(text.split())))
    chunks = chunk_(text, WORD_COUNT)
    summaries = []
    for i, chunk in enumerate(chunks):
      print("Summarizing chunk %s of %s" % (i + 1, len(chunks)))
      if TEST_MODE:
        summaries.append(chunk[:250] + "\n" + chunk[250:500] + "\n" +
                         chunk[500:750] + "\n" + chunk[750:1000] + "\n" +
                         chunk[1000:1250])
      else:
        data = summarize(chunk, MAX_RESPONSE_TOKENS, PROMPT)
        token_count += data["token_usage"]
        summaries.append(data["text"])
    os.makedirs(f"recursive_summaries/iter-{iter}", exist_ok=True)
    for i, s in enumerate(summaries):
      with open(f"recursive_summaries/iter-{iter}/chunk{i+1}.txt",
                "w") as file:
        file.write(s)
    return recursive_summary(summaries=summaries, iter=iter + 1)
  elif iter > MAX_ITERATIONS:
    print("Reached max loops...")
    return "\n\n".join(summaries)
  elif summaries != []:
    print("Summarizing summaries passed in...")
    # concat summaries
    summaries_block = ""
    for summary in summaries:
      summaries_block += summary + "\n"
    tmp = [t.strip() for t in summaries_block.split("\n") if t.strip() != ""]
    if len(tmp) <= DESIRED_LENGTH:
      print("Length is less than or equal to the desired length, returning...")
      return summaries_block
    # split by word count
    summaries = chunk_(summaries_block, WORD_COUNT)
    # todo: rename
    summaries_ = []
    # summarize each chunk and add to summaries_
    for i, summary in enumerate(summaries):
      print("Summarizing chunk %s of %s" % (i + 1, len(summaries)))
      if TEST_MODE:
        summaries_.append(summary[:250] + "\n" + summary[250:500] + "\n" +
                          summary[500:750] + "\n" + summary[750:1000] + "\n" +
                          summary[1000:1250])
      else:
        data = summarize(summary, MAX_RESPONSE_TOKENS, SUMMARY_PROMPT)
        summaries_.append(data["text"])
        token_count += data["token_usage"]

    os.makedirs(f"recursive_summaries/iter-{iter}", exist_ok=True)
    for i, s in enumerate(summaries_):
      with open(f"recursive_summaries/iter-{iter}/chunk{i+1}.txt",
                "w") as file:
        file.write(s)

    tmp = "\n".join(summaries_)
    tmp = tmp.split("\n")
    tmp = [t.strip() for t in tmp if t.strip() != ""]
    if len(tmp) <= DESIRED_LENGTH:
      print(
        "Length is less than or equal to the desired length after summarization, returning..."
      )
      return "\n".join(summaries_)
    else:
      print("Another round of summarization...")
      return recursive_summary(summaries=tmp, iter=iter + 1)


clear("recursive_summaries")
clear("split_chunks")
split("file", WORD_COUNT)

print(
  "Folders with intermediate summaries will be created at the end of each iteration (after all chunks have been summarized)"
)
t1 = datetime.now()
data = recursive_summary()
t2 = datetime.now()
print("\n\n" + data + "\n\n")
# remove blank lines
data = "\n".join([t for t in data.split("\n") if t.strip() != ""])
with open("output.txt", "w") as file:
  file.write(data)
print("\n\n----\nSummary:")
print("output.txt contains the summary.")
print("Token usage: " + str(token_count))
print("Time (seconds): " + str((t2 - t1).seconds))
print("Test mode:", TEST_MODE)
