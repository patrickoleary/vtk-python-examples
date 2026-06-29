#!/usr/bin/env python
# Demonstrate serialization round-trip of a simple sphere rendering pipeline.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source.
sphere = vtkSphereSource()

# Mapper.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("single update")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
