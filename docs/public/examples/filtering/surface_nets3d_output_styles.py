#!/usr/bin/env python

# Extract 3D label boundaries using vtkSurfaceNets3D with different output
# styles: selected label faces and boundary-only faces, displayed in two
# viewports.

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
x_dim = 4
y_dim = 5
z_dim = 6
slice_size = x_dim * y_dim

# Create a small volume with 8 labeled regions
image = vtkImageData()
image.SetDimensions(x_dim, y_dim, z_dim)
image.AllocateScalars(VTK_SHORT, 1)

scalars = image.GetPointData().GetScalars()
scalars.Fill(0)

# Eight adjacent labeled regions
scalars.SetTuple1(1 + 1 * x_dim + 1 * slice_size, 1)
scalars.SetTuple1(2 + 1 * x_dim + 1 * slice_size, 2)
scalars.SetTuple1(1 + 2 * x_dim + 1 * slice_size, 3)
scalars.SetTuple1(2 + 2 * x_dim + 1 * slice_size, 4)
scalars.SetTuple1(1 + 1 * x_dim + 2 * slice_size, 5)
scalars.SetTuple1(2 + 1 * x_dim + 2 * slice_size, 6)
scalars.SetTuple1(1 + 2 * x_dim + 2 * slice_size, 7)
scalars.SetTuple1(2 + 2 * x_dim + 2 * slice_size, 8)

# --- Viewport 0: selected label (label 1 only) ---
surface_nets_0 = vtkSurfaceNets3D()
surface_nets_0.SetInputData(image)
for i in range(8):
    surface_nets_0.SetValue(i, i + 1)
surface_nets_0.GetSmoother().SetNumberOfIterations(0)
surface_nets_0.GetSmoother().SetRelaxationFactor(0.2)
surface_nets_0.GetSmoother().SetConstraintDistance(0.25)
surface_nets_0.SetOutputStyleToSelected()
surface_nets_0.AddSelectedLabel(1)
surface_nets_0.Update()

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(surface_nets_0.GetOutputPort())
mapper_0.SetScalarModeToUseCellData()
mapper_0.SelectColorArray("BoundaryLabels")
mapper_0.SetScalarRange(1, 8)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetInterpolationToFlat()

# --- Viewport 1: boundary faces (triangles) ---
surface_nets_1 = vtkSurfaceNets3D()
surface_nets_1.SetInputData(image)
for i in range(8):
    surface_nets_1.SetValue(i, i + 1)
surface_nets_1.GetSmoother().SetNumberOfIterations(0)
surface_nets_1.GetSmoother().SetRelaxationFactor(0.2)
surface_nets_1.GetSmoother().SetConstraintDistance(0.25)
surface_nets_1.SetOutputMeshTypeToTriangles()
surface_nets_1.SetOutputStyleToBoundary()
surface_nets_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(surface_nets_1.GetOutputPort())
mapper_1.SetScalarModeToUseCellData()
mapper_1.SelectColorArray("BoundaryLabels")
mapper_1.SetScalarRange(1, 8)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetInterpolationToFlat()

# Two viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0, 0, 0)
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0, 0, 0)
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(actor_1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(400, 200)
render_window.SetWindowName("surface nets3d output styles")

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
