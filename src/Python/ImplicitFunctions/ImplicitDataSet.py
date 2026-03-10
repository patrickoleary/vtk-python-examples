#!/usr/bin/env python

# Use vtkImplicitDataSet to clip a sphere with a sampled implicit box.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkBox,
    vtkImplicitDataSet,
)
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
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
tomato_rgb = (1.0, 0.388, 0.278)
light_grey_rgb = (0.827, 0.827, 0.827)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: a high-resolution sphere offset so it partially overlaps the box
sphere = vtkSphereSource()
sphere.SetCenter(0.5, 0.5, 0.5)
sphere.SetRadius(1.0)
sphere.SetThetaResolution(40)
sphere.SetPhiResolution(40)

# ImplicitBox: define an axis-aligned box as an implicit function.
# vtkBox evaluates to negative inside, zero on the surface, positive outside.
box = vtkBox()
box.SetBounds(-1, 1, -1, 1, -1, 1)

# SampleFunction: evaluate the implicit box on a regular 3D grid.
# This produces a vtkImageData with scalar values (distance to box surface).
# vtkImplicitDataSet needs a dataset with scalars to interpolate.
sampler = vtkSampleFunction()
sampler.SetImplicitFunction(box)
sampler.SetModelBounds(-1.5, 1.5, -1.5, 1.5, -1.5, 1.5)
sampler.SetSampleDimensions(30, 30, 30)
sampler.ComputeNormalsOff()
sampler.Update()

# ImplicitDataSet: wrap the sampled volume as an implicit function.
# The scalar field in the dataset defines inside (negative) vs outside
# (positive), allowing it to be used as a clip function.
implicit = vtkImplicitDataSet()
implicit.SetDataSet(sampler.GetOutput())

# Clip: cut the sphere using the implicit dataset
clipper = vtkClipPolyData()
clipper.SetClipFunction(implicit)
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.InsideOutOn()

# Mapper: map the clipped sphere
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())

# Actor: display the clipped sphere
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetSpecular(0.4)
actor.GetProperty().SetSpecularPower(20)

# Context: show the box region as a wireframe for reference
box_mapper = vtkDataSetMapper()
box_mapper.SetInputConnection(sampler.GetOutputPort())
box_mapper.ScalarVisibilityOff()

box_actor = vtkActor()
box_actor.SetMapper(box_mapper)
box_actor.GetProperty().SetRepresentationToWireframe()
box_actor.GetProperty().SetColor(light_grey_rgb)
box_actor.GetProperty().SetOpacity(0.3)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(box_actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitDataSet")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
