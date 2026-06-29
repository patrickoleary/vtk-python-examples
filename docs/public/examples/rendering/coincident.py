#!/usr/bin/env python

# Demonstrate coincident topology resolution with points, wireframe, and surface.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read dragon mesh
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

vtkPolyDataMapper.SetResolveCoincidentTopologyToPolygonOffset()

# Points representation (pink)
point_mapper = vtkPolyDataMapper()
point_mapper.SetInputConnection(reader.GetOutputPort())
point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetDiffuseColor(1.0, 0.3, 1.0)
point_actor.GetProperty().SetPointSize(4.0)
point_actor.GetProperty().SetRepresentationToPoints()

# Wireframe representation (blue)
wire_mapper = vtkPolyDataMapper()
wire_mapper.SetInputConnection(reader.GetOutputPort())
wire_actor = vtkActor()
wire_actor.SetMapper(wire_mapper)
wire_actor.GetProperty().SetDiffuseColor(0.3, 0.3, 1.0)
wire_actor.GetProperty().SetRepresentationToWireframe()

# Surface representation (yellow)
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(reader.GetOutputPort())
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetDiffuseColor(1.0, 1.0, 0.3)

# Rendering pipeline
renderer = vtkRenderer()
renderer.AddActor(point_actor)
renderer.AddActor(wire_actor)
renderer.AddActor(surface_actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("coincident")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
