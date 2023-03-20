import io
import requests
import time
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class UnicornGame:
    def __init__(self):
        self.score = 0
        self.unicorn_health = 50
        self.root = tk.Tk()
        self.root.title("Unicorn Pet Game")
        self.root.geometry("400x500")
        self.root.resizable(0, 0)
        self.create_widgets()
        self.update_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Create ttk style
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 12))

        # Unicorn image
        self.unicorn_label = ttk.Label(self.root)
        self.unicorn_label.place(x=0, y=50, width=400, height=400)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, mode="determinate")
        self.progress_bar.place(x=0, y=450, width=400, height=20)

        # Score label
        self.score_label = ttk.Label(self.root, text="Score: 0")
        self.score_label.pack(side=tk.LEFT, padx=10)

        # Result label
        self.result_label = ttk.Label(self.root, text="")
        self.result_label.pack(side=tk.LEFT, padx=10)

        # Buttons
        self.feed_button = ttk.Button(self.root, text="Feed Unicorn", command=self.feed_unicorn)
        self.feed_button.place(x=10, y=10, width=120, height=30)

        self.water_button = ttk.Button(self.root, text="Give Water", command=self.give_water)
        self.water_button.place(x=140, y=10, width=120, height=30)

        self.walk_button = ttk.Button(self.root, text="Take Walk", command=self.take_walk)
        self.walk_button.place(x=270, y=10, width=120, height=30)

    def update_widgets(self):
        self.update_score_label()
        self.update_progress_bar()
        self.update_unicorn_image()

    def feed_unicorn(self):
        self.unicorn_health += 10
        self.score += 10
        self.check_win()
        self.update_widgets()

    def give_water(self):
        self.unicorn_health += 5
        self.score += 5
        self.check_win()
        self.update_widgets()

    def take_walk(self):
        self.unicorn_health += 15
        self.score += 15
        self.check_win()
        self.update_widgets()

    def check_win(self):
        if self.unicorn_health >= 100:
            self.result_label.config(text="Congratulations! You have successfully taken care of your unicorn and raised its health to 100. You win!")

    def update_score_label(self):
        self.score_label.config(text="Score: {}".format(self.score))

    def update_progress_bar(self):
        self.progress_bar['value'] = self.unicorn_health
        self.progress_bar['maximum'] = 100


    def update_unicorn_image(self):
        unicorn_opacity = self.unicorn_health / 100.0
        unicorn_color = "blue"

        if self.unicorn_health < 60:
            unicorn_color = "red"
        elif self.unicorn_health < 80:
            unicorn_color = "blue"
        elif self.unicorn_health < 100:
            unicorn_color = "yellow"
        else:
            unicorn_color = "pink"

        unicorn_image_url = "https://raw.githubusercontent.com/realityinspector/unicorn-pet/main/unicorn.png".format(unicorn_color)
        unicorn_image = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get(unicorn_image_url).content)).convert("RGBA"))
        self.unicorn_label.config(image=unicorn_image)
        self.unicorn_label.image = unicorn_image

if __name__ == "__main__":
    game = UnicornGame()
