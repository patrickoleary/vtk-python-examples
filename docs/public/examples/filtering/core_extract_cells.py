#!/usr/bin/env python

# Extract cells from a sampled quadric volume using vtkExtractCells,
# comparing full range and interior range extraction in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkExtractCells
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 50

# Source: sample a quadric function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()
sample.Update()

# Extract all cells
extract_all = vtkExtractCells()
extract_all.SetInputConnection(sample.GetOutputPort())
extract_all.AddCellRange(0, sample.GetOutput().GetNumberOfCells())

extract_all_mapper = vtkDataSetMapper()
extract_all_mapper.SetInputConnection(extract_all.GetOutputPort())
extract_all_mapper.ScalarVisibilityOff()

extract_all_actor = vtkActor()
extract_all_actor.SetMapper(extract_all_mapper)
extract_all_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Extract interior range of cells
extract_interior = vtkExtractCells()
extract_interior.SetInputConnection(sample.GetOutputPort())
extract_interior.AddCellRange(100, 5000)
extract_interior.Update()

extract_interior_mapper = vtkDataSetMapper()
extract_interior_mapper.SetInputConnection(extract_interior.GetOutputPort())
extract_interior_mapper.ScalarVisibilityOff()

extract_interior_actor = vtkActor()
extract_interior_actor.SetMapper(extract_interior_mapper)
extract_interior_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Two viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(extract_all_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(extract_interior_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 150)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("core extract cells")

# Scene
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
