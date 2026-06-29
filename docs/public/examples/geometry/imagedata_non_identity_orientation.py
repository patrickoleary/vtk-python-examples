#!/usr/bin/env python
# Demonstrate oriented image data with non-identity direction matrix and point extraction.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkThresholdPoints
from vtkmodules.vtkFiltersModeling import vtkSelectEnclosedPoints
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create an oriented image data.
angle = -math.pi / 4.0
direction = [
    math.cos(angle), math.sin(angle), 0,
    -math.sin(angle), math.cos(angle), 0,
    0, 0, 1,
]
image = vtkImageData()
image.SetExtent(0, 6, 0, 10, 0, 10)
image.SetOrigin(-0.4, 0.2, -0.6)
image.SetSpacing(0.4, -0.25, 0.25)
image.SetDirectionMatrix(direction)
image.AllocateScalars(11, 0)  # VTK_DOUBLE = 11

# Create a containing surface.
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(25)
sphere_source.SetThetaResolution(38)
sphere_source.SetCenter(0, 0, 0)
sphere_source.SetRadius(2.5)

# Select points inside the sphere.
select = vtkSelectEnclosedPoints()
select.SetInputData(image)
select.SetSurfaceConnection(sphere_source.GetOutputPort())

# Threshold to extract selected points.
thresh = vtkThresholdPoints()
thresh.SetInputConnection(select.GetOutputPort())
thresh.SetInputArrayToProcess(0, 0, 0, 0, "SelectedPoints")
thresh.SetUpperThreshold(0.5)
thresh.SetThresholdFunction(2)

# Show points as glyphs.
glyph_source = vtkSphereSource()
glypher = vtkGlyph3D()
glypher.SetInputConnection(thresh.GetOutputPort())
glypher.SetSourceConnection(glyph_source.GetOutputPort())
glypher.SetScaleModeToDataScalingOff()
glypher.SetScaleFactor(0.15)

points_mapper = vtkPolyDataMapper()
points_mapper.SetInputConnection(glypher.GetOutputPort())
points_mapper.ScalarVisibilityOff()

points_actor = vtkActor()
points_actor.SetMapper(points_mapper)
points_actor.GetProperty().SetColor(0, 0, 1)

renderer = vtkRenderer()
renderer.AddActor(points_actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("imagedata non identity orientation")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
