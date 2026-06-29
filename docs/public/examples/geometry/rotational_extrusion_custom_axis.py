#!/usr/bin/env python

# Demonstrate vtkRotationalExtrusionFilter with a custom rotation axis
# by creating a line segment, performing a 270-degree extrusion around
# the (1,0,1) axis, and rendering the smooth surface with wireframe overlay.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a line source
line = vtkLineSource()
line.SetPoint1(0.0, 1.0, 0.0)
line.SetPoint2(0.0, 1.0, 2.0)
line.SetResolution(10)

# Line actor
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(line.GetOutputPort())

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetLineWidth(5)
line_actor.GetProperty().SetColor(0.0, 0.749, 1.0)

# 270-degree rotational extrusion around custom axis
sweeper = vtkRotationalExtrusionFilter()
sweeper.SetResolution(20)
sweeper.SetInputConnection(line.GetOutputPort())
sweeper.SetAngle(270)
sweeper.SetRotationAxis(1, 0, 1)

# Normals for smooth rendering
normals = vtkPolyDataNormals()
normals.SetInputConnection(sweeper.GetOutputPort())

# Surface mapper and actor
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(normals.GetOutputPort())
cylinder_mapper.SetResolveCoincidentTopologyToPolygonOffset()

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetRepresentationToSurface()
cylinder_actor.GetProperty().SetInterpolationToGouraud()
cylinder_actor.GetProperty().SetColor(1.0, 0.3882, 0.2784)

# Wireframe mapper and actor
cylinder_wireframe_mapper = vtkPolyDataMapper()
cylinder_wireframe_mapper.SetInputConnection(sweeper.GetOutputPort())
cylinder_wireframe_mapper.SetResolveCoincidentTopologyToPolygonOffset()

cylinder_wireframe_actor = vtkActor()
cylinder_wireframe_actor.SetMapper(cylinder_wireframe_mapper)
cylinder_wireframe_actor.GetProperty().SetRepresentationToWireframe()
cylinder_wireframe_actor.GetProperty().SetColor(0.0, 0.0, 0.0)
cylinder_wireframe_actor.GetProperty().SetAmbient(1.0)
cylinder_wireframe_actor.GetProperty().SetDiffuse(0.0)
cylinder_wireframe_actor.GetProperty().SetSpecular(0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(line_actor)
renderer.AddActor(cylinder_actor)
renderer.AddActor(cylinder_wireframe_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.SetWindowName("rotational extrusion custom axis")

# Scene
camera = vtkCamera()
camera.SetPosition(7.395789993306532, 9.691575562803443, 3.026104158779236)
camera.SetFocalPoint(1.4814705502887429, -0.3407913255461607, 0.8067055831393791)
camera.SetViewUp(-0.15295139734386498, -0.12664956167569574, 0.9800845670542483)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
