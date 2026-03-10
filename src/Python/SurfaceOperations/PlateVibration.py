#!/usr/bin/env python

# Beam displacement visualization showing vibration mode shapes.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
plate_color = (1.000, 0.627, 0.549)
bkg_color = (0.255, 0.388, 0.584)
white = (1.000, 1.000, 1.000)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "plate.vtk")

# Reader: load the plate vibration data
plate = vtkPolyDataReader()
plate.SetFileName(file_name)
plate.SetVectorsName("mode2")
plate.Update()

# Filter: compute surface normals
plate_normals = vtkPolyDataNormals()
plate_normals.SetInputConnection(plate.GetOutputPort())

# Filter: warp the surface by displacement vectors
warp = vtkWarpVector()
warp.SetInputConnection(plate_normals.GetOutputPort())
warp.SetScaleFactor(0.5)

# Mapper: map the warped surface to graphics primitives
plate_mapper = vtkDataSetMapper()
plate_mapper.SetInputConnection(warp.GetOutputPort())

# Actor: display the warped plate
plate_actor = vtkActor()
plate_actor.SetMapper(plate_mapper)
plate_actor.GetProperty().SetColor(plate_color)
plate_actor.RotateX(-90)

# Filter: bounding outline of the original plate
outline = vtkOutlineFilter()
outline.SetInputConnection(plate.GetOutputPort())

# Mapper: map the outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.RotateX(-90)
outline_actor.GetProperty().SetColor(white)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(plate_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(bkg_color)
renderer.GetActiveCamera().SetPosition(-3.7, 13, 15.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("PlateVibration")
render_window.SetSize(500, 500)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
