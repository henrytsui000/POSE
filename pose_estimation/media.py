from mediapipe.framework.formats import landmark_pb2
import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class Pose():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5)

    def inference(self, show=False):
        # while True:
        _, image = self.cap.read()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if results.pose_landmarks:
            PL = landmark_pb2.NormalizedLandmarkList(
            landmark = [
                results.pose_landmarks.landmark[i] for i in range(11, 17)
                ]
            )
        RAL = results.pose_landmarks.landmark[12]
        LAL = results.pose_landmarks.landmark[14]
        UAR = math.degrees(np.arctan2(LAL.y - RAL.y, LAL.x - RAL.x))
        joint_vec = {
            "CR" : UAR, 
        }
        # print(UAR)
        posx, posy = RAL.x, RAL.y
        posx, posy = RAL.x, RAL.y
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())\
        
        h, w, _ = image.shape
        cv2.circle(image, (int(RAL.x*w), int(RAL.y*h)), 20, (0, 0, 255), -1)
        cv2.circle(image, (int(LAL.x*w), int(LAL.y*h)), 20, (0, 255, 0), -1)
        cv2.arrowedLine(image, (int(RAL.x*w), int(RAL.y*h)), (int(RAL.x*w+np.cos(math.radians(UAR))*200), int(RAL.y*h+np.sin(math.radians(UAR))*200)),
                                     (255, 0, 0), 2)
        image = cv2.flip(image, 1)

        if show:
            cv2.imshow('MediaPipe Pose', image)
        cv2.waitKey(5)
        return joint_vec
        

    def __del__(self):
        self.cap.release()

def main():
    pose = Pose()
    # print(ret)
        
    while True:
        ret = pose.inference(show=True)
        print(ret)
        if cv2.waitKey(5) & 0xFF == 27:
            break

if __name__ == "__main__":
    main()