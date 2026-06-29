#!/usr/bin/env python

# Read a single-patch STL file via vtkFileResourceStream and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Open file via stream
file_stream = vtkFileResourceStream()
file_stream.Open(os.path.join(data_dir, "42400-IDGH.stl"))

# Read STL from stream
stl_reader = vtkSTLReader()
stl_reader.SetStream(file_stream)
stl_reader.Update()

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(stl_reader.GetOutputPort())

# Actor
stl_actor = vtkActor()
stl_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(stl_actor)
renderer.SetBackground(0.3, 0.6, 0.3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("stl reader stream single patch")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
