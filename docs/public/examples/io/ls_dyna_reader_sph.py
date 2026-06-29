#!/usr/bin/env python

# Read LSDyna SPH foam data and render.

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

# Read LSDyna file
lsdyna_reader = vtkLSDynaReader()
lsdyna_reader.SetFileName(os.path.join(data_dir, "foam", "foam.d3plot"))
lsdyna_reader.Update()

# Extract geometry from composite data
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(lsdyna_reader.GetOutputPort(0))

# Mapper
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.SetScalarModeToUsePointFieldData()
geometry_mapper.SelectColorArray("Deflected Coordinates")
geometry_mapper.SetScalarRange(-130, 130)

# Actor
actor = vtkActor()
actor.SetMapper(geometry_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.2, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ls dyna reader sph")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(-60)
camera.Azimuth(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
