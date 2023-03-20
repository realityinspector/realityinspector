from PIL import Image, ImageDraw

# Create a new image
im = Image.new("RGB", (500, 200))

# Create a draw object
draw = ImageDraw.Draw(im)

# Define the colors of the rainbow
colors = [
    (255, 0, 0),    # Red
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211)   # Violet
]

# Draw the rainbow
for i in range(len(colors)):
    draw.rectangle([(i * 70, 0), (i * 70 + 70, 200)], fill=colors[i])

# Save the image
im.save("rainbow.png")
