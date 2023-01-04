from mediapipe.framework.formats import landmark_pb2
import cv2
import mediapipe as mp
import numpy as np
import math
import matplotlib.pyplot as plt



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class Pose():
    def __init__(self):
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
            for i in range(0,33):
                print(f'{i},{mp_pose.PoseLandmark(i).name}:\n{results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value]}')   
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
        
        joint_names = ["L_sho","R_sho","L_elb","R_elb","L_wri","R_wri"]
        joint_info = {
            joint_name : results.pose_world_landmarks\
                .landmark[mp_pose.PoseLandmark(idx).value] 
                        for idx, joint_name in enumerate(joint_names, start=11)
        } 
        # print(UAR)
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
        # return joint_vec
        return joint_info
        

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


