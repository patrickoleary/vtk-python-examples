#!/usr/bin/env python

# Linearly extrude a 2D polygon along a vector using
# vtkLinearExtrusionFilter to create a 3D solid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: define a star-shaped polygon in the XY plane
points = vtkPoints()
points.InsertPoint(0, 1.0, 0.0, 0.0)
points.InsertPoint(1, 0.3, 0.3, 0.0)
points.InsertPoint(2, 0.0, 1.0, 0.0)
points.InsertPoint(3, -0.3, 0.3, 0.0)
points.InsertPoint(4, -1.0, 0.0, 0.0)
points.InsertPoint(5, -0.3, -0.3, 0.0)
points.InsertPoint(6, 0.0, -1.0, 0.0)
points.InsertPoint(7, 0.3, -0.3, 0.0)

polygon = vtkCellArray()
polygon.InsertNextCell(8)
for i in range(8):
    polygon.InsertCellPoint(i)

star = vtkPolyData()
star.SetPoints(points)
star.SetPolys(polygon)

# Filter: triangulate the polygon so it renders correctly
triangle = vtkTriangleFilter()
triangle.SetInputData(star)

# Filter: linearly extrude along the Z axis
extrude = vtkLinearExtrusionFilter()
extrude.SetInputConnection(triangle.GetOutputPort())
extrude.SetExtrusionTypeToNormalExtrusion()
extrude.SetVector(0, 0, 2)
extrude.SetScaleFactor(1.0)
extrude.CappingOn()

# Mapper: the extruded solid
extrude_mapper = vtkPolyDataMapper()
extrude_mapper.SetInputConnection(extrude.GetOutputPort())

extrude_actor = vtkActor()
extrude_actor.SetMapper(extrude_mapper)
extrude_actor.GetProperty().SetColor(cornflower_blue_rgb)

# Mapper: the original star outline as wireframe
star_mapper = vtkPolyDataMapper()
star_mapper.SetInputConnection(triangle.GetOutputPort())

star_actor = vtkActor()
star_actor.SetMapper(star_mapper)
star_actor.GetProperty().SetRepresentationToWireframe()
star_actor.GetProperty().SetColor(tomato_rgb)
star_actor.GetProperty().SetLineWidth(3)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(extrude_actor)
renderer.AddActor(star_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("LinearExtrusion")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
