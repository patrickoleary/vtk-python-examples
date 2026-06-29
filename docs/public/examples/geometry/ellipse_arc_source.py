#!/usr/bin/env python

# Demonstrate vtkEllipseArcSource with specified ratio, angles, and resolution.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkEllipseArcSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Ellipse arc source
source = vtkEllipseArcSource()
source.SetCenter(0.0, 0.0, 0.0)
source.SetRatio(0.25)
source.SetNormal(0.0, 0.0, 1.0)
source.SetMajorRadiusVector(10, 0.0, 0.0)
source.SetStartAngle(20)
source.SetSegmentAngle(250)
source.SetResolution(80)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.3, 0.6, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("ellipse arc source")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
