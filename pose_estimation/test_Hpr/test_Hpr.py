from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.actor.Actor import Actor

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()
        self.environment = loader.loadModel("./environment")
        self.environment.reparentTo(render)

        self.tempActor = Actor("./act_p3d_chan", {"walk" : "./a_p3d_chan_run"})
        self.tempActor.reparentTo(render)

        self.tempActor.setPos(0, 7, 0)
        # self.tempActor.getChild(0).setR(90)
        # self.tempActor.getChild(0).setP(60)
        self.tempActor.getChild(0).setH(60)

        
game = Game()
game.run()