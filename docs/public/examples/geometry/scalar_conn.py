#!/usr/bin/env python
# Demonstrate scalar connectivity filter with quadric implicit function and contour extraction.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkConnectivityFilter, vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Quadric definition.
quadric = vtkQuadric()
quadric.SetCoefficients([0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0])

# Sample the quadric.
sample = vtkSampleFunction()
sample.SetSampleDimensions(30, 30, 30)
sample.SetImplicitFunction(quadric)
sample.Update()
sample.ComputeNormalsOff()

# Extract cells containing isosurface of interest.
conn = vtkConnectivityFilter()
conn.SetInputConnection(sample.GetOutputPort())
conn.ScalarConnectivityOn()
conn.SetScalarRange(0.6, 0.6)
conn.SetExtractionModeToCellSeededRegions()
conn.AddSeed(105)

# Create contours.
contours = vtkContourFilter()
contours.SetInputConnection(conn.GetOutputPort())
contours.GenerateValues(5, 0.0, 1.2)

# Mapper and actor for connectivity output.
cont_mapper = vtkDataSetMapper()
cont_mapper.SetInputConnection(conn.GetOutputPort())
cont_mapper.SetScalarRange(0.0, 1.2)

cont_actor = vtkActor()
cont_actor.SetMapper(cont_mapper)

# Create outline.
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(cont_actor)
renderer.AddActor(outline_actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scalar conn")

renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
