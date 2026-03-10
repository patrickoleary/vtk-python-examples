#!/usr/bin/env python

# Extract geometry from a sampled quadric using a boolean union of spheres.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkImplicitBoolean,
    vtkQuadric,
    vtkSphere,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
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

# Colors (normalized RGB)
black = (0.000, 0.000, 0.000)
slate_gray = (0.439, 0.502, 0.565)

# Source: define and sample a quadric implicit function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(50, 50, 50)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

# Implicit function: first transformed sphere
trans = vtkTransform()
trans.Scale(1, 0.5, 0.333)

sphere = vtkSphere()
sphere.SetRadius(0.25)
sphere.SetTransform(trans)

# Implicit function: second transformed sphere
trans2 = vtkTransform()
trans2.Scale(0.25, 0.5, 1.0)

sphere2 = vtkSphere()
sphere2.SetRadius(0.25)
sphere2.SetTransform(trans2)

# Implicit function: boolean union of the two spheres
boolean_union = vtkImplicitBoolean()
boolean_union.AddFunction(sphere)
boolean_union.AddFunction(sphere2)
boolean_union.SetOperationType(0)

# Filter: extract geometry within the boolean region
extract = vtkExtractGeometry()
extract.SetInputConnection(sample.GetOutputPort())
extract.SetImplicitFunction(boolean_union)

# Filter: shrink the extracted cells for visual clarity
shrink = vtkShrinkFilter()
shrink.SetInputConnection(extract.GetOutputPort())
shrink.SetShrinkFactor(0.5)

# Mapper: map extracted data to graphics primitives
data_mapper = vtkDataSetMapper()
data_mapper.SetInputConnection(shrink.GetOutputPort())

# Actor: display the extracted data
data_actor = vtkActor()
data_actor.SetMapper(data_mapper)

# Filter: bounding outline of the sample volume
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

# Mapper: map outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(data_actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ExtractData")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
