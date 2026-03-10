#!/usr/bin/env python

# Warp combustor computational planes by scalar value along the local normal.

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
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
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
silver = (0.753, 0.753, 0.753)
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
scalar_range = sg.GetScalarRange()

# Filter: extract three computational planes at i=10, 30, 45
append = vtkAppendPolyData()
for i_val in (10, 30, 45):
    plane = vtkStructuredGridGeometryFilter()
    plane.SetInputData(sg)
    plane.SetExtent(i_val, i_val, 1, 100, 1, 100)
    append.AddInputConnection(plane.GetOutputPort())

# Filter: warp planes by scalar along the x-normal direction
warp = vtkWarpScalar()
warp.SetInputConnection(append.GetOutputPort())
warp.UseNormalOn()
warp.SetNormal(1.0, 0.0, 0.0)
warp.SetScaleFactor(2.5)

# Filter: recompute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())
normals.SetFeatureAngle(60)

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
renderer.AddActor(outline_actor)
renderer.AddActor(plane_actor)
renderer.SetBackground(silver)
renderer.GetActiveCamera().SetClippingRange(3.95297, 50)
renderer.GetActiveCamera().SetFocalPoint(8.88908, 0.595038, 29.3342)
renderer.GetActiveCamera().SetPosition(-12.3332, 31.7479, 41.2387)
renderer.GetActiveCamera().SetViewUp(0.060772, -0.319905, 0.945498)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("WarpCombustor")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
