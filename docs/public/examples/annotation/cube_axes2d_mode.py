#!/usr/bin/env python

# Test vtkCubeAxesActor in 2D mode with a plane source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
plane_source = vtkPlaneSource()
plane_source.SetXResolution(10)
plane_source.SetYResolution(10)

# Plane actor (filled)
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_source.GetOutputPort())
plane_mapper.SetResolveCoincidentTopologyToPolygonOffset()

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)

# Edge actor (wireframe)
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(plane_source.GetOutputPort())
edge_mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, 2)

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(0.0, 0.0, 0.0)
edge_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)

# Cube axes actor in 2D mode
axes = vtkCubeAxesActor()
axes.SetBounds(-0.5, 0.5, -0.5, 0.5, 0.0, 0.0)
axes.SetCornerOffset(0.0)
axes.SetXAxisVisibility(True)
axes.SetYAxisVisibility(True)
axes.SetZAxisVisibility(False)
axes.SetUse2DMode(True)
axes.SetEnableDistanceLOD(False)
axes.SetEnableViewAngleLOD(False)

# Red for X axis
axes.GetXAxesLinesProperty().SetColor(1.0, 0.0, 0.0)
axes.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes.GetLabelTextProperty(0).SetColor(1.0, 0.0, 0.0)

# Green for Y axis
axes.GetYAxesLinesProperty().SetColor(0.0, 1.0, 0.0)
axes.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes.GetLabelTextProperty(1).SetColor(0.0, 1.0, 0.0)

renderer.AddActor(plane_actor)
renderer.AddActor(edge_actor)
renderer.AddActor(axes)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cube axes2d mode")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.GetActiveCamera().SetPosition(0.0, 0.0, 2.5)
axes.SetCamera(renderer.GetActiveCamera())

interactor.Initialize()
interactor.Start()
