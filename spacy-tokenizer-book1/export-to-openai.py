import openai
import numpy as np

openai.api_key = "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"

# Load embeddings from .npz file
with np.load("book_embeddings.npz", allow_pickle=True) as data:
    embeddings = data["embeddings"]
    names = data["names"]

# Upload embeddings to OpenAI
response = openai.api.create_dataset(
    name="book_embeddings",
    files={
        "embeddings": embeddings.tobytes(),
        "names": names.tobytes()
    }
)

# Check the response
print(response)
