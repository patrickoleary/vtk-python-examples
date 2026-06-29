#!/usr/bin/env python

# Demonstrate vtkDataSetSurfaceFilter with blanked image data in
# four modes: fast/non-fast and delegation on/off, showing concentric
# surfaces from clipped wavelet data resampled to an image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkClipPolyData,
    vtkResampleToImage,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate a blanked image dataset
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)

outer_sphere = vtkSphere()
outer_sphere.SetCenter(0, 0, 0)
outer_sphere.SetRadius(8)

outer_clip = vtkClipDataSet()
outer_clip.SetInputConnection(wavelet.GetOutputPort())
outer_clip.SetClipFunction(outer_sphere)
outer_clip.InsideOutOn()

inner_sphere = vtkSphere()
inner_sphere.SetCenter(2, 2, 2)
inner_sphere.SetRadius(4)

inner_clip = vtkClipDataSet()
inner_clip.SetInputConnection(outer_clip.GetOutputPort())
inner_clip.SetClipFunction(inner_sphere)

resampler = vtkResampleToImage()
resampler.UseInputBoundsOff()
resampler.SetSamplingBounds(-10, 10, -10, 10, -10, 10)
resampler.SetSamplingDimensions(100, 100, 100)
resampler.SetInputConnection(inner_clip.GetOutputPort())
resampler.Update()

dataset = resampler.GetOutputDataObject(0)

# Clip plane for half-view
plane = vtkPlane()

renderer = vtkRenderer()

# Mode 1: fast=false, delegate=false
dsf_1 = vtkDataSetSurfaceFilter()
dsf_1.SetInputData(dataset)
dsf_1.FastModeOff()
dsf_1.DelegationOff()

clipper_1 = vtkClipPolyData()
clipper_1.SetInputConnection(dsf_1.GetOutputPort())
clipper_1.SetClipFunction(plane)
clipper_1.InsideOutOn()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(clipper_1.GetOutputPort())
mapper_1.SetColorModeToMapScalars()
mapper_1.SetScalarModeToUsePointFieldData()
mapper_1.SelectColorArray("RTData")
mapper_1.SetScalarRange(37, 280)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
renderer.AddActor(actor_1)

# Mode 2: fast=true, delegate=false
dsf_2 = vtkDataSetSurfaceFilter()
dsf_2.SetInputData(dataset)
dsf_2.FastModeOn()
dsf_2.DelegationOff()

clipper_2 = vtkClipPolyData()
clipper_2.SetInputConnection(dsf_2.GetOutputPort())
clipper_2.SetClipFunction(plane)
clipper_2.InsideOutOn()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(clipper_2.GetOutputPort())
mapper_2.SetColorModeToMapScalars()
mapper_2.SetScalarModeToUsePointFieldData()
mapper_2.SelectColorArray("RTData")
mapper_2.SetScalarRange(37, 280)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.AddPosition(22, 0, 0)
renderer.AddActor(actor_2)

# Mode 3: fast=false, delegate=true
dsf_3 = vtkDataSetSurfaceFilter()
dsf_3.SetInputData(dataset)
dsf_3.FastModeOff()
dsf_3.DelegationOn()

clipper_3 = vtkClipPolyData()
clipper_3.SetInputConnection(dsf_3.GetOutputPort())
clipper_3.SetClipFunction(plane)
clipper_3.InsideOutOn()

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(clipper_3.GetOutputPort())
mapper_3.SetColorModeToMapScalars()
mapper_3.SetScalarModeToUsePointFieldData()
mapper_3.SelectColorArray("RTData")
mapper_3.SetScalarRange(37, 280)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.AddPosition(0, -22, 0)
renderer.AddActor(actor_3)

# Mode 4: fast=true, delegate=true
dsf_4 = vtkDataSetSurfaceFilter()
dsf_4.SetInputData(dataset)
dsf_4.FastModeOn()
dsf_4.DelegationOn()

clipper_4 = vtkClipPolyData()
clipper_4.SetInputConnection(dsf_4.GetOutputPort())
clipper_4.SetClipFunction(plane)
clipper_4.InsideOutOn()

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(clipper_4.GetOutputPort())
mapper_4.SetColorModeToMapScalars()
mapper_4.SetScalarModeToUsePointFieldData()
mapper_4.SelectColorArray("RTData")
mapper_4.SetScalarRange(37, 280)

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.AddPosition(22, -22, 0)
renderer.AddActor(actor_4)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("dataset surface filter with blanked imagedata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
