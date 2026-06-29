#!/usr/bin/env python

# Demonstrate clipping and capping on a sphere using vtkClipPolyData,
# vtkFeatureEdges, vtkStripper, and vtkTriangleFilter to generate a
# cap surface from boundary edges.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkCleanPolyData,
    vtkClipPolyData,
    vtkFeatureEdges,
    vtkStripper,
    vtkTriangleFilter,
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

colors = vtkNamedColors()

peacock = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock)
tomato = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato)
banana = [0.0, 0.0, 0.0]
colors.GetColorRGB("banana", banana)

# Source: sphere
sphere = vtkSphereSource()
sphere.SetRadius(1)
sphere.SetPhiResolution(10)
sphere.SetThetaResolution(10)

# Clip plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(-1, -1, 0)

# Clip the sphere
clipper = vtkClipPolyData()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()
clipper.SetValue(0)

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

back_prop = vtkProperty()
back_prop.SetDiffuseColor(tomato)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(peacock)
clip_actor.SetBackfaceProperty(back_prop)

# Extract boundary edges from clipped output
boundary_edges = vtkFeatureEdges()
boundary_edges.SetInputConnection(clipper.GetOutputPort())
boundary_edges.BoundaryEdgesOn()
boundary_edges.FeatureEdgesOff()
boundary_edges.NonManifoldEdgesOff()

boundary_clean = vtkCleanPolyData()
boundary_clean.SetInputConnection(boundary_edges.GetOutputPort())

boundary_strips = vtkStripper()
boundary_strips.SetInputConnection(boundary_clean.GetOutputPort())
boundary_strips.Update()

# Convert polyline loops to polygons
boundary_poly = vtkPolyData()
boundary_poly.SetPoints(boundary_strips.GetOutput().GetPoints())
boundary_poly.SetPolys(boundary_strips.GetOutput().GetLines())

# Triangulate the cap surface
boundary_triangles = vtkTriangleFilter()
boundary_triangles.SetInputData(boundary_poly)

boundary_mapper = vtkPolyDataMapper()
boundary_mapper.SetInputConnection(boundary_triangles.GetOutputPort())

boundary_actor = vtkActor()
boundary_actor.SetMapper(boundary_mapper)
boundary_actor.GetProperty().SetColor(banana)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(boundary_actor)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("cap sphere")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
