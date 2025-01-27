from assembly import GameAssembly
from pygame import event

assembly = GameAssembly()

while True:
    for e in event.get():
        assembly.emit(e)
    assembly.update()
    assembly.draw()
    assembly.clock.tick()
