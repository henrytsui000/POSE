import multiprocessing as mp 
from threading import Thread
import logging
import time
import cv2

import sys
# sys.path.insert(1, "./panda")

from panda.Venv import Env
from pose_estimation.media import Pose

class controller():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.env = Env("./src/")
        self.pe = Pose()
        self.Plist = [
            Thread(target = self.penv, args = ()),
            Thread(target = self.ppe , args = ())
        ]
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
        time.sleep(5)
        self.env.chg()
        # self.env.run()
        

    def ppe(self, ):
        """
        This is the function which get the human pose estimation

        you don't need give parameters, after run __init__ all the parameters would save in self        
        """
        logging.info("Start running PE")
        while True:
            self.pe.infernce(show=True)
            if cv2.waitKey(5) & 0xFF == 27:
                break

def main():
    env = controller()
    env.run()
    
if __name__ == "__main__":
    main()