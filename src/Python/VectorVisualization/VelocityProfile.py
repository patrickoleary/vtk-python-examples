#!/usr/bin/env python

# Visualize flow momentum by warping computational planes with the velocity vector.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkPolyDataNormals,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
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
bkg_color = (0.255, 0.388, 0.584)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(str(data_dir / "combxyz.bin"))
pl3d.SetQFileName(str(data_dir / "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)
extent = sg.GetExtent()
scalar_range = sg.GetScalarRange()

# Filter: extract three computational planes at i=10, 30, 45
append = vtkAppendPolyData()
for i_val in (10, 30, 45):
    plane = vtkStructuredGridGeometryFilter()
    plane.SetInputData(sg)
    plane.SetExtent(i_val, i_val, 1, extent[3], 1, extent[5])
    append.AddInputConnection(plane.GetOutputPort())

# Filter: warp planes by velocity vector
warp = vtkWarpVector()
warp.SetInputConnection(append.GetOutputPort())
warp.SetScaleFactor(0.005)
warp.Update()

# Filter: recompute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputData(warp.GetPolyDataOutput())
normals.SetFeatureAngle(45)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(normals.GetOutputPort())
plane_mapper.SetScalarRange(scalar_range)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Filter: outline around the data
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(bkg_color)
renderer.GetActiveCamera().SetPosition(19.8562, -31.8912, 47.0755)
renderer.GetActiveCamera().SetFocalPoint(8.255, 0.147815, 29.7631)
renderer.GetActiveCamera().SetViewUp(-0.0333325, 0.465756, 0.884285)
renderer.GetActiveCamera().SetClippingRange(17.3078, 64.6375)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("VelocityProfile")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
