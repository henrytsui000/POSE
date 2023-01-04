from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task import Task

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
        self.accept('escape', sys.exit)
        self.disableMouse()
        self.set_frame_rate_meter(True)

        # self.
        self.path = src + model
        self.model = Actor(os.path.join(self.path, "model.fbx"))
        tex = Loader.loadTexture(self, os.path.join(self.path, "texture.jpg"))
        self.model.setTexture(tex, 1)
        
        # self.pandaActor = loader.load_model(os.path.join(self.path, "model.fbx"))


        self.root = render.attach_new_node("Root")
        self.root.setPos( 0, 0, 1 )
        self.root.setScale( 0.01 )
        
        # self.model = loader.load_model( "Meshes/Tentacle.bam" )
        # self.model = loader.load_model( "Meshes/person.bam" )
        
        self.ik_actor = IKActor( self.model, os.path.join(self.path, "texture.jpg"))
        print(type(self.ik_actor))
        self.ik_actor.reparent_to(self.root)
        
        print(self.ik_actor.actor.listJoints())



        
        # ["pelvis", "spine_01", "spine_02", "spine_03", 
        joint_names = ["clavicle_l", "upperarm_l", "lowerarm_l", "hand_l"]
        
        # joint_names = []
        # joint_names.append( "Bone" )
        # for i in range(1,8):
        #     joint_names.append( f"Bone.{i:03d}" )
                
        self.ik_chain = self.ik_actor.create_ik_chain( joint_names )
        # for name in joint_names:
        #     self.ik_chain.set_hinge_constraint( name, LVector3f.unit_x(),
        #             min_ang=-math.pi*0.6, max_ang=math.pi*0.6 )
        self.ik_chain.debug_display( line_length=0.5 )   
        
        
        tar = create_point( thickness=10 )
        
        self.ik_target = render.attach_new_node( tar )
        self.ik_target.setPos( 0.7, 0, 2.2)
        
        self.task_mgr.add( self.move_target, "MoveTarget")
        
        self.ik_chain.set_target( self.ik_target )


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
        

        self.cam_control = CameraControl( camera, self.mouseWatcherNode )
        self.taskMgr.add( self.cam_control.move_camera, "MoveCameraTask")

        self.accept( "wheel_down", self.cam_control.wheel_down )
        self.accept( "wheel_up", self.cam_control.wheel_up )

    def move_target( self, task ):
        self.ik_target.setPos(self.dx, self.dy, self.dz)
        self.ik_chain.update_ik()
        return task.cont
    
    def rst(self, ):
        self.dx = self.dy = self.dz = 0
    def xp(self, ):
        self.dx += .10
        print(self.ik_target.getPos())
        
    def xn(self, ):
        self.dx -= .10
        print(self.ik_target.getPos())

    def yp(self, ):
        self.dy += .10
        print(self.ik_target.getPos())

    def yn(self, ):
        self.dy -= .10
        print(self.ik_target.getPos())

    def zp(self, ):
        self.dz += .10
        print(self.ik_target.getPos())

    def zn(self, ):
        self.dz -= .10
        print(self.ik_target.getPos())

    
def main():
    env = Env()
    env.run()
    
if __name__ == "__main__":
    main()
