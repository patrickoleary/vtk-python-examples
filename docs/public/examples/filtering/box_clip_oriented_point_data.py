#!/usr/bin/env python

# Clip an unstructured grid (hexa.vtk) with an oriented box using
# vtkBoxClipDataSet, showing clipped-in and clipped-out surfaces
# colored by scalar data.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "hexa.vtk"))
reader.Update()

bounds = reader.GetOutput().GetBounds()
scalar_range = reader.GetOutput().GetScalarRange()

# Compute box clip region: upper half of the data
min_box_point = [
    (bounds[1] - bounds[0]) / 2.0 + bounds[0],
    (bounds[3] - bounds[2]) / 2.0 + bounds[2],
    (bounds[5] - bounds[4]) / 2.0 + bounds[4],
]
max_box_point = [bounds[1], bounds[3], bounds[5]]

# Oriented box clip using plane normals and points
box_clip = vtkBoxClipDataSet()
box_clip.SetInputConnection(reader.GetOutputPort())
box_clip.GenerateClippedOutputOn()
box_clip.SetBoxClip(
    [-1, 0, 0], min_box_point,
    [0, -1, 0], min_box_point,
    [0, 0, -1], min_box_point,
    [1, 0, 0], max_box_point,
    [0, 1, 0], max_box_point,
    [0, 0, 1], max_box_point,
)

# Lookup table
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0)
lut.Build()

# Inside surface
surface_in = vtkDataSetSurfaceFilter()
surface_in.SetInputConnection(box_clip.GetOutputPort(0))

mapper_in = vtkDataSetMapper()
mapper_in.SetInputConnection(surface_in.GetOutputPort())
mapper_in.SetScalarRange(scalar_range)
mapper_in.SetLookupTable(lut)

actor_in = vtkActor()
actor_in.SetMapper(mapper_in)

# Outside surface
surface_out = vtkDataSetSurfaceFilter()
surface_out.SetInputConnection(box_clip.GetOutputPort(1))

mapper_out = vtkDataSetMapper()
mapper_out.SetInputConnection(surface_out.GetOutputPort())
mapper_out.SetScalarRange(scalar_range)
mapper_out.SetLookupTable(lut)

actor_out = vtkActor()
actor_out.SetMapper(mapper_out)
actor_out.AddPosition(
    -0.5 * (max_box_point[0] - min_box_point[0]),
    -0.5 * (max_box_point[1] - min_box_point[1]),
    -0.5 * (max_box_point[2] - min_box_point[2]),
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor_in)
renderer.AddActor(actor_out)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("box clip oriented point data")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(120)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
