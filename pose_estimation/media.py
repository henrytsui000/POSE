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
            self.print_joint_pos(shows = False)
            
        joint_names = ["L_sho","R_sho","L_elb","R_elb","L_wri","R_wri"]
        joint_info = {
            joint_name : results.pose_world_landmarks\
                .landmark[mp_pose.PoseLandmark(idx).value] 
                        for idx, joint_name in enumerate(joint_names, start=11)
        } 
        # nor_vec = self.joint_to_vec("NOR",joint_info["L_sho"], joint_info["R_sho"])

        joint_vec_dict = {
            "LH": ("L_sho", "L_wri", "R_sho", "L_sho"),
            "RH": ("R_sho", "R_wri", "L_sho", "R_sho"),
            "LH_U": ("L_sho", "L_elb", "R_sho", "L_sho"),
            "LH_D": ("L_elb", "L_wri", "R_sho", "L_sho"),
            "RH_U": ("R_sho", "R_elb","L_sho", "R_sho"),
            "RH_D": ("R_elb", "R_wri","L_sho", "R_sho"),
            # "NOR" : ("L_sho", "R_sho")
        }
        for key, (S, T, NS, NT) in joint_vec_dict.items():
            joint_info[key] = self.joint_to_vec(key,joint_info[S], joint_info[T], \
                self.joint_to_vec("NOR",joint_info[NS], joint_info[NT])) 

        # logging.debug(joint_info["NOR"])
        
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
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
    
    def draw_3d_landmarks(self):
        return
    def print_joint_pos(self, shows):
        if shows is True:
            for i in range(0,33):
                print(f'{i},{mp_pose.PoseLandmark(i).name}:\n{results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')   
        return

    def getxyz(self, point):
        return point.x, -point.y, -point.z

    def get_len(self, vec):
        return math.sqrt(sum(i**2 for i in vec))
    
    def rotate(self, vec, theta, z):
        px, _, py = vec
        qx = px * math.cos(theta)-py * math.sin(theta)
        qy = px * math.sin(theta)+py * math.cos(theta)
        return qx, qy, z


    def joint_to_vec(self,key, start, end, nor_vec = None) -> tuple:
        start = self.getxyz(start)
        print(key,start)
        end = self.getxyz(end)
        print(key,end)
        vec = tuple(map(lambda i, j: i - j, end, start))
        if not nor_vec is None:
            nor = self.get_len((nor_vec[0], nor_vec[2]))   
            vec = tuple(l/nor for l in vec)
            theta = math.atan2(nor_vec[2], nor_vec[0])
            vec = self.rotate(vec, -theta, vec[1])
        return vec
    
    def __del__(self):
        self.cap.release()

def main():
    pose = Pose()
        
    while True:
        ret = pose.inference(show=True) #return joint_vec
        if cv2.waitKey(1) & 0xFF == 27: # ESC=27
            break
    pose.__del__()

if __name__ == "__main__":
    main()


