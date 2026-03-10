#!/usr/bin/env python

# Visualize an implicit superquadric by sampling it on a volume grid
# and extracting the zero isosurface with vtkContourFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkSuperquadric
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

# Implicit function: a toroidal superquadric
superquadric = vtkSuperquadric()
superquadric.SetPhiRoundness(0.3)
superquadric.SetThetaRoundness(0.4)
superquadric.SetToroidal(1)
superquadric.SetSize(0.5)
superquadric.SetThickness(0.33)

# SampleFunction: evaluate the superquadric on a 60x60x60 grid
sample = vtkSampleFunction()
sample.SetImplicitFunction(superquadric)
sample.SetSampleDimensions(60, 60, 60)
sample.SetModelBounds(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
sample.ComputeNormalsOff()

# Contour: extract the zero isosurface (the superquadric surface)
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
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitSuperquadric")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
