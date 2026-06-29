#!/usr/bin/env python

# Visualize plate vibration using warp, normals, and vector dot product.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkVectorDot,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read plate data
plate = vtkPolyDataReader()
plate.SetFileName(os.path.join(data_dir, "plate.vtk"))
plate.SetVectorsName("mode8")

# Warp by displacement vectors
warp = vtkWarpVector()
warp.SetInputConnection(plate.GetOutputPort())
warp.SetScaleFactor(0.5)

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())

# Compute dot product of vectors with normals
color = vtkVectorDot()
color.SetInputConnection(normals.GetOutputPort())

# Build a symmetric grayscale lookup table
lut = vtkLookupTable()
lut.SetNumberOfColors(256)
lut.Build()
for i in range(128):
    lut.SetTableValue(i, (128.0 - i) / 128.0, (128.0 - i) / 128.0,
                      (128.0 - i) / 128.0, 1)
for i in range(128, 256):
    lut.SetTableValue(i, (i - 128.0) / 128.0, (i - 128.0) / 128.0,
                      (i - 128.0) / 128.0, 1)

# Map the result
plate_mapper = vtkDataSetMapper()
plate_mapper.SetInputConnection(color.GetOutputPort())
plate_mapper.SetLookupTable(lut)
plate_mapper.SetScalarRange(-1, 1)

plate_actor = vtkActor()
plate_actor.SetMapper(plate_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plate_actor)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("disp plot")

# Scene
renderer.GetActiveCamera().SetPosition(13.3991, 14.0764, 9.97787)
renderer.GetActiveCamera().SetFocalPoint(1.50437, 0.481517, 4.52992)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(-0.120861, 0.458556, -0.880408)
renderer.GetActiveCamera().SetClippingRange(12.5724, 26.8374)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
