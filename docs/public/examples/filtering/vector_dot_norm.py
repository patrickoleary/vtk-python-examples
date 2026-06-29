#!/usr/bin/env python

# Visualize plate vibration using vtkVectorDot and vtkVectorNorm with
# a custom lookup table, displayed in two viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkVectorDot,
    vtkVectorNorm,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: plate vibration data
plate = vtkPolyDataReader()
plate.SetFileName(os.path.join(data_dir, "plate.vtk"))
plate.SetVectorsName("mode8")

# Warp by displacement vectors
warp = vtkWarpVector()
warp.SetInputConnection(plate.GetOutputPort())
warp.SetScaleFactor(0.5)

# Compute normals for vector dot product
normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())

# VectorDot: dot product of vectors with normals
color = vtkVectorDot()
color.SetInputConnection(normals.GetOutputPort())

# Custom grayscale lookup table
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfColors(256)
lookup_table.Build()
for i in range(128):
    v = (128.0 - i) / 128.0
    lookup_table.SetTableValue(i, v, v, v, 1)
for i in range(128, 256):
    v = (i - 128.0) / 128.0
    lookup_table.SetTableValue(i, v, v, v, 1)

# VectorDot mapper
plate_mapper = vtkDataSetMapper()
plate_mapper.SetInputConnection(color.GetOutputPort())
plate_mapper.SetLookupTable(lookup_table)
plate_mapper.SetScalarRange(-1, 1)

plate_actor = vtkActor()
plate_actor.SetMapper(plate_mapper)

# VectorNorm: magnitude of vectors
color_2 = vtkVectorNorm()
color_2.SetInputConnection(plate.GetOutputPort())
color_2.NormalizeOn()

plate_mapper_2 = vtkDataSetMapper()
plate_mapper_2.SetInputConnection(color_2.GetOutputPort())
plate_mapper_2.SetLookupTable(lookup_table)
plate_mapper_2.SetScalarRange(0, 1)

plate_actor_2 = vtkActor()
plate_actor_2.SetMapper(plate_mapper_2)

# Two viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(plate_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(plate_actor_2)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("vector dot norm")

# Scene
camera = vtkCamera()
camera.SetPosition(1, 1, 1)
renderer_0.SetActiveCamera(camera)
renderer_1.SetActiveCamera(camera)
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
