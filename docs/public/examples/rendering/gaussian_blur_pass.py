#!/usr/bin/env python

# Demonstrate Gaussian blur render pass with depth peeling on translucent data and a cone.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkDepthPeelingPass,
    vtkGaussianBlurPass,
    vtkRenderStepsPass,
)

# Render pass pipeline: basic + depth peeling + gaussian blur
basic_passes = vtkRenderStepsPass()
peeling = vtkDepthPeelingPass()
peeling.SetMaximumNumberOfPeels(20)
peeling.SetOcclusionRatio(0.001)
peeling.SetTranslucentPass(basic_passes.GetTranslucentPass())
basic_passes.SetTranslucentPass(peeling)

blur_pass = vtkGaussianBlurPass()
blur_pass.SetDelegatePass(basic_passes)

# Sinusoidal image data surface with translucent LUT
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
actor.SetVisibility(1)

# Cone
cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetVisibility(1)

# Renderer
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
render_window.SetWindowName("gaussian blur pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(-40.0)
camera.Elevation(20.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
