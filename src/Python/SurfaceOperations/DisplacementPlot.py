#!/usr/bin/env python

# Surface displacement plot of a vibrating plane colored by vector dot product.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkVectorDot,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "plate.vtk")

# Reader: load the plate vibration data with mode8 displacement vectors
plate = vtkPolyDataReader()
plate.SetFileName(file_name)
plate.SetVectorsName("mode8")
plate.Update()

# Filter: warp the surface by displacement vectors
warp = vtkWarpVector()
warp.SetInputConnection(plate.GetOutputPort())
warp.SetScaleFactor(0.5)

# Filter: compute surface normals on the warped geometry
normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())

# Filter: compute dot product between vectors and normals
color = vtkVectorDot()
color.SetInputConnection(normals.GetOutputPort())

# Lookup table: cool-to-warm diverging color map
nc = 256
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.230, 0.299, 0.754)
ctf.AddRGBPoint(1.0, 0.706, 0.016, 0.150)

lut = vtkLookupTable()
lut.SetNumberOfTableValues(nc)
lut.Build()
for i in range(nc):
    rgb = list(ctf.GetColor(float(i) / nc))
    rgb.append(1.0)
    lut.SetTableValue(i, *rgb)

# Mapper: map the displacement data to graphics primitives
plate_mapper = vtkDataSetMapper()
plate_mapper.SetInputConnection(color.GetOutputPort())
plate_mapper.SetLookupTable(lut)
plate_mapper.SetScalarRange(-1, 1)

# Actor: display the displacement-colored surface
plate_actor = vtkActor()
plate_actor.SetMapper(plate_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(plate_actor)
renderer.SetBackground(wheat)
cam = renderer.GetActiveCamera()
cam.SetPosition(13.3991, 14.0764, 9.97787)
cam.SetFocalPoint(1.50437, 0.481517, 4.52992)
cam.SetViewAngle(30)
cam.SetViewUp(-0.120861, 0.458556, -0.880408)
cam.SetClippingRange(12.5724, 26.8374)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("DisplacementPlot")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
