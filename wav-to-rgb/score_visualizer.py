import csv

def read_data_from_csv(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            try:
                time, rgb_value = row
                data.append([time, rgb_value])
            except ValueError:
                continue
    return data

def create_visualization_html(data, output_file):
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
        width: 20px;
        height: 20px;
        margin: 2px;
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

        for row in data:
            if len(row) < 2:
                continue

            rgb = row[1]
            color_box = f'<div class="color-box" style="background-color: rgb{rgb};"></div>'
            file.write(color_box)

        file.write(html_end)

def main():
    chosen_file = 'rgb_scores_time.csv'
    if not os.path.exists(chosen_file):
        print(f"Could not find {chosen_file} in the local folder.")
        return

    data = read_data_from_csv(chosen_file)
    create_visualization_html(data, 'data_visualization.html')
    print("Generated data_visualization.html successfully.")
