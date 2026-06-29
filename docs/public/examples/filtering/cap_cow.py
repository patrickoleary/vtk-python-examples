#!/usr/bin/env python

# Demonstrate clipping and capping on a cow model using vtkClipPolyData,
# vtkCutter, vtkStripper, and vtkTriangleFilter to generate a cut surface.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkCutter,
    vtkPolyDataNormals,
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
colors = vtkNamedColors()

peacock = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock)
tomato = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato)

# Read the cow geometry and generate vertex normals
cow = vtkBYUReader()
cow.SetGeometryFileName(os.path.join(data_dir, "Viewpoint", "cow.g"))

cow_normals = vtkPolyDataNormals()
cow_normals.SetInputConnection(cow.GetOutputPort())

# Define a clip plane
plane = vtkPlane()
plane.SetOrigin(0.25, 0, 0)
plane.SetNormal(-1, -1, 0)

# Clip the cow
clipper = vtkClipPolyData()
clipper.SetInputConnection(cow_normals.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()
clipper.SetValue(0.5)

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

back_prop = vtkProperty()
back_prop.SetDiffuseColor(tomato)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(peacock)
clip_actor.SetBackfaceProperty(back_prop)

# Generate cut lines and triangulate to create cap surface
cut_edges = vtkCutter()
cut_edges.SetInputConnection(cow_normals.GetOutputPort())
cut_edges.SetCutFunction(plane)
cut_edges.GenerateCutScalarsOn()
cut_edges.SetValue(0, 0.5)

cut_strips = vtkStripper()
cut_strips.SetInputConnection(cut_edges.GetOutputPort())
cut_strips.Update()

# Convert polyline loops to polygons
cut_poly = vtkPolyData()
cut_poly.SetPoints(cut_strips.GetOutput().GetPoints())
cut_poly.SetPolys(cut_strips.GetOutput().GetLines())

# Triangulate the cap polygons
cut_triangles = vtkTriangleFilter()
cut_triangles.SetInputData(cut_poly)

cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cut_triangles.GetOutputPort())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(peacock)

# Wireframe of the clipped-away portion
rest_mapper = vtkPolyDataMapper()
rest_mapper.SetInputData(clipper.GetClippedOutput())
rest_mapper.ScalarVisibilityOff()

rest_actor = vtkActor()
rest_actor.SetMapper(rest_mapper)
rest_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(cut_actor)
renderer.AddActor(rest_actor)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("cap cow")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
