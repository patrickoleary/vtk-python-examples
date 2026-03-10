#!/usr/bin/env python

# Clip a rectilinear grid with a cone polydata using
# vtkImplicitPolyDataDistance and vtkClipDataSet. Two viewports show
# the inside (left) and outside (right) portions of the clipped grid.
# A translucent wireframe of the cone appears in both viewports so
# the relationship between the clip surface and the results is clear.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
banana_rgb = (0.890, 0.812, 0.341)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: generate a cone pointing downward
cone = vtkConeSource()
cone.SetResolution(50)
cone.SetDirection(0, 0, -1)
cone.SetHeight(3.0)
cone.CappingOn()
cone.Update()

# ImplicitPolyDataDistance: signed distance from the cone surface
implicit_distance = vtkImplicitPolyDataDistance()
implicit_distance.SetInput(cone.GetOutput())

# Rectilinear grid: 51x51x51 uniform grid over [-1, 1]^3
dimension = 51
x_coords = vtkFloatArray()
y_coords = vtkFloatArray()
z_coords = vtkFloatArray()
for i in range(dimension):
    val = -1.0 + i * 2.0 / (dimension - 1)
    x_coords.InsertNextValue(val)
    y_coords.InsertNextValue(val)
    z_coords.InsertNextValue(val)

rgrid = vtkRectilinearGrid()
rgrid.SetDimensions(dimension, dimension, dimension)
rgrid.SetXCoordinates(x_coords)
rgrid.SetYCoordinates(y_coords)
rgrid.SetZCoordinates(z_coords)

# Evaluate the signed distance function at all grid points
signed_distances = vtkFloatArray()
signed_distances.SetNumberOfComponents(1)
signed_distances.SetName("SignedDistances")
for point_id in range(rgrid.GetNumberOfPoints()):
    p = rgrid.GetPoint(point_id)
    signed_distances.InsertNextValue(implicit_distance.EvaluateFunction(p))
rgrid.GetPointData().SetScalars(signed_distances)

# Clip: extract the region inside the cone
clipper_left = vtkClipDataSet()
clipper_left.SetInputData(rgrid)
clipper_left.SetClipFunction(implicit_distance)
clipper_left.SetValue(0.0)
clipper_left.InsideOutOn()
clipper_left.GenerateClippedOutputOff()

clipper_right = vtkClipDataSet()
clipper_right.SetInputData(rgrid)
clipper_right.SetClipFunction(implicit_distance)
clipper_right.SetValue(0.0)
clipper_right.InsideOutOff()
clipper_right.GenerateClippedOutputOff()

# Grid surface: translucent outer skin of the rectilinear grid with edges
grid_surface = vtkRectilinearGridGeometryFilter()
grid_surface.SetInputData(rgrid)
grid_surface.SetExtent(0, dimension - 1, 0, dimension - 1, 0, dimension - 1)

grid_mapper = vtkPolyDataMapper()
grid_mapper.SetInputConnection(grid_surface.GetOutputPort())
grid_mapper.ScalarVisibilityOff()

grid_actor = vtkActor()
grid_actor.SetMapper(grid_mapper)
grid_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
grid_actor.GetProperty().SetOpacity(0.25)

# Outline: black bounding box around the rectilinear grid
outline = vtkOutlineFilter()
outline.SetInputData(rgrid)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)
outline_actor.GetProperty().SetLineWidth(2)

# Cone wireframe: visible in both viewports as the clip surface reference
cone_mapper_left = vtkPolyDataMapper()
cone_mapper_left.SetInputConnection(cone.GetOutputPort())
cone_mapper_left.ScalarVisibilityOff()

cone_actor_left = vtkActor()
cone_actor_left.SetMapper(cone_mapper_left)
cone_actor_left.GetProperty().SetRepresentationToWireframe()
cone_actor_left.GetProperty().SetColor(tomato_rgb)
cone_actor_left.GetProperty().SetLineWidth(2)


# Mapper: inside portion shown on the left (cone-shaped piece)
inside_mapper = vtkDataSetMapper()
inside_mapper.SetInputConnection(clipper_left.GetOutputPort())
inside_mapper.ScalarVisibilityOff()

inside_actor = vtkActor()
inside_actor.SetMapper(inside_mapper)
inside_actor.GetProperty().SetColor(banana_rgb)

# Mapper: outside portion shown on the right (cube with cone removed)
outside_mapper = vtkDataSetMapper()
outside_mapper.SetInputConnection(clipper_right.GetOutputPort())
outside_mapper.ScalarVisibilityOff()

outside_actor = vtkActor()
outside_actor.SetMapper(outside_mapper)
outside_actor.GetProperty().SetColor(banana_rgb)

# Left renderer: inside clip + cone wireframe + translucent grid + outline
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
#left_renderer.AddActor(grid_actor)
left_renderer.AddActor(outline_actor)
left_renderer.AddActor(inside_actor)
left_renderer.AddActor(cone_actor_left)

# Duplicate outline for right renderer (actors can't be shared across renderers)
outline_r = vtkOutlineFilter()
outline_r.SetInputData(rgrid)

outline_mapper_r = vtkPolyDataMapper()
outline_mapper_r.SetInputConnection(outline_r.GetOutputPort())

outline_actor_r = vtkActor()
outline_actor_r.SetMapper(outline_mapper_r)
outline_actor_r.GetProperty().SetColor(0.0, 0.0, 0.0)
outline_actor_r.GetProperty().SetLineWidth(2)

# Duplicate cone wireframe for right renderer
cone_mapper_right = vtkPolyDataMapper()
cone_mapper_right.SetInputConnection(cone.GetOutputPort())
cone_mapper_right.ScalarVisibilityOff()

cone_actor_right = vtkActor()
cone_actor_right.SetMapper(cone_mapper_right)
cone_actor_right.GetProperty().SetRepresentationToWireframe()
cone_actor_right.GetProperty().SetColor(tomato_rgb)
cone_actor_right.GetProperty().SetLineWidth(2)

# Right renderer: outside clip + cone wireframe + outline
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(outline_actor_r)
right_renderer.AddActor(outside_actor)
right_renderer.AddActor(cone_actor_right)

# Shared camera
left_renderer.GetActiveCamera().SetPosition(0, -1, 0)
left_renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
left_renderer.GetActiveCamera().SetViewUp(0, 0, 1)
left_renderer.GetActiveCamera().Azimuth(30)
left_renderer.GetActiveCamera().Elevation(30)
left_renderer.ResetCamera()
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipDataSetWithPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
