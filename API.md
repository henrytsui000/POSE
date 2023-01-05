# API document
This is the API file to specify how our various components should be built and the specifications for input and output.

# Pose Estiamtion
The name of this category should be called "Pose", and it has at least two functions, \__init__ and inference, \__init__ should initialize all the parameters that must be used. Inference uses the argument show, which represents whether to display the result of pose estiamtion, and the returned value is a dictionary, representing the three-dimensional coordinates of each joint point.

```python
class Pose(...):
    def __init__(self):
        pass
    def inference(self, show=False):
        pass
    def __del__(self):
        pass
```
# MediaPipe
### POSE_WORLD_LANDMARKS
Another list of pose landmarks in world coordinates. Each landmark consists of the following:

x, y and z: Real-world 3D coordinates in meters with the origin at the center between hips.
visibility: Identical to that defined in the corresponding pose_landmarks.

# Env
```python
class Env(...):
    def __init__(self):
        pass
    def run(self):
        pass
```

