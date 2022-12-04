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
        self.pandaActor = Actor(self.src + "human_model/waiter.fbx")
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        self.pandaActor.setPos(0, 200, -50)
        self.pandaActor.setHpr(0, 0, 0)
        self.oriarm = None

        tex = Loader.loadTexture(self, self.src + "texture/waiter.jpg")
        self.pandaActor.setTexture(tex, 1)
        self.dir = 0

        print(self.pandaActor.listJoints())

        joint_trans = {
            "CR" : "clavicle_r",
            "UAR": "upperarm_r",
            "LAR": "lowerarm_r",

            "CL" : "clavicle_l",
            "UAL": "upperarm_l",
            "LAL": "lowerarm_l",
        }

        init_joint = {
            "CR" : ( 180, 0, 90),
            "UAR": ( 0, 0, 0),
            "LAR": ( 0, 0, 0),

            "CL" : ( 0, 0, 90),
            "UAL": ( 0, 0, 0),
            "LAL": ( 0, 0, 0),
        }

        self.joint_dict = dict()
        self.rotate_target = dict()
        self.joint_list = ["CR", "UAR", "LAR", "CL", "UAL", "LAL"]
        for joint_name in self.joint_list:
            self.rotate_target[joint_name] = init_joint[joint_name]
            self.joint_dict[joint_name] = \
                self.pandaActor.controlJoint(None, "modelRoot", joint_trans[joint_name])

        self.taskMgr.add(self.rotate_human_joint, "rotate_human")
        self.taskMgr.add(self.rotate_human, "rotate_human")
        self.pandaActor.reparentTo(self.render)
        
        # Debug Function
        self.accept("enter", self.chg)

    def rotate_human(self, task):
        self.pandaActor.setHpr(self.pandaActor, 1, 0, 0)
        return Task.cont

    def update_pos_target(self, update_dict):
        self.joint = update_dict
        return Task.cont

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
        self.dir += 30
        print(self.dir)
        self.rotate_target["CR"] = (self.dir, 0, 90)

    def command(self, args):
        print(args)

    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()


