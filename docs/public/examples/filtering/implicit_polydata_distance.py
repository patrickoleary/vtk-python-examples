#!/usr/bin/env python

# Compute implicit distances from a cuspy surface, display interior
# points as red glyphs and closest surface points as blue glyphs.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkImplicitPolyDataDistance,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
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

# Set up implicit distance calculator
implicit_distance = vtkImplicitPolyDataDistance()
implicit_distance.SetInput(reader.GetOutput())

# Compute distances to test points on a grid
inside_points = vtkPoints()
surface_points = vtkPoints()

x_range = (-47.6, 46.9)
y_range = (-18.2, 82.1)
z_range = (1.63, 102.0)
spacing = 10.0

z = z_range[0]
while z < z_range[1]:
    y = y_range[0]
    while y < y_range[1]:
        x = x_range[0]
        while x < x_range[1]:
            point = [x, y, z]
            surface_point = [0.0, 0.0, 0.0]
            distance = implicit_distance.EvaluateFunctionAndGetClosestPoint(point, surface_point)
            if distance <= 0.0:
                inside_points.InsertNextPoint(point)
                surface_points.InsertNextPoint(surface_point)
            x += spacing
        y += spacing
    z += spacing

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

# Surface points: blue sphere glyphs
surface_polydata = vtkPolyData()
surface_polydata.SetPoints(surface_points)

surface_sphere = vtkSphereSource()
surface_sphere.SetRadius(3)

surface_glypher = vtkGlyph3D()
surface_glypher.SetInputData(surface_polydata)
surface_glypher.SetSourceConnection(surface_sphere.GetOutputPort())

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface_glypher.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetColor(0.0, 0.0, 1.0)

# Bounding surface
surface_display_mapper = vtkPolyDataMapper()
surface_display_mapper.SetInputConnection(reader.GetOutputPort())

surface_display_actor = vtkActor()
surface_display_actor.SetMapper(surface_display_mapper)
surface_display_actor.GetProperty().FrontfaceCullingOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(inside_actor)
renderer.AddActor(surface_actor)
renderer.AddActor(surface_display_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("implicit polydata distance")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(-20)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
