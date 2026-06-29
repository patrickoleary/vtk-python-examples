#!/usr/bin/env python

# Read a Nek5000 dataset and render the pressure field with a lookup table.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOParallel import vtkNek5000Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "nek5000", "eddy_uv")

nek_reader = vtkNek5000Reader()
nek_reader.SetFileName(os.path.join(data_dir, "eddy_uv.nek5000"))

pressure_lut = vtkLookupTable()
pressure_lut.SetHueRange(0.66, 0.0)
pressure_lut.SetNumberOfTableValues(256)
pressure_lut.SetTableRange(-3.599372625350952, 1.3908110857009888)
pressure_lut.Build()

# Filter
surface_filter = vtkGeometryFilter()
surface_filter.SetInputConnection(nek_reader.GetOutputPort(0))

# Mapper
pressure_mapper = vtkPolyDataMapper()
pressure_mapper.SetInputConnection(surface_filter.GetOutputPort(0))
pressure_mapper.ScalarVisibilityOn()
pressure_mapper.SetScalarModeToUsePointFieldData()
pressure_mapper.SelectColorArray("Pressure")
pressure_mapper.SetLookupTable(pressure_lut)
pressure_mapper.UseLookupTableScalarRangeOn()

# Actor
pressure_actor = vtkActor()
pressure_actor.SetMapper(pressure_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(pressure_actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("nek5000 reader")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
