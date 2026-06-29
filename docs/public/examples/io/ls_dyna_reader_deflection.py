#!/usr/bin/env python

# Read an LS-DYNA impact simulation and render deflection data at time step 1.

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
lsdyna_reader.SetFileName(os.path.join(data_dir, "impact", "d3plot"))
lsdyna_reader.UpdateTimeStep(1.0)

# Geometry filter
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(lsdyna_reader.GetOutputPort())

# Mapper with deflection coloring
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.SetScalarModeToUsePointFieldData()
geometry_mapper.SelectColorArray("Deflection")
geometry_mapper.CreateDefaultLookupTable()
geometry_mapper.GetLookupTable().SetVectorModeToMagnitude()
geometry_mapper.GetLookupTable().SetRange(0, 1)

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
render_window.SetWindowName("ls dyna reader deflection")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
render_window.Render()
renderer.GetActiveCamera().Pitch(-135)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
