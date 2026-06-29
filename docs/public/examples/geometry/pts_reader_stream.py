#!/usr/bin/env python

# Read a PTS point cloud file via vtkFileResourceStream and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOGeometry import vtkPTSReader
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
file_stream.Open(os.path.join(data_dir, "samplePTS.pts"))

# Read PTS from stream
pts_reader = vtkPTSReader()
pts_reader.SetStream(file_stream)
pts_reader.SetLimitToMaxNumberOfPoints(True)
pts_reader.SetMaxNumberOfPoints(100000)
pts_reader.Update()

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(pts_reader.GetOutputPort())

# Actor
pts_actor = vtkActor()
pts_actor.SetMapper(poly_mapper)
pts_actor.GetProperty().SetPointSize(5)
pts_actor.GetProperty().SetColor(0.9, 0.4, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(pts_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pts reader stream")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
