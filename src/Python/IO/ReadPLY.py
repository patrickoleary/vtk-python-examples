#!/usr/bin/env python

# Read a PLY (Polygon File Format) file using vtkPLYReader and display the
# mesh.  A small PLY file is generated from a sphere if it does not already
# exist, so this example is self-contained.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOPLY import vtkPLYReader, vtkPLYWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.000, 0.855, 0.725)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
ply_path = data_dir / "sphere.ply"

# Generate a PLY file if one does not exist
if not ply_path.exists():
    sphere = vtkSphereSource()
    sphere.SetPhiResolution(32)
    sphere.SetThetaResolution(32)
    writer = vtkPLYWriter()
    writer.SetInputConnection(sphere.GetOutputPort())
    writer.SetFileName(str(ply_path))
    writer.Write()

# Reader: load the PLY file
reader = vtkPLYReader()
reader.SetFileName(str(ply_path))
reader.Update()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadPLY")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
