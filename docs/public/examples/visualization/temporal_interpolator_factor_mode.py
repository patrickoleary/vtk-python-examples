#!/usr/bin/env python
# Demonstrate vtkTemporalInterpolator with resample factor mode on can.ex2.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import vtkTemporalInterpolator
from vtkmodules.vtkIOIOSS import vtkIOSSReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read temporal Exodus data
reader = vtkIOSSReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))

# Temporal interpolation with resample factor
interpolator = vtkTemporalInterpolator()
interpolator.SetResampleFactor(2)
interpolator.SetInputConnection(reader.GetOutputPort())

# Convert composite data to polydata
geom = vtkCompositeDataGeometryFilter()
geom.SetInputConnection(interpolator.GetOutputPort())
geom.UpdateTimeStep(0.001)

mapper = vtkPolyDataMapper()
mapper.SetInputDataObject(geom.GetOutputDataObject(0))

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("temporal interpolator factor mode")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(90)

interactor.Initialize()
interactor.Start()
