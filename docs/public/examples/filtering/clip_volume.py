#!/usr/bin/env python

# Generate a 3D tetrahedral mesh from a volume by clipping a sampled
# quadric function using vtkClipVolume.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersGeneral import vtkClipVolume
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
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

# Generate tetrahedral mesh
clip = vtkClipVolume()
clip.SetInputConnection(sample.GetOutputPort())
clip.SetValue(1.0)
clip.GenerateClippedOutputOff()

clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

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
render_window.SetWindowName("clip volume")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
