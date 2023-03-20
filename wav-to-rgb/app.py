from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from wav2rgb import process_audio_file
from visualizer import create_visualization
from rgb2txt import read_rgb_values_from_csv, write_rgb_values_to_txt
from oai_pass import request_openai_response

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/process_wav', methods=['POST'])
def process_wav():
    if request.method == 'POST':
        wav_file = request.files['wav_file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], wav_file.filename)
        wav_file.save(file_path)

        process_audio_file(file_path)
        create_visualization("rgb_stats.csv")

        csv_file = "rgb_stats.csv"
        rgb_values = read_rgb_values_from_csv(csv_file)
        txt_file = "rgb_colors.txt"
        write_rgb_values_to_txt(rgb_values, txt_file)

        return jsonify({"rgb_values": rgb_values})

@app.route('/send_to_openai', methods=['POST'])
def send_to_openai():
    if request.method == 'POST':
        txt_file = request.json['txt_file']

        with open(txt_file, 'r') as file:
            rgb_values = file.read()

        generated_text = request_openai_response(rgb_values)

        return jsonify({"generated_text": generated_text})

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index route called") 
    if request.method == 'POST':
        return process_wav()
    return render_template('index.html')

@app.route('/uploads/<path:subpath>')
def serve_uploads(subpath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], subpath)

@app.route('/visualization')
def visualization():
    return send_from_directory('.', 'data_visualization.html')

if __name__ == '__main__':
    app.run(debug=True)
