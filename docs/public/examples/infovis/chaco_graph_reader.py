#!/usr/bin/env python
# Demonstrate vtkChacoGraphReader with circular layout and graph mapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkInfovisLayout import (
    vtkCircularLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkIOInfovis import vtkChacoGraphReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGraphMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Chaco graph file.
reader = vtkChacoGraphReader()
reader.SetFileName(os.path.join(data_dir, "small.graph"))
reader.Update()

# Circular layout.
strategy = vtkCircularLayoutStrategy()

layout = vtkGraphLayout()
layout.SetInputConnection(reader.GetOutputPort())
layout.SetLayoutStrategy(strategy)

# Graph mapper.
mapper = vtkGraphMapper()
mapper.SetInputConnection(layout.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetWindowName("chaco graph reader")

# Scene
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
