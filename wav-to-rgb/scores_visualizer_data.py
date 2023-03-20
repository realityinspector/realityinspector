import csv

def read_data_from_csv(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            try:
                r, g, b = row[1:4]
                rgb_value = f'({r},{g},{b})'
                time = row[0]
                data.append([time, rgb_value])
            except ValueError:
                continue
    return data

def write_data_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'rgb'])
        for row in data:
            writer.writerow(row)

def main():
    chosen_file = 'rgb_scores.csv'
    if not os.path.exists(chosen_file):
        print(f"Could not find {chosen_file} in the local folder.")
        return

    data = read_data_from_csv(chosen_file)
    write_data_to_csv(data, 'rgb_scores_time.csv')
    print("Generated rgb_scores_time.csv successfully.")
