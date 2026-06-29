#!/usr/bin/env python

# Demonstrate vtkDensifyPolyData by densifying a hand-built box polydata
# and a sphere, showing original and densified wireframes in a 2x2 grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_POLYGON,
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeneral import vtkDensifyPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build a box polydata with mixed polygon faces
box_points = vtkPoints()
box_points.InsertNextPoint(-0.5, -0.5, -0.5)
box_points.InsertNextPoint(-0.5, -0.5, 0.5)
box_points.InsertNextPoint(-0.5, 0.5, 0.5)
box_points.InsertNextPoint(-0.5, 0.5, -0.5)
box_points.InsertNextPoint(0.5, -0.5, -0.5)
box_points.InsertNextPoint(0.5, 0.5, -0.5)
box_points.InsertNextPoint(0.5, -0.5, 0.5)
box_points.InsertNextPoint(0.5, 0.5, 0.023809850216)
box_points.InsertNextPoint(0.5, 0.072707727551, 0.5)
box_points.InsertNextPoint(-0.014212930575, 0.5, 0.5)

box_polydata = vtkPolyData()
polys = vtkCellArray()
box_polydata.SetPolys(polys)
box_polydata.SetPoints(box_points)

box_polydata.InsertNextCell(VTK_POLYGON, 4, [0, 1, 2, 3])
box_polydata.InsertNextCell(VTK_POLYGON, 5, [4, 5, 7, 8, 6])
box_polydata.InsertNextCell(VTK_POLYGON, 4, [0, 4, 6, 1])
box_polydata.InsertNextCell(VTK_POLYGON, 5, [3, 2, 9, 7, 5])
box_polydata.InsertNextCell(VTK_POLYGON, 4, [0, 3, 5, 4])
box_polydata.InsertNextCell(VTK_POLYGON, 5, [1, 6, 8, 9, 2])
box_polydata.InsertNextCell(VTK_POLYGON, 3, [7, 9, 8])

# Densify the box
densify_box = vtkDensifyPolyData()
densify_box.SetInputData(box_polydata)
densify_box.SetNumberOfSubdivisions(2)

# Create a sphere and densify it
sphere = vtkSphereSource()

densify_sphere = vtkDensifyPolyData()
densify_sphere.SetInputConnection(sphere.GetOutputPort())
densify_sphere.SetNumberOfSubdivisions(1)

# Top-left: original box wireframe
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(box_polydata)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetRepresentationToWireframe()
actor_0.GetProperty().SetPointSize(3.0)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0.0, 0.5, 0.5)
renderer_0.SetViewport(0, 0, 0.5, 0.5)

# Top-right: densified box wireframe
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(densify_box.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetRepresentationToWireframe()
actor_1.GetProperty().SetPointSize(3.0)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0.0, 0.5, 0.5)
renderer_1.SetViewport(0.5, 0.0, 1, 0.5)

# Bottom-left: original sphere wireframe
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(sphere.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetRepresentationToWireframe()
actor_2.GetProperty().SetPointSize(3.0)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(0.0, 0.5, 0.5)
renderer_2.SetViewport(0, 0.5, 0.5, 1)

# Bottom-right: densified sphere wireframe
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(densify_sphere.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetRepresentationToWireframe()
actor_3.GetProperty().SetPointSize(3.0)

renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_3)
renderer_3.SetBackground(0.0, 0.5, 0.5)
renderer_3.SetViewport(0.5, 0.5, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(800, 640)
render_window.SetWindowName("densify polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
