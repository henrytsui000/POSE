from mediapipe.framework.formats import landmark_pb2
import cv2
import mediapipe as mp
import numpy as np
import math
import matplotlib.pyplot as plt
import logging


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class Pose():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s %(levelname)-4s %(message)s',
                            datefmt='%m-%d %H:%M',)
        self.cap = cv2.VideoCapture(0)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)   # work as image recognition processor
        
    def inference(self, show=False):
        # while True:
        _, image = self.cap.read()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if results.pose_landmarks == None:
            return
        if results.pose_landmarks:
            PL = landmark_pb2.NormalizedLandmarkList(
                landmark = [
                    results.pose_landmarks.landmark[i] for i in range(0, 33)  # joint number(0:32)
                ])
            # for i in range(0,33):
            #     print(f'{i},{mp_pose.PoseLandmark(i).name}:\n{results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')   
        
        joint_names = ["L_sho","R_sho","L_elb","R_elb","L_wri","R_wri"]
        joint_info = {
            joint_name : results.pose_world_landmarks\
                .landmark[mp_pose.PoseLandmark(idx).value] 
                        for idx, joint_name in enumerate(joint_names, start=11)
        } 
        nor = self.get_len(self.joint_to_vec(joint_info["L_sho"], joint_info["R_sho"]))

        joint_vec_dict = {
            "LH": ("L_sho", "L_wri"),
            "RH": ("R_sho", "R_wri"),
            "LH_U": ("L_sho", "L_elb"),
            "LH_D": ("L_elb", "L_wri"),
            "RH_U": ("R_sho", "R_elb"),
            "RH_D": ("R_elb", "R_wri"),
        }
        for key, (S, T) in joint_vec_dict.items():
            joint_info[key] = self.joint_to_vec(joint_info[S], joint_info[T], nor) 

        # logging.info(joint_info)
        
        # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        h, w, _ = image.shape
        image = cv2.flip(image, 1)
        if show:
            cv2.imshow('MediaPipe Pose', image)
        
        # return normalized joint position
        return joint_info
    
    def getxyz(self, point):
        return point.x, point.y, point.z

    def get_len(self, vec):
        return math.sqrt(sum(i**2 for i in vec))
    
    def joint_to_vec(self, start, end, nor = None) -> tuple:
        start = self.getxyz(start)
        end = self.getxyz(end)
        vec = tuple(map(lambda i, j: i - j, start, end))
        if not nor is None:
            vec = tuple(l/nor for l in vec)
        return vec
    
    def __del__(self):
        self.cap.release()

def main():
    pose = Pose()
    # print(ret)
        
    while True:
        ret = pose.inference(show=True) #return joint_vec
        # print(ret)
        if cv2.waitKey(1) & 0xFF == 27: # ESC=27
            break
    pose.__del__()

if __name__ == "__main__":
    main()


