import argparse
import numpy as np
from jina import Document, DocumentArray, Client

# create a Jina client to communicate with the index server
client = Client(port=12345)

def search(query, top_k=5):
    # create a DocumentArray with a single query Document
    query_doc = Document()
    query_doc.embedding = np.random.rand(768).astype('float32') # set a random embedding for the query
    query_doc.text = query
    query_docs = DocumentArray([query_doc])

    # search the index for the query document
    client.search(query_docs, parameters={"top_k": top_k})

    # return the top-k search results
    results = []
    for match in query_doc.matches:
        results.append((match.id, match.scores["dot_product"], match.text))
    return results

if __name__ == '__main__':
    # create a command-line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str, help='the query string')
    parser.add_argument('--top_k', type=int, default=5, help='the number of results to return')
    args = parser.parse_args()

    # perform the search and print the results
    results = search(args.query, args.top_k)
    for result in results:
        print(f"{result[0]} ({result[1]:.2f}): {result[2]}")
