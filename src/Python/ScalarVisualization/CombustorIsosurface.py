#!/usr/bin/env python

# Marching cubes isosurface of combustor flow density.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkPolyDataNormals,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke = (0.961, 0.961, 0.961)
dark_slate_gray = (0.184, 0.310, 0.310)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
xyz_file = str(data_dir / "combxyz.bin")
q_file = str(data_dir / "combq.bin")

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(xyz_file)
pl3d.SetQFileName(q_file)
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

# Filter: extract isosurface at density value 0.38
iso = vtkContourFilter()
iso.SetInputData(pl3d.GetOutput().GetBlock(0))
iso.SetValue(0, 0.38)

# Filter: compute smooth normals for the isosurface
normals = vtkPolyDataNormals()
normals.SetInputConnection(iso.GetOutputPort())
normals.SetFeatureAngle(45)

# Mapper: map isosurface to graphics primitives
iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

# Actor: display the isosurface
iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(white_smoke)

# Filter: structured grid outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputConnection(pl3d.GetOutputPort())

# Mapper: map outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline wireframe
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(dark_slate_gray)
renderer.GetActiveCamera().SetFocalPoint(9.71821, 0.458166, 29.3999)
renderer.GetActiveCamera().SetPosition(2.7439, -37.3196, 38.7167)
renderer.GetActiveCamera().SetViewUp(-0.16123, 0.264271, 0.950876)
renderer.GetActiveCamera().Zoom(1.3)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CombustorIsosurface")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
