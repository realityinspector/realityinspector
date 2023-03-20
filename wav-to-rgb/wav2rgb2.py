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

def create_visualization_html(labels, data, output_file, csv_files):
    csv_options = ''.join([f'<option value="{csv_file}">{csv_file}</option>' for csv_file in csv_files])

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
<script>
    function loadCsvFile() {{
        var selectedFile = document.getElementById("csvFileSelect").value;
        if (selectedFile) {{
            window.location.href = window.location.pathname + "?file=" + encodeURIComponent(selectedFile);
        }}
    }}
</script>
</head>
<body>
<h1>Data Visualization</h1>
<label for="csvFileSelect">Choose a CSV file:</label>
<select id="csvFileSelect" onchange="loadCsvFile()">
    <option value="">--Select a file--</option>
    {csv_options}
</select>
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
            if len(row) < 3:
                continue

            rgb = [int(float(value)) for value in row[0:3]]
            color_box = f'<div class="color-box" style="background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});"><span>{label}</span></div>'
            file.write(color_box)

        file.write(html_end)

def main():
    csv_files = [os.path.basename(file) for file in glob.glob('*.csv')]

    chosen_file = 'rgb_stats.csv'
    if chosen_file not in csv_files:
        print(f"Could not find {chosen_file} in the local folder.")
        return

    labels, data = read_data_from_csv(chosen_file)
    create_visualization_html(labels, data, 'data_visualization.html', csv_files)
    print("Generated data_visualization.html successfully.")
    
    while True:
        print("Please select a CSV file from the following list:")
        for i, file in enumerate(csv_files, start=1):
            print(f"{i}. {file}")
        choice = int(input("Enter the corresponding number (0 to quit): "))
        if choice == 0:
            break
        chosen_file = csv_files[choice - 1]
        labels, data = read_data_from_csv(chosen_file)
        create_visualization_html(labels, data, 'data_visualization.html', csv_files)
        print(f"Generated data_visualization.html for {chosen_file} successfully.")

if __name__ == '__main__':
    main()
