#!/usr/bin/env python

# Demonstrate Gaussian blur followed by Sobel edge detection render passes on a cone.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkLightsPass,
    vtkOpaquePass,
    vtkOverlayPass,
    vtkRenderPassCollection,
    vtkSequencePass,
    vtkTranslucentPass,
    vtkVolumetricPass,
    vtkGaussianBlurPass,
    vtkSobelGradientMagnitudePass,
)

# Render pass pipeline
camera_pass = vtkCameraPass()
seq = vtkSequencePass()
opaque = vtkOpaquePass()
translucent = vtkTranslucentPass()
volume = vtkVolumetricPass()
overlay = vtkOverlayPass()
lights = vtkLightsPass()

passes = vtkRenderPassCollection()
passes.AddItem(lights)
passes.AddItem(opaque)
passes.AddItem(translucent)
passes.AddItem(volume)
passes.AddItem(overlay)
seq.SetPasses(passes)
camera_pass.SetDelegatePass(seq)

# Sobel gradient magnitude pass wrapping camera pass
sobel_pass = vtkSobelGradientMagnitudePass()
sobel_pass.SetDelegatePass(camera_pass)

# Gaussian blur pass wrapping Sobel pass
blur_pass = vtkGaussianBlurPass()
blur_pass.SetDelegatePass(sobel_pass)

# Sinusoidal image data surface (invisible, from original test)
image_source = vtkRTAnalyticSource()
image_source.SetWholeExtent(0, 9, 0, 9, 0, 9)
image_source.Update()
scalar_range = image_source.GetOutput().GetScalarRange()

surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(image_source.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

lut = vtkLookupTable()
lut.SetTableRange(scalar_range)
lut.SetAlphaRange(0.5, 0.5)
lut.SetHueRange(0.2, 0.7)
lut.SetNumberOfTableValues(256)
lut.Build()
mapper.SetScalarVisibility(1)
mapper.SetLookupTable(lut)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetVisibility(0)

# Cone (visible)
cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetVisibility(1)

# Renderer with custom pass
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.3, 0.0)
renderer.SetPass(blur_pass)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("blur and sobel passes")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(-40.0)
camera.Elevation(20.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
