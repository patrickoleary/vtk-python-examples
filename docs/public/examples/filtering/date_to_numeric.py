#!/usr/bin/env python

# Demonstrate vtkDateToNumeric by reading polydata with date fields,
# converting dates to numeric values, and rendering colored by the
# converted numeric date array.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDateToNumeric
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read polydata with date fields
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "mine_with_dates.vtp"))

# Convert dates to numeric
date_to_numeric = vtkDateToNumeric()
date_to_numeric.SetInputConnection(reader.GetOutputPort())

# Map and render
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(date_to_numeric.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUseCellFieldData()
mapper.SetColorModeToMapScalars()
mapper.SelectColorArray("START_numeric")
mapper.SetScalarRange(1.5444e9, 1.5921e9)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.SetWindowName("date to numeric")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(6.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
