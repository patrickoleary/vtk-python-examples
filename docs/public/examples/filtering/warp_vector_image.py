#!/usr/bin/env python

# Warp a rectilinear grid by its vector field using vtkWarpVector and
# extract a sub-volume with vtkExtractGrid.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the rectilinear grid
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
reader.Update()

# Warp by vector
warper = vtkWarpVector()
warper.SetInputConnection(reader.GetOutputPort())
warper.SetScaleFactor(0.2)

# Extract a sub-volume
extract = vtkExtractGrid()
extract.SetInputConnection(warper.GetOutputPort())
extract.SetVOI(0, 100, 0, 100, 7, 15)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(extract.GetOutputPort())
mapper.SetScalarRange(0.197813, 0.710419)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("warp vector image")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.76213, 10.712)
cam.SetFocalPoint(-0.0842503, -0.136905, 0.610234)
cam.SetPosition(2.53813, 2.2678, -5.22172)
cam.SetViewUp(-0.241047, 0.930635, 0.275343)

interactor.Initialize()
interactor.Start()
