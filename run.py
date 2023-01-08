import multiprocessing as mp 
from threading import Thread
import logging
import time
import cv2

import sys
# sys.path.insert(1, "./panda")

from Venv.PandaWithIK import Env
from pose_estimation.media import Pose

class controller():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.env = Env("./src/", debug=False)
        self.pe = Pose()
        self.Plist = [
            Thread(target = self.penv, args = ()),
            Thread(target = self.ppe , args = ())
        ]
        self.human_pose = None
    def run(self):
        # self.env.run()
        logging.info("Start thread")
        for p in self.Plist:
            p.start()
        logging.info("Run main Thread")
        self.env.run()
        logging.info("End thread, joining thread")
        for p in self.Plist:
            p.join()

    def penv(self,):
        """
        This is the function which maintain the panda3d environemt        
        """
        logging.info("Start running ENV")
        while self.env.running:
            self.env.update_pos_target(self.human_pose)
            time.sleep(5e-2)
        logging.info("Stop running, Closing all process...")


    def ppe(self, ):
        """
        This is the function which get the human pose estimation

        you don't need give parameters, after run __init__ all the parameters would save in self        
        """
        logging.info("Start running PE")
        while self.env.running:
            self.human_pose = self.pe.inference(True, True, False)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

def main():
    env = controller()
    env.run()
    
if __name__ == "__main__":
    main()