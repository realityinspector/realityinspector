import csv

def read_rgb_values_from_csv(csv_file):
    rgb_values = []
    with open(csv_file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for row in data[1:]:
            r, g, b = int(float(row[1])), int(float(row[2])), int(float(row[3]))
            rgb_values.append(f"({r},{g},{b})")
    return rgb_values

def write_rgb_values_to_txt(rgb_values, output_file):
    with open(output_file, 'w') as file:
        file.write(','.join(rgb_values))

def main():
    csv_file = "rgb_stats.csv"
    output_file = "rgb_colors.txt"
    rgb_values = read_rgb_values_from_csv(csv_file)
    write_rgb_values_to_txt(rgb_values, output_file)
    print(f"RGB color values have been written to {output_file}")
