from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
from direct.task import Task
from math import pi, sin, cos

import sys

class Env(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.src = "../src/"

        self.pandaActor = Actor(self.src + 'human_model/robot')
        # self.pandaActor = Actor('../city-models.obj/lpFemale_casual_A-model.obj')
        self.pandaActor.setScale(10, 10, 10)
        self.pandaActor.setPos(0, 200, -50)
        # self.pandaActor.setHpr(0, 90, 0)
        self.oriarm = None

        tex = Loader.loadTexture(self, self.src + "texture/world_people_colors.png")
        self.pandaActor.setTexture(tex, 1)
        self.dir = 1


        # print(type(self.pandaActor.getJoints()[0]))
        print(self.pandaActor.getJoints())
    
        # self.pandaActor.control_joint(self, self.pandaActor, "bip Pelvis")
        self.node = self.pandaActor.controlJoint(None, "modelRoot", "joint9")
        print(self.node.getHpr())
        print(self.node.getPos())
        # print(self.pandaActor.)
        print(self.oriarm)

        # self.node.setHpr(0, 90, 0)
        # self.node.setPos(10, 10, 10)
        self.taskMgr.add(self.rotate_human, "rotate_human")
        self.pandaActor.reparentTo(self.render)
        self.accept("enter", self.chg)

    def rotate_human(self, task):
        angleDegrees = 1 * self.dir
        # print(angleDegrees, self.oriarm)
        # print(task.time)
        # self.pandaActor.setHpr(angleDegrees, 0, 0)

        self.node.setHpr(self.node, 0, 0, angleDegrees) 
        # self.node.setPos(-angleDegrees, 0, 0) 
        return Task.cont

    def chg(self):
        self.dir *= -1
    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()


