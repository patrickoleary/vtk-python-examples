#!/usr/bin/env python

# Demonstrate boolean operations on implicit functions by subtracting
# a sphere from a box using vtkImplicitBoolean.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkBox,
    vtkImplicitBoolean,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
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
alice_blue_rgb = (0.941, 0.973, 1.000)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Implicit function 1: a sphere offset to the right
sphere = vtkSphere()
sphere.SetRadius(1.0)
sphere.SetCenter(1.0, 0.0, 0.0)

# Implicit function 2: an axis-aligned box
box = vtkBox()
box.SetBounds(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

# Boolean: subtract the sphere from the box (difference)
boolean = vtkImplicitBoolean()
boolean.SetOperationTypeToDifference()
boolean.AddFunction(box)
boolean.AddFunction(sphere)

# SampleFunction: evaluate the boolean on a 40x40x40 grid
sample = vtkSampleFunction()
sample.SetImplicitFunction(boolean)
sample.SetModelBounds(-1.0, 2.0, -1.0, 1.0, -1.0, 1.0)
sample.SetSampleDimensions(40, 40, 40)
sample.ComputeNormalsOff()

# Contour: extract the zero isosurface (the boolean surface)
contour = vtkContourFilter()
contour.SetInputConnection(sample.GetOutputPort())
contour.SetValue(0, 0.0)

# Mapper: map the contour surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(alice_blue_rgb)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(5.0, -4.0, 1.6)
renderer.GetActiveCamera().SetViewUp(0.1, 0.5, 0.9)
renderer.GetActiveCamera().SetDistance(6.7)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("BooleanOperationImplicitFunctions")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
