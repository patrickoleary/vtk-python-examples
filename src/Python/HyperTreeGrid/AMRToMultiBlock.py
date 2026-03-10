#!/usr/bin/env python

# Convert an overlapping AMR dataset to a multi-block dataset using
# vtkAMRToMultiBlockFilter and render the individual blocks with
# shrunk cells and edge visibility.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkAMRBox,
    vtkOverlappingAMR,
    vtkUniformGrid,
)
from vtkmodules.vtkFiltersAMR import vtkAMRToMultiBlockFilter
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.000, 0.843, 0.000)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Gaussian pulse centered at (5, 5, 5) with standard deviation 2
center = (5.0, 5.0, 5.0)
sigma = 2.0

# AMR: two-level overlapping adaptive mesh refinement
amr = vtkOverlappingAMR()
amr.Initialize([1, 2])
dims = [11, 11, 11]

# Level 0, Block 0: coarse grid covering [0, 10]^3
ug0 = vtkUniformGrid()
ug0.SetOrigin(0.0, 0.0, 0.0)
ug0.SetSpacing(1.0, 1.0, 1.0)
ug0.SetDimensions(dims)
scalars0 = vtkFloatArray()
scalars0.SetName("Gaussian-Pulse")
scalars0.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
idx = 0
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            dx = 0.0 + 1.0 * i - center[0]
            dy = 0.0 + 1.0 * j - center[1]
            dz = 0.0 + 1.0 * k - center[2]
            scalars0.SetValue(idx, math.exp(-(dx*dx + dy*dy + dz*dz) / (2.0 * sigma * sigma)))
            idx += 1
ug0.GetPointData().SetScalars(scalars0)
amr.SetAMRBox(0, 0, vtkAMRBox())
amr.SetDataSet(0, 0, ug0)

# Level 1, Block 0: refined grid at origin
ug1 = vtkUniformGrid()
ug1.SetOrigin(0.0, 0.0, 0.0)
ug1.SetSpacing(0.5, 0.5, 0.5)
ug1.SetDimensions(dims)
scalars1 = vtkFloatArray()
scalars1.SetName("Gaussian-Pulse")
scalars1.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
idx = 0
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            dx = 0.0 + 0.5 * i - center[0]
            dy = 0.0 + 0.5 * j - center[1]
            dz = 0.0 + 0.5 * k - center[2]
            scalars1.SetValue(idx, math.exp(-(dx*dx + dy*dy + dz*dz) / (2.0 * sigma * sigma)))
            idx += 1
ug1.GetPointData().SetScalars(scalars1)
amr.SetAMRBox(1, 0, vtkAMRBox())
amr.SetDataSet(1, 0, ug1)

# Level 1, Block 1: refined grid at (3, 3, 3)
ug2 = vtkUniformGrid()
ug2.SetOrigin(3.0, 3.0, 3.0)
ug2.SetSpacing(0.5, 0.5, 0.5)
ug2.SetDimensions(dims)
scalars2 = vtkFloatArray()
scalars2.SetName("Gaussian-Pulse")
scalars2.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
idx = 0
for k in range(dims[2]):
    for j in range(dims[1]):
        for i in range(dims[0]):
            dx = 3.0 + 0.5 * i - center[0]
            dy = 3.0 + 0.5 * j - center[1]
            dz = 3.0 + 0.5 * k - center[2]
            scalars2.SetValue(idx, math.exp(-(dx*dx + dy*dy + dz*dz) / (2.0 * sigma * sigma)))
            idx += 1
ug2.GetPointData().SetScalars(scalars2)
amr.SetAMRBox(1, 1, vtkAMRBox())
amr.SetDataSet(1, 1, ug2)
amr.SetRefinementRatio(0, 2)

# Convert: AMR to multi-block dataset
to_mb = vtkAMRToMultiBlockFilter()
to_mb.SetInputData(amr)

# Geometry: extract the block surfaces for rendering
mb_geom = vtkCompositeDataGeometryFilter()
mb_geom.SetInputConnection(to_mb.GetOutputPort())

mb_mapper = vtkPolyDataMapper()
mb_mapper.SetInputConnection(mb_geom.GetOutputPort())
mb_mapper.SetScalarModeToUsePointFieldData()
mb_mapper.SelectColorArray("Gaussian-Pulse")
mb_mapper.SetScalarRange(0.0, 1.0)

mb_actor = vtkActor()
mb_actor.SetMapper(mb_mapper)
mb_actor.GetProperty().EdgeVisibilityOn()
mb_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

# Outline: show block bounding boxes from the original AMR
outline = vtkOutlineFilter()
outline.SetInputData(amr)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(gold_rgb)
outline_actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(mb_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(150)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("AMRToMultiBlock")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
