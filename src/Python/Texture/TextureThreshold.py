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

# ThresholdPlanes: three cutting planes with different scalar thresholds.
# Each plane extracts a slice of the structured grid, then
# vtkThresholdTextureCoords generates texture coordinates that make
# regions outside the threshold range transparent.
plane_extents = [
    [10, 10, 0, 100, 0, 100],
    [30, 30, 0, 100, 0, 100],
    [35, 35, 0, 100, 0, 100],
]

# Renderer: assemble the scene
renderer = vtkRenderer()

for i in range(3):
    plane = vtkStructuredGridGeometryFilter()
    plane.SetInputData(output)
    plane.SetExtent(*plane_extents[i])

    thresh = vtkThresholdTextureCoords()
    thresh.SetInputConnection(plane.GetOutputPort())
    if i == 0:
        thresh.ThresholdByUpper(1.5)
    elif i == 1:
        thresh.ThresholdByLower(1.5)
    else:
        thresh.ThresholdBetween(1.5, 1.8)

    plane_mapper = vtkDataSetMapper()
    plane_mapper.SetInputConnection(thresh.GetOutputPort())
    plane_mapper.SetScalarRange(output.GetScalarRange())

    plane_actor = vtkActor()
    plane_actor.SetMapper(plane_mapper)
    plane_actor.SetTexture(texture)
    plane_actor.GetProperty().SetOpacity(0.999)
    renderer.AddActor(plane_actor)

# Outline: wireframe bounding box for context
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

renderer.AddActor(outline_actor)
renderer.AddActor(wall_actor)
renderer.AddActor(fin_actor)
renderer.SetBackground(misty_rose_rgb)

# Camera: position the view
cam = vtkCamera()
cam.SetClippingRange(1.51176, 75.5879)
cam.SetFocalPoint(2.33749, 2.96739, 3.61023)
cam.SetPosition(10.8787, 5.27346, 15.8687)
cam.SetViewAngle(30)
cam.SetViewUp(-0.0610856, 0.987798, -0.143262)
renderer.SetActiveCamera(cam)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextureThreshold")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
