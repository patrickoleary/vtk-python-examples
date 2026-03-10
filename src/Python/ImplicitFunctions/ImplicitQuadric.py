#!/usr/bin/env python

# Visualize an implicit quadric surface (ellipsoid) by sampling it on
# a volume grid and extracting the zero isosurface with vtkContourFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkQuadric
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

# Implicit function: a quadric surface (ellipsoid)
# F(x,y,z) = 0.5x² + y² + 0.2z² + 0.1xz + 0.2y = 0
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1.0, 0.2, 0.0, 0.1, 0.0, 0.0, 0.2, 0.0, 0.0)

# SampleFunction: evaluate the implicit quadric on a 40x40x40 grid
sample = vtkSampleFunction()
sample.SetImplicitFunction(quadric)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(40, 40, 40)
sample.ComputeNormalsOff()

# Contour: extract the zero isosurface (the quadric surface)
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

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitQuadric")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
