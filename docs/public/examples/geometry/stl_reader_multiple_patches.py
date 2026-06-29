#!/usr/bin/env python

# Read a multi-patch STL file and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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

# Read multi-patch STL file
stl_reader = vtkSTLReader()
stl_reader.SetFileName(os.path.join(data_dir, "multiple_patches.stl"))
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
render_window.SetWindowName("stl reader multiple patches")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
