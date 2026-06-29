#!/usr/bin/env python

# Read an OpenFOAM case and render the cavity simulation with pressure scalars.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOParallel import vtkPOpenFOAMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "OpenFOAM")

foam_reader = vtkPOpenFOAMReader()
foam_reader.SetFileName(os.path.join(data_dir, "cavity", "cavity.foam"))
foam_reader.SetCaseType(1)  # DECOMPOSED_CASE
foam_reader.Update()

foam_reader.SetTimeValue(0.5)
foam_reader.ReadZonesOn()
foam_reader.Update()

# Filter
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(foam_reader.GetOutputPort())

# Mapper
cavity_mapper = vtkPolyDataMapper()
cavity_mapper.SetInputConnection(geometry_filter.GetOutputPort())

# Actor
cavity_actor = vtkActor()
cavity_actor.SetMapper(cavity_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cavity_actor)
renderer.SetBackground(0.2, 0.4, 0.6)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("p open foam reader")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
interactor.Initialize()
interactor.Start()
