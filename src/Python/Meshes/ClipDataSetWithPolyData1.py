#!/usr/bin/env python

# Clip a coarse rectilinear grid with a cone polydata using
# vtkImplicitPolyDataDistance and vtkClipDataSet. The clipped region
# and background grid are shown as wireframes.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersCore import vtkImplicitPolyDataDistance
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
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
tomato_rgb = (1.000, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
light_gray_rgb = (0.750, 0.750, 0.750)

# Source: generate a cone
cone = vtkConeSource()
cone.SetResolution(20)
cone.Update()

# ImplicitPolyDataDistance: signed distance from the cone surface
implicit_distance = vtkImplicitPolyDataDistance()
implicit_distance.SetInput(cone.GetOutput())

# Rectilinear grid: 15x15x15 coarse grid over [-1, 1]^3
dimension = 15
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
clipper = vtkClipDataSet()
clipper.SetInputData(rgrid)
clipper.InsideOutOn()
clipper.SetValue(0.0)
clipper.Update()

# Cone wireframe: the clip surface shown in tomato red
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_mapper.ScalarVisibilityOff()

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetRepresentationToWireframe()
cone_actor.GetProperty().SetColor(tomato_rgb)
cone_actor.GetProperty().SetLineWidth(2)

# Geometry filter: mid-Z slice of the grid for wireframe context
geometry_filter = vtkRectilinearGridGeometryFilter()
geometry_filter.SetInputData(rgrid)
geometry_filter.SetExtent(0, dimension, 0, dimension,
                          dimension // 2, dimension // 2)

wire_mapper = vtkPolyDataMapper()
wire_mapper.SetInputConnection(geometry_filter.GetOutputPort())
wire_mapper.ScalarVisibilityOff()

wire_actor = vtkActor()
wire_actor.SetMapper(wire_mapper)
wire_actor.GetProperty().SetRepresentationToWireframe()
wire_actor.GetProperty().SetColor(light_gray_rgb)

# Outline: black bounding box around the rectilinear grid
outline = vtkOutlineFilter()
outline.SetInputData(rgrid)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)
outline_actor.GetProperty().SetLineWidth(2)

# Mapper: clipped mesh as wireframe in steel blue
clipper_mapper = vtkDataSetMapper()
clipper_mapper.SetInputConnection(clipper.GetOutputPort())
clipper_mapper.ScalarVisibilityOff()

clipper_actor = vtkActor()
clipper_actor.SetMapper(clipper_mapper)
clipper_actor.GetProperty().SetRepresentationToWireframe()
clipper_actor.GetProperty().SetColor(steel_blue_rgb)
clipper_actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(wire_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(clipper_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.GetActiveCamera().SetPosition(0, -1, 0)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipDataSetWithPolyData1")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
