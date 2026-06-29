#!/usr/bin/env python
# Demonstrate vtkRemoteInteractionAdapter processing events on a cone scene.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Cone source.
cone = vtkConeSource()

# Mapper.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("remote interaction adapter")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
