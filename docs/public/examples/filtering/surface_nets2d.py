#!/usr/bin/env python

# Extract 2D label boundaries using vtkSurfaceNets2D on a manually
# created labeled image with four regions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkSurfaceNets2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a small labeled image
VTK_SHORT = 4
row_len = 10
image = vtkImageData()
image.SetDimensions(row_len, 7, 1)
image.AllocateScalars(VTK_SHORT, 1)

scalars = image.GetPointData().GetScalars()
scalars.Fill(0)

# Region 1
for i, j in [(0,2),(1,2),(2,2),(3,0),(3,1),(3,2),(3,3),(4,1),(3,2),(4,2),(4,3)]:
    scalars.SetTuple1(i + j * row_len, 1)

# Region 2
for i, j in [(5,2),(6,2),(5,3)]:
    scalars.SetTuple1(i + j * row_len, 2)

# Region 3
for i, j in [(3,4),(4,4),(4,5)]:
    scalars.SetTuple1(i + j * row_len, 3)

# Region 4
for i, j in [(5,4),(6,4),(5,5),(6,5),(7,5),(8,5),(7,6),(8,6),(9,6)]:
    scalars.SetTuple1(i + j * row_len, 4)

# Extract boundaries of labels 1-4 with SurfaceNets (no smoothing)
surface_nets = vtkSurfaceNets2D()
surface_nets.SetInputData(image)
surface_nets.SetValue(0, 1)
surface_nets.SetValue(1, 2)
surface_nets.SetValue(2, 3)
surface_nets.SetValue(3, 4)
surface_nets.GetSmoother().SetNumberOfIterations(0)
surface_nets.GetSmoother().SetRelaxationFactor(0.2)
surface_nets.GetSmoother().SetConstraintDistance(0.25)
surface_nets.ComputeScalarsOff()
surface_nets.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface_nets.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("surface nets2d")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
