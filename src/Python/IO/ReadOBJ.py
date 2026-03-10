#!/usr/bin/env python

# Read a Wavefront OBJ file using vtkOBJReader and display the mesh with
# surface normals computed for smooth shading.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tan_rgb = (0.824, 0.706, 0.549)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the OBJ file
reader = vtkOBJReader()
reader.SetFileName(str(data_dir / "ReadSTLWriteOBJ.obj"))
reader.Update()

# Filter: compute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tan_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadOBJ")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
