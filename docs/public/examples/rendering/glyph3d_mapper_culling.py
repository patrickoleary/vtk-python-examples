#!/usr/bin/env python

# Demonstrate vtkGlyph3DMapper with culling and LOD on a plane of sphere glyphs.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Plane with glyphs
plane = vtkPlaneSource()
plane.SetResolution(10, 10)

sphere = vtkSphereSource()
sphere.SetPhiResolution(10)
sphere.SetThetaResolution(10)
sphere.SetRadius(0.05)

# Glyph mapper with culling and LOD
glypher = vtkGlyph3DMapper()
glypher.SetInputConnection(plane.GetOutputPort())
glypher.SetSourceConnection(sphere.GetOutputPort())
glypher.SetCullingAndLOD(True)
glypher.SetNumberOfLOD(2)
glypher.SetLODDistanceAndTargetReduction(0, 18.0, 0.2)
glypher.SetLODDistanceAndTargetReduction(1, 20.0, 1.0)
glypher.SetLODColoring(True)

actor = vtkActor()
actor.SetMapper(glypher)

# Rendering pipeline
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper culling")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().Azimuth(45.0)
renderer.GetActiveCamera().Roll(20.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
