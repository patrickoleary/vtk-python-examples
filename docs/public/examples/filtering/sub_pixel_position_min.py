#!/usr/bin/env python

# Sub-pixel positioning of edgels on a sampled sphere using
# vtkSubPixelPositionEdgels.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkCommonExecutionModel import vtkImageToStructuredPoints
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeneral import vtkSubPixelPositionEdgels
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(1, 1, 1)
sphere.SetRadius(0.9)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(0, 2, 0, 2, 0, 2)
sample.SetSampleDimensions(30, 30, 30)
sample.ComputeNormalsOff()
sample.Update()

# Threshold to get cells near the surface
threshold = vtkThreshold()
threshold.SetInputConnection(sample.GetOutputPort())
threshold.SetThresholdFunction(vtkThreshold.THRESHOLD_LOWER)
threshold.SetLowerThreshold(0.001)

geometry = vtkGeometryFilter()
geometry.SetInputConnection(threshold.GetOutputPort())

# Compute gradient
grad = vtkImageGradient()
grad.SetDimensionality(3)
grad.SetInputConnection(sample.GetOutputPort())
grad.Update()

# Square the scalar field
mult = vtkImageMathematics()
mult.SetOperationToMultiply()
mult.SetInput1Data(sample.GetOutput())
mult.SetInput2Data(sample.GetOutput())

itosp = vtkImageToStructuredPoints()
itosp.SetInputConnection(mult.GetOutputPort())
itosp.SetVectorInputData(grad.GetOutput())
itosp.Update()

# Sub-pixel position the edgels
sub = vtkSubPixelPositionEdgels()
sub.SetInputConnection(geometry.GetOutputPort())
sub.SetGradMapsData(itosp.GetOutput())

mapper = vtkDataSetMapper()
mapper.SetInputConnection(sub.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("sub pixel position min")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(20)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Zoom(1.4)

interactor.Initialize()
interactor.Start()
