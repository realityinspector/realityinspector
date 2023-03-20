import os
import csv
import svgwrite
import numpy as np
from cairosvg import svg2png
from faker import Faker

def generate_pokemon_name(fake):
    return fake.word().capitalize()


def generate_pokemon_shapes(dwg, rng):
    num_shapes = rng.integers(3, 7)
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

    for _ in range(num_shapes):
        shape_type = rng.choice(['circle', 'rect'])
        color = rng.choice(colors)
        pos_x, pos_y = rng.integers(20, 80, size=2)
        size = rng.integers(10, 40)

        if shape_type == 'circle':
            dwg.add(dwg.circle(center=(pos_x, pos_y), r=size, fill=color))
        elif shape_type == 'rect':
            dwg.add(dwg.rect(insert=(pos_x, pos_y), size=(size, size), fill=color))


def save_drawing_as_png(dwg, filename):
    png_data = svg2png(bytestring=dwg.tostring())
    with open(filename, 'wb') as f:
        f.write(png_data)

def generate_pokemon_name(fake):
    return fake.word().capitalize()


def generate_pokemon_shapes(dwg, rng):
    num_shapes = rng.integers(3, 7)
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

    for _ in range(num_shapes):
        shape_type = rng.choice(['circle', 'rect'])
        color = rng.choice(colors)
        pos_x, pos_y = rng.integers(20, 80, size=2)
        size = rng.integers(10, 40)

        if shape_type == 'circle':
            dwg.add(dwg.circle(center=(pos_x, pos_y), r=size, fill=color))
        elif shape_type == 'rect':
            dwg.add(dwg.rect(insert=(pos_x, pos_y), size=(size, size), fill=color))


def save_drawing_as_png(dwg, filename):
    png_data = svg2png(bytestring=dwg.tostring())
    with open(filename, 'wb') as f:
        f.write(png_data)

fake = Faker()
rng = np.random.default_rng()

if not os.path.exists('pokemon_images'):
    os.makedirs('pokemon_images')

with open('pokemon_data.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Name', 'Filename'])

    for i in range(24):
        name = generate_pokemon_name(fake)
        dwg = svgwrite.Drawing(size=(100, 100))

        generate_pokemon_shapes(dwg, rng)
        
        filename = f'pokemon_images/{name}.png'
        save_drawing_as_png(dwg, filename)
        csv_writer.writerow([name, filename])

if __name__ == "__main__":
    game = UnicornGame()