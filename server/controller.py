import multiprocessing as mp 
from threading import Thread
import logging
import time

import sys
sys.path.insert(1, "./panda")

from Venv import Env

class controller():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.env = Env()
        self.Plist = [
            Thread(target = self.penv, args = ()),
            Thread(target = self.ppe , args = ())
        ]
    def run(self):
        # self.env.run()
        for p in self.Plist:
            p.start()
        for p in self.Plist:
            p.join()
        self.env.run()

    def penv(self,):
        """
        This is the function which maintain the panda3d environemt        
        """
        logging.info("Start running ENV")

    def ppe(self, ):
        """
        This is the function which get the human pose estimation

        you don't need give parameters, after run __init__ all the parameters would save in self        
        """
        logging.info("Start running PE")


def main():
    env = controller()
    env.run()
    
if __name__ == "__main__":
    main()