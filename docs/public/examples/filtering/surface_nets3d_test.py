#!/usr/bin/env python

# Extract 3D label boundaries using vtkSurfaceNets3D on two small labeled
# volumes: a single voxel and eight adjacent labeled voxels, displayed
# in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkSurfaceNets3D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

VTK_SHORT = 4

# --- First volume: single labeled voxel ---
x_dim_1 = 3
y_dim_1 = 4
z_dim_1 = 5
slice_size_1 = x_dim_1 * y_dim_1

image_1 = vtkImageData()
image_1.SetDimensions(x_dim_1, y_dim_1, z_dim_1)
image_1.AllocateScalars(VTK_SHORT, 1)

scalars_1 = image_1.GetPointData().GetScalars()
scalars_1.Fill(0)

# Region 1: single labeled point
scalars_1.SetTuple1(1 + 1 * x_dim_1 + 1 * slice_size_1, 1)

# Surface nets on single voxel (no smoothing)
surface_nets_1 = vtkSurfaceNets3D()
surface_nets_1.SetInputData(image_1)
surface_nets_1.SetValue(0, 1)
surface_nets_1.GetSmoother().SetNumberOfIterations(0)
surface_nets_1.GetSmoother().SetRelaxationFactor(0.2)
surface_nets_1.GetSmoother().SetConstraintDistance(0.25)
surface_nets_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(surface_nets_1.GetOutputPort())
mapper_1.SetScalarModeToUseCellData()
mapper_1.SelectColorArray("BoundaryLabels")
mapper_1.SetScalarRange(1, 8)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetInterpolationToFlat()

# --- Second volume: eight labeled voxels ---
x_dim_2 = 4
y_dim_2 = 5
z_dim_2 = 6
slice_size_2 = x_dim_2 * y_dim_2

image_2 = vtkImageData()
image_2.SetDimensions(x_dim_2, y_dim_2, z_dim_2)
image_2.AllocateScalars(VTK_SHORT, 1)

scalars_2 = image_2.GetPointData().GetScalars()
scalars_2.Fill(0)

# Eight adjacent regions
scalars_2.SetTuple1(1 + 1 * x_dim_2 + 1 * slice_size_2, 1)
scalars_2.SetTuple1(2 + 1 * x_dim_2 + 1 * slice_size_2, 2)
scalars_2.SetTuple1(1 + 2 * x_dim_2 + 1 * slice_size_2, 3)
scalars_2.SetTuple1(2 + 2 * x_dim_2 + 1 * slice_size_2, 4)
scalars_2.SetTuple1(1 + 1 * x_dim_2 + 2 * slice_size_2, 5)
scalars_2.SetTuple1(2 + 1 * x_dim_2 + 2 * slice_size_2, 6)
scalars_2.SetTuple1(1 + 2 * x_dim_2 + 2 * slice_size_2, 7)
scalars_2.SetTuple1(2 + 2 * x_dim_2 + 2 * slice_size_2, 8)

# Surface nets on eight voxels (no smoothing)
surface_nets_2 = vtkSurfaceNets3D()
surface_nets_2.SetInputData(image_2)
for i in range(8):
    surface_nets_2.SetValue(i, i + 1)
surface_nets_2.GetSmoother().SetNumberOfIterations(0)
surface_nets_2.GetSmoother().SetRelaxationFactor(0.2)
surface_nets_2.GetSmoother().SetConstraintDistance(0.25)
surface_nets_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(surface_nets_2.GetOutputPort())
mapper_2.SetScalarModeToUseCellData()
mapper_2.SelectColorArray("BoundaryLabels")
mapper_2.SetScalarRange(1, 8)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetInterpolationToFlat()

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0, 0, 0)
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(actor_1)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0, 0, 0)
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(actor_2)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(400, 200)
render_window.SetWindowName("surface nets3d test")

# Scene
camera = renderer_1.GetActiveCamera()
camera.SetPosition(-1, 0.9, 0.7)
camera.SetFocalPoint(0, 0, 0)
renderer_1.ResetCamera()
renderer_0.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
