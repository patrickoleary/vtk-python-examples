#!/usr/bin/env python

# Demonstrate 3D morphing between letters v, t, k using vtkImplicitModeller
# and vtkInterpolateDataSetAttributes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeneral import vtkInterpolateDataSetAttributes
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Make the letters v, t, and k
letter_v = vtkVectorText()
letter_v.SetText("v")

letter_t = vtkVectorText()
letter_t.SetText("t")

letter_k = vtkVectorText()
letter_k.SetText("k")

# Create implicit models of each
blobby_v = vtkImplicitModeller()
blobby_v.SetInputConnection(letter_v.GetOutputPort())
blobby_v.SetMaximumDistance(0.2)
blobby_v.SetSampleDimensions(50, 50, 12)
blobby_v.SetModelBounds(-0.5, 1.5, -0.5, 1.5, -0.5, 0.5)

blobby_t = vtkImplicitModeller()
blobby_t.SetInputConnection(letter_t.GetOutputPort())
blobby_t.SetMaximumDistance(0.2)
blobby_t.SetSampleDimensions(50, 50, 12)
blobby_t.SetModelBounds(-0.5, 1.5, -0.5, 1.5, -0.5, 0.5)

blobby_k = vtkImplicitModeller()
blobby_k.SetInputConnection(letter_k.GetOutputPort())
blobby_k.SetMaximumDistance(0.2)
blobby_k.SetSampleDimensions(50, 50, 12)
blobby_k.SetModelBounds(-0.5, 1.5, -0.5, 1.5, -0.5, 0.5)

# Interpolate the data
interpolate = vtkInterpolateDataSetAttributes()
interpolate.AddInputConnection(blobby_v.GetOutputPort())
interpolate.AddInputConnection(blobby_t.GetOutputPort())
interpolate.AddInputConnection(blobby_k.GetOutputPort())
interpolate.SetT(0.0)

# Extract an iso surface
blobby_iso = vtkContourFilter()
blobby_iso.SetInputConnection(interpolate.GetOutputPort())
blobby_iso.SetValue(0, 0.1)

# Map to rendering primitives
blobby_mapper = vtkPolyDataMapper()
blobby_mapper.SetInputConnection(blobby_iso.GetOutputPort())
blobby_mapper.ScalarVisibilityOff()

blobby_actor = vtkActor()
blobby_actor.SetMapper(blobby_mapper)
blobby_actor.GetProperty().SetDiffuseColor(0.89, 0.81, 0.34)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(blobby_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 350)
render_window.SetWindowName("3d morph")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetClippingRange(0.265, 13.2)
camera.SetFocalPoint(0.539, 0.47464, 0)
camera.SetPosition(0.539, 0.474674, 2.644)
camera.SetViewUp(0, 1, 0)
renderer.SetActiveCamera(camera)

# Animate morphing through letters
sub_iters = 4.0
i = 0
while i < 2:
    j = 1
    while j <= sub_iters:
        t = i + j / sub_iters
        interpolate.SetT(t)
        render_window.Render()
        j += 1
    i += 1

interactor.Initialize()
interactor.Start()
