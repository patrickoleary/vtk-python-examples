#!/usr/bin/env python

# Check whether a polydata surface is closed by detecting boundary edges
# with vtkFeatureEdges.  Reads cow.vtp and displays any open edges in red.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFeatureEdges
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
cow_file = str(data_dir / "cow.vtp")

# Reader: load the cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(cow_file)
reader.Update()

# Filter: detect boundary (open) edges only
feature_edges = vtkFeatureEdges()
feature_edges.SetInputConnection(reader.GetOutputPort())
feature_edges.BoundaryEdgesOn()
feature_edges.FeatureEdgesOff()
feature_edges.ManifoldEdgesOff()
feature_edges.NonManifoldEdgesOff()
feature_edges.Update()

num_open_edges = feature_edges.GetOutput().GetNumberOfCells()
if num_open_edges > 0:
    print(f"Surface is NOT closed ({num_open_edges} boundary edges)")
else:
    print("Surface is closed")

# Mapper & Actor: map boundary edges to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(feature_edges.GetOutputPort())

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Mapper & Actor: map translucent surface to graphics primitives
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(reader.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetOpacity(0.5)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(surface_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClosedSurface")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
