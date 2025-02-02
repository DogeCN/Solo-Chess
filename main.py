from assembly import GameAssembly
from pygame import event
import os

os.environ["SDL_IME_SHOW_UI"] = "1"

assembly = GameAssembly()

while True:
    assembly.update()
    assembly.draw()
    for e in event.get():
        assembly.emit(e)
