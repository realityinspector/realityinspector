import math, os


def console_in():
  print("Enter/Paste your content (press CTRL+D when done):")
  contents = []
  while True:
    try:
      line = input()
    except EOFError:
      break
    contents.append(line)
  return "\n".join(contents)


def file_in(filename):
  with open(filename) as file:
    return file.read()


def split(INPUT_TYPE, WORD_COUNT, print_summary=False):
  for file in os.listdir("split_chunks"):
    os.remove("split_chunks/" + file)
  out = ""
  in_ = ""
  if INPUT_TYPE == "file":
    in_ = file_in("input.txt")
  elif INPUT_TYPE == "console":
    in_ = console_in()
  else:
    raise Exception(
      "Please set INPUT_TYPE to be one of the following: ['file', 'console']")
  words = in_.split(" ")
  chunks = math.floor(len(words) / WORD_COUNT) + 1
  if chunks != 0:
    for i in range(chunks):
      try:
        out += " ".join(words[i * WORD_COUNT:(i + 1) * WORD_COUNT])
        out += "[to_split]"
      except:
        out += " ".join(words[i * WORD_COUNT:])
        out += "[to_split]"
  else:
    out = " ".join(words) + "[to_split]"
  out = out.split("[to_split]")
  out = [i for i in out if i != ""]

  os.system("clear")
  for i, chunk in enumerate(out):
    with open("split_chunks/chunk_" + str(i + 1) + ".txt", "w") as file:
      if chunk.strip() != "":
        file.write(chunk)
  # for i, chunk in enumerate(out):
  #   print("\n\n------\nChunk %s:" % (i + 1))
  #   print(chunk)
  if print_summary:
    print("----\n\nSummary:\nOutput types:")
    print("""- New file for each chunk: "output" folder
  - Entire output split by "----": output.txt
  - Entire output split by "----": console output""")
    print("--")
    if INPUT_TYPE == "file":
      print("Input type: File (input.txt)")
    else:
      print("Input type: Console (copy/paste)")
    print("Change input type at the top of main.py")
    print("--")
    print("Words per chunk: " + str(WORD_COUNT) +
          " (change in main.py at the top)")
    print("Word count: " + str(len(words)))
    if chunks != 0:
      print("Chunks: " + str(chunks))
    else:
      print("Chunks: 1")
