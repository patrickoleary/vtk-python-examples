#!/usr/bin/env python

# Demonstrate vtkAdaptiveTemporalInterpolator by reading two exodus
# time steps, interpolating at t=0.5, and rendering the composite
# geometry with point field data coloring.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import (
    vtkAlgorithm,
    vtkCompositeDataPipeline,
)
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersParallel import vtkAdaptiveTemporalInterpolator
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Set composite data pipeline as default
prototype = vtkCompositeDataPipeline()
vtkAlgorithm.SetDefaultExecutivePrototype(prototype)

# Read the exodus file directly (it contains both time steps)
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "simpleamrgrid.e-s000"))
reader.SetElementBlockArrayStatus("Unnamed block ID: 12", 1)
reader.SetElementResultArrayStatus("cell_dist", 1)
reader.SetElementResultArrayStatus("cell_poly", 1)
reader.SetPointResultArrayStatus("point_dist", 1)
reader.SetPointResultArrayStatus("point_poly", 1)
reader.UpdateInformation()

# Temporal interpolation
interp = vtkAdaptiveTemporalInterpolator()
interp.SetInputConnection(reader.GetOutputPort())

# Extract surface geometry
geom = vtkCompositeDataGeometryFilter()
geom.SetInputConnection(interp.GetOutputPort())

# Composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(geom.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("point_poly")
mapper.SetScalarRange(1.0, 6.0)
mapper.InterpolateScalarsBeforeMappingOn()
mapper.SetScalarVisibility(1)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("resampling interpolator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Request interpolation at t=0.5
info = geom.GetOutputInformation(0)
geom.UpdateInformation()
info.Set(prototype.UPDATE_TIME_STEP(), 0.5)
mapper.Modified()
renderer.ResetCameraClippingRange()

vtkAlgorithm.SetDefaultExecutivePrototype(None)

interactor.Initialize()
interactor.Start()
