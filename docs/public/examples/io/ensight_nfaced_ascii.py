#!/usr/bin/env python

# Read EnSight nfaced ASCII case file and render Pressure field.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
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

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "TEST.case"))

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(ensight_reader.GetOutputPort())

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(surface_filter.GetOutputPort())
composite_mapper.SetColorModeToMapScalars()
composite_mapper.SetScalarModeToUseCellFieldData()
composite_mapper.ColorByArrayComponent("Pressure", 0)
composite_mapper.SetScalarRange(0.121168, 0.254608)

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight nfaced ascii")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0.643568, 0.424804, -0.477458)
camera.SetFocalPoint(0.894177, 0.490735, 0.028153)
camera.SetViewAngle(30)
camera.SetViewUp(0.338885, 0.896657, -0.284892)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
