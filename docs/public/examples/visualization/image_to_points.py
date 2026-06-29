#!/usr/bin/env python

# Test vtkImageToPoints by converting CT slices to glyphed point set.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkScalarsToColors
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithm
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingHybrid import vtkImageToPoints
from vtkmodules.vtkImagingStencil import vtkImageToImageStencil
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Volume parameters
extent = [0, 63, 0, 63, 0, 3]
origin = [0.0, 0.0, 0.0]
spacing = [3.2, 3.2, 1.5]
center = [0.5 * 3.2 * 63, 0.5 * 3.2 * 63, 0.5 * 1.5 * 3]

# Read CT slices
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(extent)
reader.SetDataOrigin(origin)
reader.SetDataSpacing(spacing)
reader.SetFileNameSliceOffset(40)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Convert image to color scalars
table = vtkScalarsToColors()
table.SetRange(0, 2000)

colors = vtkImageMapToColors()
colors.SetInputConnection(reader.GetOutputPort())
colors.SetLookupTable(table)
colors.SetOutputFormatToRGB()

# Generate a stencil by thresholding the image
stencil = vtkImageToImageStencil()
stencil.SetInputConnection(reader.GetOutputPort())
stencil.ThresholdBetween(800, 4000)

# Generate point set from image
image_to_point_set = vtkImageToPoints()
image_to_point_set.SetInputConnection(colors.GetOutputPort())
image_to_point_set.SetStencilConnection(stencil.GetOutputPort())
image_to_point_set.SetOutputPointsPrecision(vtkAlgorithm.SINGLE_PRECISION)
image_to_point_set.Update()

# Sphere glyph source
sphere = vtkSphereSource()
sphere.SetRadius(1.5)

# Display points as glyphs
mapper = vtkGlyph3DMapper()
mapper.ScalingOff()
mapper.SetInputConnection(image_to_point_set.GetOutputPort())
mapper.SetSourceConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddViewProp(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("image to points")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(center)
camera.SetPosition(center[0], center[1], center[2] - 400.0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
