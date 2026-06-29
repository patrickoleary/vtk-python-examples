#!/usr/bin/env python

# Demonstrate vtkGlyph3DMapper with edge visibility on sphere glyphs.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Plane with elevation coloring
plane = vtkPlaneSource()
plane.SetResolution(1, 1)

colors = vtkElevationFilter()
colors.SetInputConnection(plane.GetOutputPort())
colors.SetLowPoint(-1, -1, -1)
colors.SetHighPoint(0.5, 0.5, 0.5)

# Sphere glyph source
sphere = vtkSphereSource()
sphere.SetPhiResolution(5)
sphere.SetThetaResolution(9)

# Glyph mapper
glypher = vtkGlyph3DMapper()
glypher.SetInputConnection(colors.GetOutputPort())
glypher.SetScaleFactor(1.2)
glypher.SetSourceConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(glypher)
actor.GetProperty().SetEdgeVisibility(1)
actor.GetProperty().SetEdgeColor(1.0, 0.5, 0.5)

# Rendering pipeline
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper edges")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

interactor.Initialize()
interactor.Start()
