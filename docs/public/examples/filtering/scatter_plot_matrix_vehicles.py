#!/usr/bin/env python
# Demonstrate a scatter plot matrix with vehicle data from CSV.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkScatterPlotMatrix
from vtkmodules.vtkIOInfovis import vtkDelimitedTextReader
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read vehicle data CSV.
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(data_dir, "vehicle_data.csv")

reader = vtkDelimitedTextReader()
reader.SetFileName(csv_path)
reader.SetHaveHeaders(True)
reader.SetDetectNumericColumns(True)
reader.Update()

# Set up the scatter plot matrix.
matrix = vtkScatterPlotMatrix()
matrix.SetInput(reader.GetOutput())
matrix.SetTitle("Vehicles")
prop = matrix.GetTitleProperties()
prop.SetJustification(1)
prop.SetColor(0, 0, 0)
prop.SetFontSize(15)
prop.BoldOn()

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(800, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scatter plot matrix vehicles")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
