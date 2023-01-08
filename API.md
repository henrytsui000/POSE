# API document
This is the API file to specify how our various components should be built and the specifications for input and output.

# Pose Estiamtion
The name of this class should be called "Pose", and it has at least two functions, \__init__ and inference, \__init__ should initialize all the parameters that must be used. Inference uses the argument show, which represents whether to display the result of pose estiamtion, and the returned value is a dictionary, representing the three-dimensional coordinates of each joint point.
Please note that when the inference in this class is called, it should only inference the screen captured by the current webcam, instead of enabling video streaming or endless loop.

```python
class Pose(...):
    def __init__(self):
        pass
    def inference(self, show=False) -> dict:
        return dict
    def __del__(self):
        pass
```

# Virtual Environment
If you want to inherit the panda3d environment with other environments, please implement the following functions:
- \__init__ : Renders the entire virtual environment and places the puppet on the map.
- update_pos_target: When the external program calls him, it will give you a dict corresponding to the person in the actual scene, and the position of each joint in the 3D coordinate game. The detailed dictionary contents are described in the next paragraph.
- move_func: This has no explicit name definition, hopefully you will be able to move the joints to the correct position.
- self.running: Indicates whether the virtual environment continues to run. When you close the game engine, you should set this variable to false, and other image recognition models will be automatically closed.
```python
class Env(...):
    def __init__(self):
        self.running -> bool
    def update_pos_target(self, update_dict -> dict):
        pass
    def __del__(self):
        pass
```
# Human Joint Location
The following provides an example of dict. In the above-mentioned position of the person in the real-time environment, the keys of the dictionary are basically named according to such rules, "{torso name}{left and right torso}" or more detailed "{torso name }{left and right torso}_{torso up and down}". For example, the left upper arm will be: L, H, U, which is "HL_U"; the right leg will be: L, F, which is "FL".
```json
{
    "HR" : [
        x_vec, y_vec, z_vec
    ],
    "HL" : [
        x_vec, y_vec, z_vec
    ],
    ...
}
```