# the npz file should contain two arrays:
# - embeddings: a numpy array of shape (N, D) where N is the number of embeddings and D is the dimension of the embeddings
# - names: a numpy array of shape (N,) where N is the number of embeddings and names[i] is the name of the i-th embedding

import numpy as np
import flask
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = flask.Flask(__name__)

@app.route("/")
def viz_page():
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/metrics", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.array(data["embedding"])
    # Put the result in a nice dict so we can send it as json
    results = {"distance": np.linalg.norm(x - embeddings, axis=1)}
    return flask.jsonify(results)

@app.route("/plot", methods=["POST"])
def plot():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.array(data["embedding"])
    # Put the result in a nice dict so we can send it as json
    results = {"distance": np.linalg.norm(x - embeddings, axis=1)}
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(names, results["distance"])
    axis.set_ylabel("Distance")
    axis.set_title("Distance from query")
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = flask.make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == "__main__":
    # Load the embeddings
    with np.load("book_embeddings.npz") as data:
        embeddings = data["embeddings"]
        names = data["names"]
    # Start the server, continuously listen to requests.
    app.run(host='0.0.0.0', port=7222)
