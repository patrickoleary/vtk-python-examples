#!/usr/bin/env python

# Demonstrate vtkMergeTimeFilter by reading an Exodus file with temporal
# data, creating a shifted copy, merging the time steps, and rendering
# the dataset at the first time step.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkMergeTimeFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import vtkTemporalShiftScale
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read temporal Exodus data
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))
reader.Update()

# Shift the time steps
shifter = vtkTemporalShiftScale()
shifter.SetInputConnection(reader.GetOutputPort(0))
shifter.SetPreShift(-0.002)

# Merge time steps from original and shifted
merger = vtkMergeTimeFilter()
merger.SetInputConnection(reader.GetOutputPort(0))
merger.AddInputConnection(shifter.GetOutputPort(0))
merger.SetTolerance(0.00004)
merger.Update()

# Extract geometry for rendering
geometry = vtkCompositeDataGeometryFilter()
geometry.SetInputConnection(merger.GetOutputPort())

# Render with composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("merge time")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, -40, -5)
renderer.GetActiveCamera().SetFocalPoint(0, 4, -5)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
