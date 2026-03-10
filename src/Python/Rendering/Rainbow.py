#!/usr/bin/env python

# Colour a plane extracted from PLOT3D combustor data using a rainbow
# lookup table, with a wireframe outline of the structured grid.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
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
background = (0.439, 0.502, 0.565)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D combustor geometry and solution
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(str(data_dir / "combxyz.bin"))
reader.SetQFileName(str(data_dir / "combq.bin"))
reader.SetScalarFunctionNumber(100)
reader.SetVectorFunctionNumber(202)
reader.Update()

grid = reader.GetOutput().GetBlock(0)

# Filter: extract a planar slice at k=7 from the structured grid
plane = vtkStructuredGridGeometryFilter()
plane.SetInputData(grid)
plane.SetExtent(1, 100, 1, 100, 7, 7)

# Lookup table: rainbow colour map (red → blue)
lut = vtkLookupTable()
lut.SetNumberOfColors(256)
lut.SetHueRange(0.0, 0.667)
lut.Build()

# Mapper: map the extracted plane with scalar colouring
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())
plane_mapper.SetLookupTable(lut)
plane_mapper.SetScalarRange(grid.GetScalarRange())

# Actor: the coloured plane
plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Filter: wireframe outline of the full structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(grid)

# Mapper: map the outline
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: the wireframe outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(background)
renderer.TwoSidedLightingOff()

# Camera: position to match the combustor view
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(8.88908, 0.595038, 29.3342)
camera.SetPosition(-12.3332, 31.7479, 41.2387)
camera.SetViewUp(0.060772, -0.319905, 0.945498)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Rainbow")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
