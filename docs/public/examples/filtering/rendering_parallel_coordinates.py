#!/usr/bin/env python

# Test vtkParallelCoordinatesActor with blow dataset.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkDataSetToDataObjectFilter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingAnnotation import vtkParallelCoordinatesActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read blow dataset
reader = vtkUnstructuredGridReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
reader.SetVectorsName("displacement9")
reader.SetScalarsName("thickness9")

ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(reader.GetOutputPort())
ds2do.ModernTopologyOff()
ds2do.Update()

# Parallel coordinates actor
actor = vtkParallelCoordinatesActor()
actor.SetInputConnection(ds2do.GetOutputPort())
actor.SetTitle("Parallel Coordinates Plot of blow.tcl")
actor.SetIndependentVariablesToColumns()
actor.GetPositionCoordinate().SetValue(0.05, 0.05, 0.0)
actor.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
actor.GetProperty().SetColor(1, 0, 0)
actor.GetTitleTextProperty().SetColor(1, 0, 0)
actor.GetLabelTextProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("rendering parallel coordinates")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
