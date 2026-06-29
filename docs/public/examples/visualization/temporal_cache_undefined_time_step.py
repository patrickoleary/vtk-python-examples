#!/usr/bin/env python
# Demonstrate vtkTemporalDataSetCache with an undefined time step request on can.ex2.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import vtkTemporalDataSetCache
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

# Temporal cache
temporal_cache = vtkTemporalDataSetCache()
temporal_cache.SetInputConnection(reader.GetOutputPort())
temporal_cache.SetCacheSize(43)

# Rotate for better viewing
transform = vtkTransform()
transform.RotateX(90)

transform_filter = vtkTransformFilter()
transform_filter.SetInputConnection(temporal_cache.GetOutputPort())
transform_filter.SetTransform(transform)

# Convert composite data to polydata
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(transform_filter.GetOutputPort())
geometry_filter.UpdateTimeStep(0.00165)  # time step that doesn't exist

mapper = vtkPolyDataMapper()
mapper.SetInputDataObject(geometry_filter.GetOutputDataObject(0))

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("temporal cache undefined time step")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
