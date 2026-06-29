#!/usr/bin/env python

# Demonstrate vtkDepthSortPolyData sorting overlapping translucent spheres
# back-to-front for correct transparency rendering.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersHybrid import vtkDepthSortPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    VTK_SCALAR_MODE_USE_CELL_FIELD_DATA,
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Camera
camera = vtkCamera()

# Renderer
renderer = vtkRenderer()
renderer.SetActiveCamera(camera)

# Create five spheres at different positions
sphere_1 = vtkSphereSource()
sphere_1.SetThetaResolution(80)
sphere_1.SetPhiResolution(40)
sphere_1.SetRadius(1)
sphere_1.SetCenter(0, 0, 0)

sphere_2 = vtkSphereSource()
sphere_2.SetThetaResolution(80)
sphere_2.SetPhiResolution(40)
sphere_2.SetRadius(0.5)
sphere_2.SetCenter(1, 0, 0)

sphere_3 = vtkSphereSource()
sphere_3.SetThetaResolution(80)
sphere_3.SetPhiResolution(40)
sphere_3.SetRadius(0.5)
sphere_3.SetCenter(-1, 0, 0)

sphere_4 = vtkSphereSource()
sphere_4.SetThetaResolution(80)
sphere_4.SetPhiResolution(40)
sphere_4.SetRadius(0.5)
sphere_4.SetCenter(0, 1, 0)

sphere_5 = vtkSphereSource()
sphere_5.SetThetaResolution(80)
sphere_5.SetPhiResolution(40)
sphere_5.SetRadius(0.5)
sphere_5.SetCenter(0, -1, 0)

# Append all spheres
append_data = vtkAppendPolyData()
append_data.AddInputConnection(sphere_1.GetOutputPort())
append_data.AddInputConnection(sphere_2.GetOutputPort())
append_data.AddInputConnection(sphere_3.GetOutputPort())
append_data.AddInputConnection(sphere_4.GetOutputPort())
append_data.AddInputConnection(sphere_5.GetOutputPort())

# Depth sort
depth_sort = vtkDepthSortPolyData()
depth_sort.SetInputConnection(append_data.GetOutputPort())
depth_sort.SetDirectionToBackToFront()
depth_sort.SetVector(1, 1, 1)
depth_sort.SetCamera(camera)
depth_sort.SortScalarsOn()
depth_sort.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(depth_sort.GetOutputPort())
mapper.SetScalarRange(0, depth_sort.GetOutput().GetNumberOfCells())
mapper.SetScalarVisibility(1)
mapper.SelectColorArray("sortedCellIds")
mapper.SetUseLookupTableScalarRange(0)
mapper.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_FIELD_DATA)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.5)
actor.GetProperty().SetColor(1, 0, 0)
actor.RotateX(-72)

depth_sort.SetProp3D(actor)

renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 200)
render_window.SetWindowName("depth sort")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.2)

interactor.Initialize()
interactor.Start()
