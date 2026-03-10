#!/usr/bin/env python

# Cut a sphere with a plane and fill the resulting contour to create a polygon.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
    vtkStripper,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
yellow_rgb = (1.000, 1.000, 0.000)
red_rgb = (1.000, 0.000, 0.000)
gold_rgb = (1.000, 0.843, 0.000)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Source: high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetRadius(50)
sphere_source.SetThetaResolution(100)
sphere_source.SetPhiResolution(100)

# Filter: cut the sphere with a plane offset along x
plane = vtkPlane()
plane.SetOrigin(20, 0, 0)
plane.SetNormal(1, 0, 0)

cutter = vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputConnection(sphere_source.GetOutputPort())
cutter.Update()

# Filter: strip the cut output into closed polylines
cut_strips = vtkStripper()
cut_strips.SetInputConnection(cutter.GetOutputPort())
cut_strips.Update()

# Convert closed polylines into filled polygons
cut_poly = vtkPolyData()
cut_poly.SetPoints(cut_strips.GetOutput().GetPoints())
cut_poly.SetPolys(cut_strips.GetOutput().GetLines())

# Mapper & Actor: map filled polygon to graphics primitives
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputData(cut_poly)

backface = vtkProperty()
backface.SetColor(gold_rgb)

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(yellow_rgb)
cut_actor.GetProperty().SetEdgeColor(red_rgb)
cut_actor.GetProperty().SetLineWidth(2)
cut_actor.GetProperty().EdgeVisibilityOn()
cut_actor.SetBackfaceProperty(backface)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cut_actor)
renderer.SetBackground(dark_slate_gray_rgb)

camera = renderer.GetActiveCamera()
camera.SetPosition(151.5, 12.8, -223.6)
camera.SetFocalPoint(12.5, 2.0, 7.6)
camera.SetViewUp(0.741, -0.524, 0.421)
camera.SetClippingRange(175.3, 366.5)
camera.Zoom(1.5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("FilledPolygon")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
