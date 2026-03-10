#!/usr/bin/env python

# Read PLOT3D grid (combxyz.bin) and solution (combq.bin) files, extract
# the structured grid surface geometry, and render it.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D grid and solution files
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(str(data_dir / "combxyz.bin"))
reader.SetQFileName(str(data_dir / "combq.bin"))
reader.SetScalarFunctionNumber(100)
reader.SetVectorFunctionNumber(202)
reader.Update()

# Geometry filter: extract the surface of the structured grid
geometry = vtkStructuredGridGeometryFilter()
geometry.SetInputData(reader.GetOutput().GetBlock(0))

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.GetActiveCamera().SetPosition(5.02611, -23.535, 50.3979)
renderer.GetActiveCamera().SetFocalPoint(9.33614, 0.0414149, 30.112)
renderer.GetActiveCamera().SetViewUp(-0.0676794, 0.657814, 0.750134)
renderer.GetActiveCamera().SetDistance(31.3997)
renderer.GetActiveCamera().SetClippingRange(12.1468, 55.8147)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadPLOT3D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
