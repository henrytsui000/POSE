from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
from direct.task import Task

import sys

class JointPose():
    def __init__(self,):
        self.Joint = {

        }
    def __getitem__(self,):
        self.ps = 3
    def __len__(self):
        pass
    def get(self):


class Env(ShowBase):
    def __init__(self, src="../src/"):
        super().__init__(self)
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.src = src
        self.pandaActor = Actor("../src/rp_eric_rigged_001_FBX/rp_eric_rigged_001_ue4.fbx")
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        self.pandaActor.setPos(0, 200, -50)
        self.pandaActor.setHpr(-60, 0, 0)
        self.oriarm = None

        tex = Loader.loadTexture(self, self.src + "rp_eric_rigged_001_FBX/tex/rp_eric_rigged_001_dif.jpg")
        self.pandaActor.setTexture(tex, 1)
        self.dir = 1

        print(self.pandaActor.listJoints())
    
        self.node = self.pandaActor.controlJoint(None, "modelRoot", "upperarm_r")
        self.taskMgr.add(self.rotate_human, "rotate_human")
        self.pandaActor.reparentTo(self.render)
        self.accept("enter", self.chg)

    def rotate_human(self, task):
        angleDegrees = 1 * self.dir
        self.node.setHpr(self.node, 0, 0, angleDegrees) 
        return Task.cont

    def chg(self):
        self.dir *= -1

    def command(self, args):
        print(args)

    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()


