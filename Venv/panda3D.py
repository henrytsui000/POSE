from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
from direct.task import Task
import json
import os 
import sys

class Env(ShowBase):
    def __init__(self, src="../src/", model = "waiter"):
        super().__init__(self)
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.path = src + model
        self.pandaActor = Actor(os.path.join(self.path, "model.fbx"))
        self.pandaActor.setScale(0.5, 0.5, 0.5)
        self.pandaActor.setPos(0, 200, -50)
        self.pandaActor.setHpr(0, 0, 0)

        tex = Loader.loadTexture(self, os.path.join(self.path, "texture.jpg"))
        self.pandaActor.setTexture(tex, 1)
        self.dir = 0

        print(self.pandaActor.listJoints())

        with open(os.path.join(self.path[1:], "config.json"), "r") as read_config:
            config = json.load(read_config)
        self.joint_list = ["CR", "UAR", "LAR", "CL", "UAL", "LAL"]

        self.joint_dict = dict()
        self.rotate_target = dict()
        for joint_name in self.joint_list:
            self.rotate_target[joint_name] = config[joint_name]["init_degree"]
            self.joint_dict[joint_name] = \
                self.pandaActor.controlJoint(None, "modelRoot",\
                    config[joint_name]["real_joint"])

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
