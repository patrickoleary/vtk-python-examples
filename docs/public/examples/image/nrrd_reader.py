#!/usr/bin/env python

# Read NRRD files in three formats and display in three viewports.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkNrrdReader
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read binary NRRD
reader_0 = vtkNrrdReader()
reader_0.SetFileName(os.path.join(data_dir, "beach.nrrd"))
reader_0.Update()

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(reader_0.GetOutputPort())
mapper_0.SetColorWindow(256)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.333, 1.0)

# Read ASCII NRRD
reader_1 = vtkNrrdReader()
reader_1.SetFileName(os.path.join(data_dir, "beach.ascii.nhdr"))
reader_1.Update()

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(reader_1.GetOutputPort())
mapper_1.SetColorWindow(1.0)
mapper_1.SetColorLevel(0.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetViewport(0.333, 0.0, 0.666, 1.0)

# Read gzip NRRD
reader_2 = vtkNrrdReader()
reader_2.SetFileName(os.path.join(data_dir, "beach_gzip.nrrd"))
reader_2.Update()

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(reader_2.GetOutputPort())
mapper_2.SetColorWindow(256)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.SetViewport(0.666, 0.0, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("nrrd reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 100)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
