#!/usr/bin/env python

# Read EnSight Mandelbrot SOS file with two pieces and render Iterations.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOEnSight import vtkEnSightMasterServerReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read piece 0
ensight_reader_0 = vtkEnSightMasterServerReader()
ensight_reader_0.SetCaseFileName(os.path.join(data_dir, "EnSight", "mandelbrot.sos"))
ensight_reader_0.SetCurrentPiece(0)

geometry_filter_0 = vtkGeometryFilter()
geometry_filter_0.SetInputConnection(ensight_reader_0.GetOutputPort())

composite_mapper_0 = vtkCompositePolyDataMapper()
composite_mapper_0.SetInputConnection(geometry_filter_0.GetOutputPort())
composite_mapper_0.SetColorModeToMapScalars()
composite_mapper_0.SetScalarModeToUsePointFieldData()
composite_mapper_0.ColorByArrayComponent("Iterations", 0)
composite_mapper_0.SetScalarRange(0, 112)

actor_0 = vtkActor()
actor_0.SetMapper(composite_mapper_0)

# Read piece 1
ensight_reader_1 = vtkEnSightMasterServerReader()
ensight_reader_1.SetCaseFileName(os.path.join(data_dir, "EnSight", "mandelbrot.sos"))
ensight_reader_1.SetCurrentPiece(1)

geometry_filter_1 = vtkGeometryFilter()
geometry_filter_1.SetInputConnection(ensight_reader_1.GetOutputPort())

composite_mapper_1 = vtkCompositePolyDataMapper()
composite_mapper_1.SetInputConnection(geometry_filter_1.GetOutputPort())
composite_mapper_1.SetColorModeToMapScalars()
composite_mapper_1.SetScalarModeToUsePointFieldData()
composite_mapper_1.ColorByArrayComponent("Iterations", 0)
composite_mapper_1.SetScalarRange(0, 112)

actor_1 = vtkActor()
actor_1.SetMapper(composite_mapper_1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight mandelbrot")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
