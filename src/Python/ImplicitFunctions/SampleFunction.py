#!/usr/bin/env python

# Sample an implicit superquadric function on a volume grid using
# vtkSampleFunction and extract an isosurface with vtkContourFilter.
# A bounding box outline shows the sampling volume.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkSuperquadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Implicit function: a superquadric with rounded phi and sharp theta
superquadric = vtkSuperquadric()
superquadric.SetPhiRoundness(2.5)
superquadric.SetThetaRoundness(0.5)

# SampleFunction: evaluate the superquadric on a 50x50x50 grid
sample = vtkSampleFunction()
sample.SetImplicitFunction(superquadric)
sample.SetSampleDimensions(50, 50, 50)
sample.SetModelBounds(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)

# Contour: extract the isosurface at value 2.0
contour = vtkContourFilter()
contour.SetInputConnection(sample.GetOutputPort())
contour.GenerateValues(1, 2.0, 2.0)

# Mapper: map the contour surface to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(0.0, 1.2)

# Actor: assign the mapped contour geometry
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Outline: bounding box showing the sampling volume
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(contour_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SampleFunction")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
