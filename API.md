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

# Env
```python
class Env(...):
    def __init__(self):
        pass
    def run(self):
        pass
```