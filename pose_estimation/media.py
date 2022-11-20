from mediapipe.framework.formats import landmark_pb2
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
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
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # if PL is None:
        #     continue
        
        # mp_drawing.draw_landmarks(image, PL)

        image = cv2.flip(image, 1)
        # cv2.putText(image, "DA", (10, 160), cv2.FONT_HERSHEY_COMPLEX,
        # 1, (0, 255, 255), 1, cv2.LINE_AA)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
