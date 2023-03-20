import openai
import os
import tensorflow as tf
import numpy as np

# Set up your OpenAI API key
openai.api_key = os.environ["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"]

# Load your book embeddings
with np.load('book_embeddings-2.npz') as data:
    embeddings = data['embeddings']

# Normalize your embeddings
embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)

# Set up the OpenAI GPT-3 model and parameters
model_engine = "text-davinci-002"
params = {
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

# Ask the user to choose an option
while True:
    option = input("Choose an option:\n1. Summarize the whole book\n2. Ask a question\nEnter 1 or 2: ")
    if option == "1" or option == "2":
        break

if option == "1":
    # Summarize the whole book
    prompt = "Summarize the whole book using the embeddings."
    input_embedding = embeddings.mean(axis=0)
    prompt_embedding = input_embedding.tolist()
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=params["temperature"],
        max_tokens=params["max_tokens"],
        top_p=params["top_p"],
        frequency_penalty=params["frequency_penalty"],
        presence_penalty=params["presence_penalty"],
        inputs={
            "embedding": prompt_embedding,
            "data": embeddings.tolist()
        }
    )

    # Print the book summary and save it to a file
    book_summary = response.choices[0].text.strip()
    print(book_summary)
    with open("summary_results.txt", "w") as f:
        f.write(book_summary)

elif option == "2":
    # Ask a question and generate an answer
    while True:
        # Get user input
        question = input("Ask a question (type 'quit' to exit): ")
        
        # Stop the loop if the user enters "quit"
        if question.lower() == "quit":
            break
        
        # Generate an answer using the OpenAI API
        prompt = f"Answer the question: {question}"
        prompt_embedding = tf.keras.preprocessing.sequence.pad_sequences(
            [embeddings.mean(axis=0)], maxlen=1024, dtype='float32', padding='post'
        )
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=params["temperature"],
            max_tokens=params["max_tokens"],
            top_p=params["top_p"],
            frequency_penalty=params["frequency_penalty"],
            presence_penalty=params["presence_penalty"],
            inputs={
                "embedding": prompt_embedding.tolist(),
                "data": embeddings.tolist()
            }
        )
        
        # Print the answer and save it to a file
        answer = response.choices[0].text.strip()
        print(answer)
        with open("question_results.txt", "a") as f:
            f.write(f"Question: {question}\nAnswer: {answer}\n\n")
