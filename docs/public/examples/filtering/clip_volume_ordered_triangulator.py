#!/usr/bin/env python

# Generate a 3D tetrahedral mesh from a volume using the ordered
# triangulator with clip scalars, clipping a bandpass range of a
# sampled quadric function.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImplicitDataSet,
    vtkImplicitWindowFunction,
    vtkQuadric,
)
from vtkmodules.vtkFiltersGeneral import vtkClipVolume
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Quadric definition
quadric = vtkQuadric()
quadric.SetCoefficients([0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0])

sample = vtkSampleFunction()
sample.SetSampleDimensions(20, 20, 20)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()
sample.Update()

# Program a bandpass filter to clip a range of data
dataset = vtkImplicitDataSet()
dataset.SetDataSet(sample.GetOutput())

window = vtkImplicitWindowFunction()
window.SetImplicitFunction(dataset)
window.SetWindowRange(0.5, 1.0)

# Generate tetrahedral mesh with ordered triangulator
clip = vtkClipVolume()
clip.SetInputConnection(sample.GetOutputPort())
clip.SetClipFunction(window)
clip.SetValue(0.0)
clip.GenerateClippedOutputOff()
clip.Mixed3DCellGenerationOff()

gf = vtkGeometryFilter()
gf.SetInputConnection(clip.GetOutputPort())

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(gf.GetOutputPort())
clip_mapper.ScalarVisibilityOn()
clip_mapper.SetScalarRange(0, 2)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(clip_actor)
renderer.AddActor(outline_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("clip volume ordered triangulator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
