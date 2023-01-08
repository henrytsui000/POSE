import os
import cv2
import json
import math
import logging
import mediapipe as mp
import sys
sys.path.append("./Tools/")
import our_draw

mp_drawing = mp.solutions.drawing_utils
mp_drawing = our_draw
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
        self.path = "./pose_estimation"
        with open(os.path.join(self.path, "media_config.json"), "r") as read_config:
            self.config = json.load(read_config)
        self.counter = 0    
    
    def im_show(self, cv2_img = None, mat_img = None):
        img = None
        if not (cv2_img is None or mat_img is None):
            img = cv2.vconcat([cv2_img, mat_img])
        elif not cv2_img is None:
            img = cv2_img
        elif not mat_img is None:
            img = mat_img
        if not img.all():
            cv2.imshow("Inference Result", img)
    
    def inference(self, CV2_Show = False, JointPos_Show = False, Loc_Print = False):
        _, image = self.cap.read()
        if image is None:
            return
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if results.pose_landmarks == None:        
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = cv2.flip(image, 1)
            self.im_show(image, None)
            return
        if Loc_Print:
            self.print_joint_pos(results)
        
        # print(type(results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(0).value])) 
        
        joint_info = {
            joint_name : results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(idx).value] 
                        for idx, joint_name in enumerate(self.config["Joint_List"], start=0)
        } 
        for key, (S, T, NS, NT) in self.config["Joint_Vec"].items():
             joint_info[key] = self.joint_to_vec(joint_info[S], joint_info[T], \
                self.joint_to_vec(joint_info[NS], joint_info[NT])) 
                        
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
        image = cv2.flip(image, 1)

        imgS = None
        if JointPos_Show:
            # changes drawing_utils
            if self.counter == 0: 
                img = mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
                imgS = cv2.resize(img, (image.shape[1], image.shape[0]))
                self.imgS = cv2.flip(imgS, 1)
            else: imgS = self.imgS
            imgS = cv2.cvtColor(self.imgS, cv2.COLOR_RGBA2BGR)
            self.counter = (self.counter + 1) % 5
        self.im_show(image if CV2_Show else None, imgS if JointPos_Show else None)
        return joint_info
    
    def print_joint_pos(self, results):
        for i in range(33):
            print(f"{i},{mp_pose.PoseLandmark(i).name}:",
            f"\n{results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value]}")   
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
    
    def innerproduct(self ,vec1_s ,vec1_e ,vec2_s ,vec2_e):
        vec1_s = self.getxyz(vec1_s)
        vec1_e = self.getxyz(vec1_e)
        vec2_s = self.getxyz(vec2_s)
        vec2_e = self.getxyz(vec2_e)
        vec1 = tuple(map(lambda i, j: i - j, vec1_e, vec1_s))
        vec2 = tuple(map(lambda i, j: i - j, vec2_e, vec2_s))
        len_p = self.get_len(vec1) * self.get_len(vec2)
        in_p =  vec1[0]*vec2[0] + vec1[1]*vec2[1]
        cos_theta = in_p / len_p

        return vec1 ,vec2 ,math.acos(cos_theta)


    def joint_to_vec(self, start, end, nor_vec = None) -> tuple:
        start = self.getxyz(start)
        end = self.getxyz(end)
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
        ret = pose.inference(True, True, False) #return joint_vec
        if cv2.waitKey(1) & 0xFF == 27: # ESC=27
            break
    pose.__del__()

if __name__ == "__main__":
    main()
