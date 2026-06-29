#!/usr/bin/env python

# Clip a sphere point set with a plane using vtkTableBasedClipDataSet
# and visualize the remaining points as glyphs.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkPointSet,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkTableBasedClipDataSet
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere source
sphere_source = vtkSphereSource()
sphere_source.SetRadius(1.0)
sphere_source.SetThetaResolution(30)
sphere_source.SetPhiResolution(30)
sphere_source.Update()

# Convert PolyData to PointSet
poly = sphere_source.GetOutput()
point_set = vtkPointSet()
point_set.SetPoints(poly.GetPoints())

# Define a clipping plane
plane = vtkPlane()
plane.SetOrigin(0.0, 0.0, 0.0)
plane.SetNormal(1.0, 0.0, 0.0)

# Clip the point set
clipper = vtkTableBasedClipDataSet()
clipper.SetInputData(point_set)
clipper.SetClipFunction(plane)
clipper.SetInsideOut(False)
clipper.Update()

# Visualize clipped points as small sphere glyphs
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.02)
glyph_source.SetThetaResolution(8)
glyph_source.SetPhiResolution(8)

glyph = vtkGlyph3D()
glyph.SetInputConnection(clipper.GetOutputPort())
glyph.SetSourceConnection(glyph_source.GetOutputPort())
glyph.ScalingOff()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(0.2, 0.6, 1.0)

# Also show the original sphere as wireframe for reference
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputData(poly)

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetRepresentationToWireframe()
sphere_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
sphere_actor.GetProperty().SetOpacity(0.3)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("clip pointset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
