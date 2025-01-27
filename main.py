from assembly import GameAssembly
from pygame import event

assembly = GameAssembly()

while True:
    assembly.update()
    assembly.draw()
    for e in event.get():
        assembly.emit(e)
