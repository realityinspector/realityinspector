import openai
openai.api_key = "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"

# create a new dataset
dataset_name = "my-book-dataset"
openai.Dataset.create(name=dataset_name)

# upload your book to the dataset
book_file = open("input.txt", "r")
book_text = book_file.read()
openai.Dataset.create_version(dataset_name, data=[book_text], file_type="text/plain")
