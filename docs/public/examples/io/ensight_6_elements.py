#!/usr/bin/env python

# Read EnSight6 elements case file with calculator and render computed scalars.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkArrayCalculator
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

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "elements6.case"))

# Extract geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(ensight_reader.GetOutputPort())

# Calculator
calculator = vtkArrayCalculator()
calculator.SetInputConnection(geometry_filter.GetOutputPort())
calculator.SetAttributeTypeToPointData()
calculator.SetFunction("dot(pointCVectors_r, pointCVectors_i) + pointScalars")
calculator.AddScalarArrayName("pointScalars", 0)
calculator.AddVectorArrayName("pointCVectors_r")
calculator.AddVectorArrayName("pointCVectors_i")
calculator.SetResultArrayName("test")

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(calculator.GetOutputPort())
composite_mapper.SetColorModeToMapScalars()
composite_mapper.SetScalarModeToUsePointFieldData()
composite_mapper.ColorByArrayComponent("test", 0)
composite_mapper.SetScalarRange(0, 36000)

# Actor
ensight_actor = vtkActor()
ensight_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ensight_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight 6 elements")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
