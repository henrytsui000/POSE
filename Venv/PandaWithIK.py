from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
import sys

from CCDIK.ik_chain import IKChain
from CCDIK.ik_actor import IKActor
from CCDIK.utils import *
from CCDIK.camera_control import CameraControl

from direct.showbase.Loader import Loader

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
        self.DebugMode = True
        
        logging.info("Loading model")
        self.path = src + model
        self.model = Actor(os.path.join(self.path, "model.fbx"))
        self.root = render.attach_new_node("Root")
        self.ik_actor = IKActor( self.model, os.path.join(self.path, "texture.jpg"))
        self.ik_actor.reparent_to(self.root)
        
        logging.info("Setup IK chain")
        
        self.target_list = ["LH", "RH"]
        # , "LF", "RF"]
        self.base_dict = {
            "RH" : ("upperarm_r", "upperarm_l"),
            "LH" : ("upperarm_l", "upperarm_r"),
        }
        
        self.chain_list_dict = {"LH" : ["upperarm_l", "lowerarm_l", "hand_l"],
                                "RH" : ["upperarm_r", "lowerarm_r", "hand_r"]}
        self.ik_chain = dict()
        self.ik_target = dict()
        tar = dict()
        for target in self.target_list:
            joint_names = self.chain_list_dict[target]
            self.ik_chain[target] = self.ik_actor.create_ik_chain(joint_names)
            if self.DebugMode:
                self.ik_chain[target].debug_display(line_length=0.5)   
            tar = create_point( thickness=1 )
            self.ik_target[target] = render.attach_new_node(tar)
            
            # for name in joint_names:
            #     self.ik_chain.set_hinge_constraint( name, LVector3f.unit_x(),
            #             min_ang=-math.pi*0.6, max_ang=math.pi*0.6 )
            
            self.ik_chain[target].set_target(self.ik_target[target])
            
        self.task_mgr.add( self.move_target, "MoveTarget")
        self.joint_target = dict()      

        logging.info("Setup camera")
        self.camera_setup()
        
        if self.DebugMode:
            self.debug_setup()
        
    def camera_setup(self, ):        
        self.set_frame_rate_meter(True)
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.cam_control = CameraControl(camera, self.mouseWatcherNode)
        self.taskMgr.add( self.cam_control.move_camera, "MoveCameraTask")
        self.accept( "wheel_down", self.cam_control.wheel_down )
        self.accept( "wheel_up", self.cam_control.wheel_up )
        

    def update_pos_target(self, update_dict):
        if update_dict is not None:
            for joint_name, pos in update_dict.items():
                self.joint_target[joint_name] = pos
        return Task.cont
    
    def move_target(self, task):
        if not "LH" in self.joint_target:
            return Task.cont
        for target in self.target_list:
            joint_tar = self.nor2real(self.joint_target[target], target)
            self.ik_target[target].setPos(joint_tar)
            self.ik_chain[target].update_ik()
        return Task.cont
        
    def get_len(self, vec):
        return math.sqrt(sum(i**2 for i in vec))
    
    def rotate(self, vec, angle):
        px, py, _ = vec
        qx = px * math.cos(angle) - py * math.sin(angle)
        qy = px * math.sin(angle) + py * math.cos(angle)
        return qx, -qy
    
    def vec_to_world(self, vec, bas, ref):
        thetab = math.atan2(bas[1], bas[0])
        x, y = self.rotate(vec, thetab)
        x *= 1.5 * self.get_len(bas)
        y *= 1.5 * self.get_len(bas)
        z = vec[-1] * self.get_len(bas)
        tar = LVector3f(x, y, z) + ref
        return tar
    
    def nor2real(self, normal, target):
        S, T = self.base_dict[target]
        S = self.ik_actor.actor.exposeJoint(None, "modelRoot", S).getPos()
        T = self.ik_actor.actor.exposeJoint(None, "modelRoot", T).getPos()
        bas = S - T
        ret = self.vec_to_world(normal, bas, S)
        return ret
    
    def debug_setup(self,):
        # Debug Function 
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.accept("arrow_up", self.xp)
        self.accept("arrow_up-repeat", self.xp)
        self.accept("arrow_down", self.xn)
        self.accept("arrow_down-repeat", self.xn)
        self.accept("arrow_left", self.yp)
        self.accept("arrow_left-repeat", self.yp)
        self.accept("arrow_right", self.yn)
        self.accept("arrow_right-repeat", self.yn)
        self.accept(".", self.zp)
        self.accept(".-repeat", self.zp)
        self.accept(",", self.zn)
        self.accept(",-repeat", self.zn)
        self.accept("enter", self.rst)
    def rst(self, ): self.dx = self.dy = self.dz = 0
    def xp(self, ): self.dx += 10
    def xn(self, ): self.dx -= 10
    def yp(self, ): self.dy += 10
    def yn(self, ): self.dy -= 10
    def zp(self, ): self.dz += 10
    def zn(self, ): self.dz -= 10

    

    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()
