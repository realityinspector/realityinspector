import re
import numpy as np
import spacy

# Step 1: read the book text file
with open("book.txt", "r") as f:
    text = f.read()

# Step 2: preprocess the text
text = re.sub(r"[^a-zA-Z0-9\s]+", "", text) # remove special symbols and punctuation
text = re.sub(r"\s+", " ", text) # remove extra spaces
text = text.strip() # remove leading/trailing spaces

# Step 3: split the text into paragraphs or sentences
chunks = text.split("\n\n") # split by double line break for paragraphs, or by period for sentences

# Step 4: tokenize the text
nlp = spacy.load("en_core_web_sm")
tokenized_chunks = []
for chunk in chunks:
    doc = nlp(chunk)
    tokenized_chunk = [token.text for token in doc]
    tokenized_chunks.append(tokenized_chunk)

# Step 5: convert tokens to embeddings
from transformers import GPT2Tokenizer, GPT2Model

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

embeddings = []
for tokenized_chunk in tokenized_chunks:
    input_ids = tokenizer.encode(tokenized_chunk, add_special_tokens=True, return_tensors="pt")
    with torch.no_grad():
        output = model(input_ids)[0]
    embeddings.append(output)

# Step 6: save the processed text and embeddings as training data
np.savez("book_embeddings.npz", embeddings=embeddings)