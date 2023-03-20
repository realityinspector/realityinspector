import csv
import os
import glob

def read_data_from_csv(filename):
    data = []
    labels = []

    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        labels = next(reader)  # Read header
        for row in reader:
            try:
                data.append([float(value) for value in row[1:]])
                labels.append(row[0])
            except ValueError:
                continue

    return labels, data

def create_visualization_html(labels, data, output_file):
    html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Data Visualization</title>
<style>
    body {{ font-family: Arial, sans-serif; }}
    .color-container {{ display: flex; flex-wrap: wrap; }}
    .color-box {{
        width: 150px;
        height: 150px;
        margin: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #000;
        border-radius: 5px;
    }}
</style>
</head>
<body>
<h1>Data Visualization</h1>
<div class="color-container">
"""

    html_end = """
</div>
</body>
</html>
"""

    with open(output_file, 'w') as file:
        file.write(html_start)

        for label, row in zip(labels[1:], data):
            if label not in {"Mean", "Average", "Least Frequent", "Top 1", "Top 2", "Top 3", "Top 4", "Top 5", "Top 6"}:
                continue

            if len(row) < 3:
                continue

            rgb = [int(float(value)) for value in row[0:3]]
            color_box = f'<div class="color-box" style="background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});"><span>{label}</span></div>'
            file.write(color_box)

        file.write(html_end)

def main():
    chosen_file = 'rgb_stats.csv'
    if not os.path.exists(chosen_file):
        print(f"Could not find {chosen_file} in the local folder.")
        return

    labels, data = read_data_from_csv(chosen_file)
    create_visualization_html(labels, data, 'data_visualization.html')
    print("Generated data_visualization.html successfully.")

def create_visualization(csv_file):
    labels, data = read_data_from_csv(csv_file)
    create_visualization_html(labels, data, 'data_visualization.html')
