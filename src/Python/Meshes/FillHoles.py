#!/usr/bin/env python

# Fill holes in a mesh using vtkFillHolesFilter. A sphere with cells
# removed creates holes that the filter patches. Side-by-side viewports
# show the mesh with holes (left) and the repaired mesh (right).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkFillHolesFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
peach_puff_rgb = (1.000, 0.855, 0.725)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.Update()

# Remove some cells to create holes
holed_poly = sphere.GetOutput()
holed_poly.BuildLinks()
for cell_id in range(50, 80):
    holed_poly.DeleteCell(cell_id)
for cell_id in range(200, 220):
    holed_poly.DeleteCell(cell_id)
holed_poly.RemoveDeletedCells()

# FillHoles: patch holes up to a maximum size
fill_holes = vtkFillHolesFilter()
fill_holes.SetInputData(holed_poly)
fill_holes.SetHoleSize(1000.0)

# Mapper: mesh with holes
holed_mapper = vtkPolyDataMapper()
holed_mapper.SetInputData(holed_poly)
holed_mapper.ScalarVisibilityOff()

holed_actor = vtkActor()
holed_actor.SetMapper(holed_mapper)
holed_actor.GetProperty().SetColor(peach_puff_rgb)
holed_actor.GetProperty().EdgeVisibilityOn()
holed_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Mapper: repaired mesh
filled_mapper = vtkPolyDataMapper()
filled_mapper.SetInputConnection(fill_holes.GetOutputPort())
filled_mapper.ScalarVisibilityOff()

filled_actor = vtkActor()
filled_actor.SetMapper(filled_mapper)
filled_actor.GetProperty().SetColor(peach_puff_rgb)
filled_actor.GetProperty().EdgeVisibilityOn()
filled_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, 0, 3)
camera.SetFocalPoint(0, 0, 0)

# Left renderer: mesh with holes
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(holed_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: repaired mesh
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(filled_actor)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("FillHoles")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
