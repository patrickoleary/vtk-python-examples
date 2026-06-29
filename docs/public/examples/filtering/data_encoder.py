#!/usr/bin/env python
# Demonstrate vtkDataEncoder encoding a rendered cylinder image to Base64 PNG.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cylinder source.
cylinder = vtkCylinderSource()
cylinder.SetResolution(8)

# Mapper.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cylinder.GetOutputPort())

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)
actor.RotateX(30.0)
actor.RotateY(-45.0)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("data encoder")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
