import numpy as np
from vispy import visuals, scene
from vispy.visuals.transforms import STTransform

class figure3D():

    def __init__(self, bgcolor='white', size=(800, 600), render=False):
        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor=bgcolor, size=(800, 600), show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.range = 3000
        self.camera_range = [-self.range, self.range]
        self.view.camera.set_range(x=self.camera_range, y=self.camera_range, z=self.camera_range)
        if render == True:
            self.canvas.show(run=True)