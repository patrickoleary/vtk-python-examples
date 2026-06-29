#!/usr/bin/env python

# Read EnSight blow1 ASCII case with selective array loading and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read EnSight case file with selective arrays
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "blow1_ascii.case"))
ensight_reader.SetTimeValue(1)
ensight_reader.ReadAllVariablesOff()
ensight_reader.SetPointArrayStatus("displacement", 1)
ensight_reader.SetCellArrayStatus("thickness", 1)
ensight_reader.SetCellArrayStatus("displacement", 1)

# Extract geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(ensight_reader.GetOutputPort())

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(geometry_filter.GetOutputPort())
composite_mapper.SetScalarRange(0.5, 1.0)

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight select arrays")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(99.3932, 17.6571, -22.6071)
camera.SetFocalPoint(3.5, 12, 1.5)
camera.SetViewAngle(30)
camera.SetViewUp(0.239617, -0.01054, 0.97081)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
