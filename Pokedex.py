import tkinter as tk
import pathlib
import pygubu
from PIL import Image, ImageTk
from io import BytesIO
import pokebase as pb
import requests

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Pokedex.ui"


class PokedexApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

        self.pokemon_name = builder.get_object("poke_entry_box", master)

    def run(self):
        self.mainwindow.mainloop()

    def search(self):
        pokemon_name = self.pokemon_name.get().lower()
        pokemon = pb.pokemon(pokemon_name)
        img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png"
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        self.builder.get_object("poke_img_label").config(image=photo)
        self.builder.get_object("poke_img_label").image = photo

        poke_number = self.builder.get_object("poke_number_label", self.mainwindow)
        poke_number.config(text=f"#{pokemon.id}")

        poke_types = self.builder.get_object("poke_type_label", self.mainwindow)
        poke_types.config(text="Type: " + ", ".join([t.type.name for t in pokemon.types]))

        self.mainwindow.geometry(f"{img.width + 20}x{img.height + 170}")

if __name__ == "__main__":
    app = PokedexApp()
    app.run()
