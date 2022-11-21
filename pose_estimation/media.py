from mediapipe.framework.formats import landmark_pb2
import cv2
import mediapipe as mp
import numpy as np

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
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())\

        image = cv2.flip(image, 1)
        if show:
            cv2.imshow('MediaPipe Pose', image)
        cv2.waitKey(5)

    def __del__(self):
        self.cap.release()

def main():
    pose = Pose()
    while True:
        pose.inference(show=True)
        if cv2.waitKey(5) & 0xFF == 27:
            break

if __name__ == "__main__":
    main()