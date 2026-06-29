#!/usr/bin/env python

# Decimate a sphere using vtkQuadricDecimation with volume
# preservation and regularization, displayed as wireframe.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkQuadricDecimation
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetThetaResolution(70)
sphere.SetPhiResolution(70)
sphere.Update()

print(f"Cells before decimation: {sphere.GetOutput().GetNumberOfCells()}")

# Filter: quadric decimation with regularization
decimator = vtkQuadricDecimation()
decimator.SetInputConnection(sphere.GetOutputPort())
decimator.SetTargetReduction(0.90)
decimator.SetVolumePreservation(True)
decimator.SetRegularize(True)
decimator.SetRegularization(0.05)
decimator.Update()

print(f"Cells after decimation: {decimator.GetOutput().GetNumberOfCells()}")

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(decimator.GetOutputPort())

# Actor (wireframe)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric decimation regularization")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1.5, 1.5, 1.5)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
