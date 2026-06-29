#!/usr/bin/env python

# Test vtkImageProbeFilter with plane and sphere probing on a CT volume.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable, vtkMath
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageInterpolator,
    vtkImageMapToColors,
    vtkImageProbeFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image file info
extent = [0, 63, 0, 63, 1, 93]
origin = [0.0, 0.0, 0.0]
spacing = [3.2, 3.2, 1.5]

# Read CT image
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(extent)
reader.SetDataOrigin(origin)
reader.SetDataSpacing(spacing)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Grayscale lookup table
table = vtkLookupTable()
table.SetRampToLinear()
table.SetRange(0.0, 4095.0)
table.SetValueRange(0.0, 1.0)
table.SetSaturationRange(0.0, 0.0)
table.Build()

# Create RGBA data
colors = vtkImageMapToColors()
colors.SetOutputFormatToRGBA()
colors.SetInputConnection(reader.GetOutputPort())
colors.SetLookupTable(table)

# --- Viewport 0 (upper left): probe RGBA onto plane, default ---
plane_0 = vtkPlaneSource()
plane_0.SetOrigin(0.0, 0.0, 69.75)
plane_0.SetPoint1(201.6, 0.0, 69.75)
plane_0.SetPoint2(0.0, 201.6, 69.75)
plane_0.SetXResolution(63)
plane_0.SetYResolution(63)

probe_0 = vtkImageProbeFilter()
probe_0.SetSourceConnection(colors.GetOutputPort())
probe_0.SetInputConnection(plane_0.GetOutputPort())

mapper_0 = vtkDataSetMapper()
mapper_0.SetInputConnection(probe_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)

# --- Viewport 1 (upper right): probe RGBA onto plane, cubic ---
plane_1 = vtkPlaneSource()
plane_1.SetOrigin(0.0, 0.0, 69.75)
plane_1.SetPoint1(201.6, 0.0, 69.75)
plane_1.SetPoint2(0.0, 201.6, 69.75)
plane_1.SetXResolution(255)
plane_1.SetYResolution(255)

interpolator_1 = vtkImageInterpolator()
interpolator_1.SetInterpolationModeToCubic()

probe_1 = vtkImageProbeFilter()
probe_1.SetInterpolator(interpolator_1)
probe_1.SetSourceConnection(colors.GetOutputPort())
probe_1.SetInputConnection(plane_1.GetOutputPort())

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(probe_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)

# --- Viewport 2 (lower left): probe int data onto oblique plane, cubic ---
center = [100.8, 100.8, 69.75]
point_0_oblique = [0.0, 0.0, 69.75]
point_1_oblique = [201.6, 0.0, 69.75]
point_2_oblique = [0.0, 201.6, 69.75]

transform_2 = vtkTransform()
transform_2.PostMultiply()
transform_2.Translate(-center[0], -center[1], -center[2])
transform_2.RotateWXYZ(-20.0, 0.99388, 0.0, 0.11043)
transform_2.Translate(center[0], center[1], center[2])
point_0_oblique = list(transform_2.TransformPoint(point_0_oblique))
point_1_oblique = list(transform_2.TransformPoint(point_1_oblique))
point_2_oblique = list(transform_2.TransformPoint(point_2_oblique))

plane_2 = vtkPlaneSource()
plane_2.SetOrigin(point_0_oblique)
plane_2.SetPoint1(point_1_oblique)
plane_2.SetPoint2(point_2_oblique)
plane_2.SetXResolution(255)
plane_2.SetYResolution(255)

interpolator_2 = vtkImageInterpolator()
interpolator_2.SetInterpolationModeToCubic()

probe_2 = vtkImageProbeFilter()
probe_2.SetInterpolator(interpolator_2)
probe_2.SetSourceConnection(reader.GetOutputPort())
probe_2.SetInputConnection(plane_2.GetOutputPort())

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(probe_2.GetOutputPort())
mapper_2.SetLookupTable(table)
mapper_2.UseLookupTableScalarRangeOn()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)

# --- Viewport 3 (lower right): probe float data onto sphere, linear ---
surface = vtkSphereSource()
surface.SetCenter(100.8, 100.8, 69.75)
surface.SetRadius(60.0)
surface.SetPhiResolution(200)
surface.SetThetaResolution(200)

cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToFloat()

interpolator_3 = vtkImageInterpolator()

probe_3 = vtkImageProbeFilter()
probe_3.SetInterpolator(interpolator_3)
probe_3.SetSourceConnection(cast.GetOutputPort())
probe_3.SetInputConnection(surface.GetOutputPort())

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(probe_3.GetOutputPort())
mapper_3.SetLookupTable(table)
mapper_3.UseLookupTableScalarRangeOn()

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(512, 512)
render_window.SetWindowName("image probe")

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().ParallelProjectionOn()
renderer_0.GetActiveCamera().SetParallelScale(102.4)

renderer_1.ResetCamera()
renderer_1.GetActiveCamera().ParallelProjectionOn()
renderer_1.GetActiveCamera().SetParallelScale(102.4)

renderer_2.ResetCamera()
renderer_2.GetActiveCamera().ParallelProjectionOn()
renderer_2.GetActiveCamera().SetParallelScale(102.4)

renderer_3.ResetCamera()
renderer_3.GetActiveCamera().ParallelProjectionOn()
renderer_3.GetActiveCamera().SetParallelScale(102.4)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
