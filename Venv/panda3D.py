from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor
from direct.task import Task
import json
import os 
import sys
import logging
import copy

class Env(ShowBase):
    def __init__(self, src="../src/", model = "waiter"):
        super().__init__(self)
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
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
        logging.info("test")

        print(self.pandaActor.listJoints())
        if src == "../src/": src = "./src/"
        self.path = src + model
        with open(os.path.join(self.path, "config.json"), "r") as read_config:
            config = json.load(read_config)
        self.joint_list = ["CR", "UAR", "LAR", "CL", "UAL", "LAL"]
        print(config)
        self.joint_dict = dict()
        self.rotate_target = dict()
        for joint_name in self.joint_list:
            self.rotate_target[joint_name] = config[joint_name]["init_degree"]
            self.joint_dict[joint_name] = \
                self.pandaActor.controlJoint(None, "modelRoot",\
                    config[joint_name]["real_joint"])

        self.taskMgr.add(self.rotate_human_joint, "rotate_human")
        # self.taskMgr.add(self.rotate_human, "rotate_human")
        self.pandaActor.reparentTo(self.render)
        
        self.UAR_t = copy.deepcopy(self.joint_dict["LAR"])
        logging.info("success deepcopy uar")
        print(self.UAR_t.getPos())
        
        # Debug Function
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.accept("arrow_up", self.xp, ["CR"])
        self.accept("arrow_up-repeat", self.xp, ["CR"])
        self.accept("arrow_down", self.xn, ["CR"])
        self.accept("arrow_down-repeat", self.xn, ["CR"])
        self.accept("arrow_left", self.yp, ["CR"])
        self.accept("arrow_left-repeat", self.yp, ["CR"])
        self.accept("arrow_right", self.yn, ["CR"])
        self.accept("arrow_right-repeat", self.yn, ["CR"])
        self.accept(".", self.zp, ["CR"])
        self.accept(".-repeat", self.zp, ["CR"])
        self.accept(",", self.zn, ["CR"])
        self.accept(",-repeat", self.zn, ["CR"])
        self.accept("enter", self.rst)

    def rst(self, ):
        self.dx = self.dy = self.dz = 0
    def xp(self, joint_name):
        self.dx += 10
        print(self.dx, self.dy, self.dz)
    def xn(self, joint_name):
        self.dx -= 10
        print(self.dx, self.dy, self.dz)
    def yp(self, joint_name):
        self.dy += 10
        print(self.dx, self.dy, self.dz)
    def yn(self, joint_name):
        self.dy -= 10
        print(self.dx, self.dy, self.dz)
    def zp(self, joint_name):
        self.dz += 10
        print(self.dx, self.dy, self.dz)
    def zn(self, joint_name):
        self.dz -= 10
        print(self.dx, self.dy, self.dz)


    def rotate_human(self, task):
        self.pandaActor.setHpr(self.pandaActor, 1, 0, 0)
        return Task.cont

    def update_pos_target(self, update_dict):
        print(update_dict)
        if update_dict is not None:
            for joint_name, pos in update_dict.items():
                self.rotate_target[joint_name] = pos  # *deg
        return Task.cont

    def rotate_human_joint(self, task):
        self.rotate_target = dict()
        self.rotate_target["LAR"] = (self.dx, self.dy, self.dz)
        
        for joint_name in ["LAR"]:
            vec_tmp = self.UAR_t.getPos() + self.rotate_target[joint_name]
            self.joint_dict[joint_name].setPos(vec_tmp)
        return Task.cont

    def test_rotate_human_joint(self, task):
        angleDegrees = 1 * self.dir
        pose = (0, 0, angleDegrees)
        self.node.setHpr(*pose) 
        return Task.cont

    def chg(self):
        self.dir += 30
        # print(self.dir)
        self.rotate_target["CR"] = (0, self.dir, 0)

    def command(self, args):
        print(args)

    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()
