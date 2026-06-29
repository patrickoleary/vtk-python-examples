#!/usr/bin/env python

# Demonstrate vtkProjectPointsToPlane with six projection types (X, Y, Z,
# best fit, specified, best coordinate) on a tilted disk, rendered in a
# 3x2 viewport grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersPoints import vtkProjectPointsToPlane
from vtkmodules.vtkFiltersSources import vtkDiskSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
res = 10
normal = [0.8, 0.9, 1]

# Create a tilted disk
disk = vtkDiskSource()
disk.SetInnerRadius(1)
disk.SetOuterRadius(9)
disk.SetRadialResolution(res)
disk.SetCircumferentialResolution(4 * res)
disk.SetCenter(10, 20, 30)
disk.SetNormal(normal)
disk.Update()
print("Disk Center: ", disk.GetOutput().GetCenter())
print("Disk Normal: ", normal)

# --- X plane projection ---
projection_0 = vtkProjectPointsToPlane()
projection_0.SetInputConnection(disk.GetOutputPort())
projection_0.SetProjectionTypeToXPlane()

projection_mapper_0 = vtkPolyDataMapper()
projection_mapper_0.SetInputConnection(projection_0.GetOutputPort())

projection_actor_0 = vtkActor()
projection_actor_0.SetMapper(projection_mapper_0)
projection_actor_0.GetProperty().SetRepresentationToWireframe()
projection_actor_0.GetProperty().SetColor(1, 1, 1)

# --- Y plane projection ---
projection_1 = vtkProjectPointsToPlane()
projection_1.SetInputConnection(disk.GetOutputPort())
projection_1.SetProjectionTypeToYPlane()

projection_mapper_1 = vtkPolyDataMapper()
projection_mapper_1.SetInputConnection(projection_1.GetOutputPort())

projection_actor_1 = vtkActor()
projection_actor_1.SetMapper(projection_mapper_1)
projection_actor_1.GetProperty().SetColor(1, 1, 1)
projection_actor_1.GetProperty().SetRepresentationToWireframe()

# --- Z plane projection ---
projection_2 = vtkProjectPointsToPlane()
projection_2.SetInputConnection(disk.GetOutputPort())
projection_2.SetProjectionTypeToZPlane()

projection_mapper_2 = vtkPolyDataMapper()
projection_mapper_2.SetInputConnection(projection_2.GetOutputPort())

projection_actor_2 = vtkActor()
projection_actor_2.SetMapper(projection_mapper_2)
projection_actor_2.GetProperty().SetColor(1, 1, 1)
projection_actor_2.GetProperty().SetRepresentationToWireframe()

# --- Best fitting plane ---
projection_3 = vtkProjectPointsToPlane()
projection_3.SetInputConnection(disk.GetOutputPort())
projection_3.SetProjectionTypeToBestFitPlane()
projection_3.Update()
print("Origin: ", projection_3.GetOrigin())
print("Normal: ", projection_3.GetNormal())

projection_mapper_3 = vtkPolyDataMapper()
projection_mapper_3.SetInputConnection(projection_3.GetOutputPort())

projection_actor_3 = vtkActor()
projection_actor_3.SetMapper(projection_mapper_3)
projection_actor_3.GetProperty().SetColor(1, 1, 1)
projection_actor_3.GetProperty().SetRepresentationToWireframe()

# --- Specified plane ---
spec_normal = [0.1, 0.2, 0.4]
projection_4 = vtkProjectPointsToPlane()
projection_4.SetInputConnection(disk.GetOutputPort())
projection_4.SetProjectionTypeToSpecifiedPlane()
projection_4.SetOrigin(1, 1, 1)
projection_4.SetNormal(spec_normal)

projection_mapper_4 = vtkPolyDataMapper()
projection_mapper_4.SetInputConnection(projection_4.GetOutputPort())

projection_actor_4 = vtkActor()
projection_actor_4.SetMapper(projection_mapper_4)
projection_actor_4.GetProperty().SetColor(1, 1, 1)
projection_actor_4.GetProperty().SetRepresentationToWireframe()

# --- Best coordinate plane ---
projection_5 = vtkProjectPointsToPlane()
projection_5.SetInputConnection(disk.GetOutputPort())
projection_5.SetProjectionTypeToBestCoordinatePlane()

projection_mapper_5 = vtkPolyDataMapper()
projection_mapper_5.SetInputConnection(projection_5.GetOutputPort())

projection_actor_5 = vtkActor()
projection_actor_5.SetMapper(projection_mapper_5)
projection_actor_5.GetProperty().SetColor(1, 1, 1)
projection_actor_5.GetProperty().SetRepresentationToWireframe()

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 0.5)
renderer_0.AddActor(projection_actor_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.667, 0.5)
renderer_1.AddActor(projection_actor_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.667, 0, 1, 0.5)
renderer_2.AddActor(projection_actor_2)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0, 0.5, 0.333, 1)
renderer_3.AddActor(projection_actor_3)
renderer_3.SetBackground(0, 0, 0)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.333, 0.5, 0.667, 1)
renderer_4.AddActor(projection_actor_4)
renderer_4.SetBackground(0, 0, 0)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.667, 0.5, 1, 1)
renderer_5.AddActor(projection_actor_5)
renderer_5.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(600, 400)
render_window.SetWindowName("project to plane")

# Scene
renderer_0.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_0.GetActiveCamera().SetPosition(1, 0, 0)
renderer_0.ResetCamera()

renderer_1.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_1.GetActiveCamera().SetPosition(0, 1, 0)
renderer_1.GetActiveCamera().SetViewUp(0, 0, 1)
renderer_1.ResetCamera()

renderer_2.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_2.GetActiveCamera().SetPosition(0, 0, 1)
renderer_2.ResetCamera()

renderer_3.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_3.GetActiveCamera().SetPosition(normal)
renderer_3.ResetCamera()

renderer_4.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_4.GetActiveCamera().SetPosition(spec_normal)
renderer_4.ResetCamera()

renderer_5.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_5.GetActiveCamera().SetPosition(0, 0, 1)
renderer_5.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
