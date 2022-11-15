from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
import sys

class Env(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.accept('escape', sys.exit)
        self.disableMouse()

        self.pandaActor = Actor('./src/human_model/human.fbx')
        tex = Loader.loadTexture(self, "./src/texture/world_people_colors.png")
        self.pandaActor.setTexture(tex, 1)
        # self.pandaActor.loadTexture()
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        # self.pandaActor.setPos(0, 1000, 0)
        self.pandaActor.reparentTo(self.render)

        self.camera.setPos(0, -150, 50)
        # self.useDrive()

        # self.pandaActor.loop("walk")
        # self.pandaActor.hide



def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()


