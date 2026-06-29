#!/usr/bin/env python

# Read a VPIC file and render charge density on the surface.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOVPIC import vtkVPICReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "VPIC")

vpic_reader = vtkVPICReader()
vpic_reader.SetFileName(os.path.join(data_dir, "global.vpc"))
vpic_reader.EnableAllPointArrays()
vpic_reader.Update()

# Filter
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(vpic_reader.GetOutputPort())

# Mapper
density_mapper = vtkPolyDataMapper()
density_mapper.SetInputConnection(surface_filter.GetOutputPort())
density_mapper.SetScalarModeToUsePointFieldData()
density_mapper.SelectColorArray("Charge Density(Hhydro)")
density_mapper.SetScalarRange(0.06743, 1.197)

# Actor
density_actor = vtkActor()
density_actor.SetMapper(density_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(density_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vpic reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
render_window.Render()
renderer.GetActiveCamera().Roll(45)
renderer.GetActiveCamera().Azimuth(45)

interactor.Initialize()
interactor.Start()
