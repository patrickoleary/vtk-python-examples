#!/usr/bin/env python

# Read a single 2D SEG-Y seismic line and render with a diverging color map, zoomed in.

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
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "SegY")

segy_reader = vtkSegYReader()
segy_reader.SetFileName(os.path.join(data_dir, "lineA.sgy"))
segy_reader.Update()

segy_output = segy_reader.GetOutput()
scalar_range = segy_output.GetScalarRange()
midrange = 0.5 * (scalar_range[0] + scalar_range[1])

diverging_ctf = vtkColorTransferFunction()
diverging_ctf.AddRGBPoint(scalar_range[0], 0.23, 0.30, 0.75)
diverging_ctf.AddRGBPoint(midrange, 0.86, 0.86, 0.86)
diverging_ctf.AddRGBPoint(scalar_range[1], 0.70, 0.02, 0.15)

# Mapper
seismic_mapper = vtkDataSetMapper()
seismic_mapper.SetInputConnection(segy_reader.GetOutputPort())
seismic_mapper.SetColorModeToMapScalars()
seismic_mapper.SetLookupTable(diverging_ctf)

# Actor
seismic_actor = vtkActor()
seismic_actor.SetMapper(seismic_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(seismic_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seg y2d reader zoom")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(90)
renderer.GetActiveCamera().Zoom(45.0)

interactor.Initialize()
interactor.Start()
