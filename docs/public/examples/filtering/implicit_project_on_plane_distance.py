#!/usr/bin/env python

# Compute implicit projected distances from a cuspy surface onto a plane,
# display interior points as red glyphs with the plane and surface.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkImplicitProjectOnPlaneDistance,
)
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load the cuspy surface
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "CuspySurface.vtp"))
reader.Update()
polydata_input = reader.GetOutput()

# Create a plane for projection
plane_source = vtkPlaneSource()
plane_source.SetOrigin(0, 0, -1)
plane_source.SetPoint1(-30, -10, -1)
plane_source.SetPoint2(30, 50, -1)
plane_source.Update()

# Set up projected distance calculator
implicit_distance = vtkImplicitProjectOnPlaneDistance()
implicit_distance.SetInput(plane_source.GetOutput())

# Compute distances, keeping points below the surface
inside_points = vtkPoints()
num_points = polydata_input.GetNumberOfPoints()
for i in range(num_points):
    point = [0.0, 0.0, 0.0]
    polydata_input.GetPoint(i, point)
    distance = implicit_distance.EvaluateFunction(point)
    if distance <= 0.0:
        inside_points.InsertNextPoint(point)

# Inside points: red sphere glyphs
inside_polydata = vtkPolyData()
inside_polydata.SetPoints(inside_points)

inside_sphere = vtkSphereSource()
inside_sphere.SetRadius(3)

inside_glypher = vtkGlyph3D()
inside_glypher.SetInputData(inside_polydata)
inside_glypher.SetSourceConnection(inside_sphere.GetOutputPort())

inside_mapper = vtkPolyDataMapper()
inside_mapper.SetInputConnection(inside_glypher.GetOutputPort())

inside_actor = vtkActor()
inside_actor.SetMapper(inside_mapper)
inside_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Plane display: blue
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_source.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(0.0, 0.0, 1.0)

# Bounding surface display
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputData(polydata_input)

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().FrontfaceCullingOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(inside_actor)
renderer.AddActor(plane_actor)
renderer.AddActor(surface_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("implicit project on plane distance")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(60)
camera.Elevation(-10)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
