#!/usr/bin/env python

# Read a 3D SegY file and render with a color transfer function.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOSegY import vtkSegYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

diverging_ctf = vtkColorTransferFunction()
diverging_ctf.AddRGBPoint(-127, 0.23, 0.30, 0.75)
diverging_ctf.AddRGBPoint(0.0, 0.86, 0.86, 0.86)
diverging_ctf.AddRGBPoint(126, 0.70, 0.02, 0.15)

segy_reader = vtkSegYReader()
segy_reader.SetFileName(os.path.join(data_dir, "SegY", "waha8.sgy"))
segy_reader.Update()

# Mapper
segy_mapper = vtkDataSetMapper()
segy_mapper.SetInputConnection(segy_reader.GetOutputPort())
segy_mapper.SetLookupTable(diverging_ctf)
segy_mapper.SetColorModeToMapScalars()

# Actor
segy_actor = vtkActor()
segy_actor.SetMapper(segy_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(segy_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seg y3d reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)

interactor.Initialize()
interactor.Start()
