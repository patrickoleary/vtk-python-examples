#!/usr/bin/env python

# Generate a head isosurface using vtkSliceCubes and read it back with vtkMCubesReader.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOGeometry import vtkMCubesReader
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingHybrid import vtkSliceCubes
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read volume slices
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetImageRange(30, 50)
volume_reader.SetDataMask(0x7fff)

# Write isosurface to temporary files
slice_cubes = vtkSliceCubes()
slice_cubes.SetReader(volume_reader)
slice_cubes.SetValue(1150)
slice_cubes.SetFileName("fullHead.tri")
slice_cubes.SetLimitsFileName("fullHead.lim")
slice_cubes.Update()

# Read back the isosurface
reader = vtkMCubesReader()
reader.SetFileName("fullHead.tri")
reader.SetLimitsFileName("fullHead.lim")
reader.Update()

# Clean up temporary files
try:
    os.remove("fullHead.tri")
except OSError:
    pass
try:
    os.remove("fullHead.lim")
except OSError:
    pass

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# raw_sienna color
raw_sienna_rgb = (0.784, 0.502, 0.224)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(raw_sienna_rgb)

# slate_grey color
slate_grey_rgb = (0.439, 0.502, 0.565)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_grey_rgb)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)
render_window.SetWindowName("gen head")

# Scene
renderer.GetActiveCamera().SetPosition(99.8847, 537.926, 15)
renderer.GetActiveCamera().SetFocalPoint(99.8847, 109.81, 15)
renderer.GetActiveCamera().SetViewAngle(20)
renderer.GetActiveCamera().SetViewUp(0, 0, -1)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
