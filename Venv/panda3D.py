from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
from direct.task import Task

import sys

class Env(ShowBase):
    def __init__(self, src="../src/"):
        super().__init__(self)
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.src = src
        self.pandaActor = Actor(self.src + "rp_eric_rigged_001_FBX/rp_eric_rigged_001_ue4.fbx")
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        self.pandaActor.setPos(0, 200, -50)
        self.pandaActor.setHpr(0, 0, 0)
        self.oriarm = None

        tex = Loader.loadTexture(self, self.src + "rp_eric_rigged_001_FBX/tex/rp_eric_rigged_001_dif.jpg")
        self.pandaActor.setTexture(tex, 1)
        self.dir = 1

        print(self.pandaActor.listJoints())

        joint_trans = {
            "UAR": "upperarm_r",
            "LAR": "lowerarm_r",
            "UAL": "upperarm_l",
            "LAL": "lowerarm_l",
        }

        self.joint_dict = dict()
        self.rotate_target = dict()
        self.joint_list = ["UAR", "UAL", "LAR", "LAL"]
        for joint_name in self.joint_list:
            self.rotate_target[joint_name] = (60, 30, 90)
            self.joint_dict[joint_name] = \
                self.pandaActor.controlJoint(None, "modelRoot", joint_trans[joint_name])

        self.node = self.pandaActor.controlJoint(None, "modelRoot", "upperarm_r")
        self.taskMgr.add(self.rotate_human_joint, "rotate_human")
        self.pandaActor.reparentTo(self.render)
        
        # Debug Function
        self.accept("enter", self.chg)


    def update_pos_target(self, update_dict):
        self.joint = update_dict

    def rotate_human_joint(self, task):
        for joint_name in self.joint_list:
            self.joint_dict[joint_name].setHpr(*self.rotate_target[joint_name])
        return Task.cont

    def test_rotate_human_joint(self, task):
        angleDegrees = 1 * self.dir
        pose = (0, 0, angleDegrees)
        self.node.setHpr(*pose) 
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


