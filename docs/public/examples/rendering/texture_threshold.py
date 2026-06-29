#!/usr/bin/env python

# Texture thresholding applied to scalar data from a blunt fin flow simulation.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersTexture import vtkThresholdTextureCoords
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)
black_rgb = (0.0, 0.0, 0.0)
misty_rose_rgb = (1.0, 0.894, 0.882)

# Data: locate the blunt fin dataset and texture map
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
xyz_file = str(data_dir / "bluntfinxyz.bin")
q_file = str(data_dir / "bluntfinq.bin")
texture_file = str(data_dir / "texThres2.vtk")

# Source: read the PLOT3D blunt fin dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(xyz_file)
pl3d.SetQFileName(q_file)
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()
output = pl3d.GetOutput().GetBlock(0)

# Wall: extract the floor geometry (j=0 plane)
wall = vtkStructuredGridGeometryFilter()
wall.SetInputData(output)
wall.SetExtent(0, 100, 0, 0, 0, 100)

wall_mapper = vtkPolyDataMapper()
wall_mapper.SetInputConnection(wall.GetOutputPort())
wall_mapper.ScalarVisibilityOff()

wall_actor = vtkActor()
wall_actor.SetMapper(wall_mapper)
wall_actor.GetProperty().SetColor(peach_puff_rgb)

# Fin: extract the rear wall geometry (k=0 plane)
fin = vtkStructuredGridGeometryFilter()
fin.SetInputData(output)
fin.SetExtent(0, 100, 0, 100, 0, 0)

fin_mapper = vtkPolyDataMapper()
fin_mapper.SetInputConnection(fin.GetOutputPort())
fin_mapper.ScalarVisibilityOff()

fin_actor = vtkActor()
fin_actor.SetMapper(fin_mapper)
fin_actor.GetProperty().SetColor(dark_slate_gray_rgb)

# Texture: load the threshold texture map
tmap = vtkStructuredPointsReader()
tmap.SetFileName(texture_file)

texture = vtkTexture()
texture.SetInputConnection(tmap.GetOutputPort())
texture.InterpolateOff()
texture.RepeatOff()

# --- Plane 0: threshold by upper (scalar >= 1.5) ---
plane_0 = vtkStructuredGridGeometryFilter()
plane_0.SetInputData(output)
plane_0.SetExtent(10, 10, 0, 100, 0, 100)

thresh_0 = vtkThresholdTextureCoords()
thresh_0.SetInputConnection(plane_0.GetOutputPort())
thresh_0.ThresholdByUpper(1.5)

plane_mapper_0 = vtkDataSetMapper()
plane_mapper_0.SetInputConnection(thresh_0.GetOutputPort())
plane_mapper_0.SetScalarRange(output.GetScalarRange())

plane_actor_0 = vtkActor()
plane_actor_0.SetMapper(plane_mapper_0)
plane_actor_0.SetTexture(texture)
plane_actor_0.GetProperty().SetOpacity(0.999)

# --- Plane 1: threshold by lower (scalar <= 1.5) ---
plane_1 = vtkStructuredGridGeometryFilter()
plane_1.SetInputData(output)
plane_1.SetExtent(30, 30, 0, 100, 0, 100)

thresh_1 = vtkThresholdTextureCoords()
thresh_1.SetInputConnection(plane_1.GetOutputPort())
thresh_1.ThresholdByLower(1.5)

plane_mapper_1 = vtkDataSetMapper()
plane_mapper_1.SetInputConnection(thresh_1.GetOutputPort())
plane_mapper_1.SetScalarRange(output.GetScalarRange())

plane_actor_1 = vtkActor()
plane_actor_1.SetMapper(plane_mapper_1)
plane_actor_1.SetTexture(texture)
plane_actor_1.GetProperty().SetOpacity(0.999)

# --- Plane 2: threshold between (1.5 <= scalar <= 1.8) ---
plane_2 = vtkStructuredGridGeometryFilter()
plane_2.SetInputData(output)
plane_2.SetExtent(35, 35, 0, 100, 0, 100)

thresh_2 = vtkThresholdTextureCoords()
thresh_2.SetInputConnection(plane_2.GetOutputPort())
thresh_2.ThresholdBetween(1.5, 1.8)

plane_mapper_2 = vtkDataSetMapper()
plane_mapper_2.SetInputConnection(thresh_2.GetOutputPort())
plane_mapper_2.SetScalarRange(output.GetScalarRange())

plane_actor_2 = vtkActor()
plane_actor_2.SetMapper(plane_mapper_2)
plane_actor_2.SetTexture(texture)
plane_actor_2.GetProperty().SetOpacity(0.999)

# Outline: wireframe bounding box for context
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(plane_actor_0)
renderer.AddActor(plane_actor_1)
renderer.AddActor(plane_actor_2)
renderer.AddActor(outline_actor)
renderer.AddActor(wall_actor)
renderer.AddActor(fin_actor)
renderer.SetBackground(misty_rose_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("texture threshold")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: position the camera
cam = vtkCamera()
cam.SetClippingRange(1.51176, 75.5879)
cam.SetFocalPoint(2.33749, 2.96739, 3.61023)
cam.SetPosition(10.8787, 5.27346, 15.8687)
cam.SetViewAngle(30)
cam.SetViewUp(-0.0610856, 0.987798, -0.143262)
renderer.SetActiveCamera(cam)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
