#!/usr/bin/env python

# Read an LS-DYNA d3plot file and render the hemi draw simulation.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOLSDyna import vtkLSDynaReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the LS-DYNA file
lsdyna_reader = vtkLSDynaReader()
lsdyna_reader.SetFileName(os.path.join(data_dir, "hemi.draw", "hemi_draw.d3plot"))
lsdyna_reader.Update()

# Geometry filter
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(lsdyna_reader.GetOutputPort())

# Mapper
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.SetScalarModeToUsePointFieldData()

# Actor
actor = vtkActor()
actor.SetMapper(geometry_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ls dyna reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
