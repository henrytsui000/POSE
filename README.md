# POSE

# Project Demo

# Contents

- [POSE](#pose)
- [Contents](#contents)
- [Build Environment](#build-environment)
- [Overview](#overview)
- [CheckList](#checklist)
- [Citation](#citation)

# Build Environment

```bash
$conda create -n POSE python=3.8
$conda activate POSE
$pip install -r requirements.txt
# If you aren't M1 user, use this:
# $pip install mediapipe
# If you are M1 user, use this:
# $pip install mediapipe-silicon
```

# Let's Start!

## How to run our project :

```bash
$python run.py
```

## If you only want to check out the results of Pose Estimation, run :

```bash
$python pose_estimation/media.py
```

## If you only want to check out the results of panda3D engine, run :

```bash
$python Venv/PandaWithIK.py
```

# Project Architecture

![image](./src/image/arc.png)

- Capture the action of real people through the webcam.
- Use pose estimation to capture location of the joints.
- Using 3D engine as a platform, and built a virtual reality.

# Project Platform
- We use  RTX3090 and Ub2 22.04 to develop.
- Can be deploy on Mac M1, Win11, Jatson Nano...
- Need a webcam to capture images. (Ours: Logitech C615 HD)

# Methods
## 3D Pose Estimaiton

## 3D Virtual Engine
# Future Work

# Citation / License

Thanks to Mediapipe and panda3D developers for providing us with a good development environment, so that we can stand on the shoulders of giants and make a project that satisfies us. At the same time, I would like to thank the netizens in the panda3d community for their enthusiastic responses to questions on the 3D model and GitHub for providing the basis for inverse kinematics.

The LICENSE of this github code is Apache 2.0 license, all developers are welcome to use or test our project, or provide valuable comments.
