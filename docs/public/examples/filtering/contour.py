#!/usr/bin/env python

# Sample a quadric implicit function on a volume grid and extract
# multiple iso-surfaces at different values using vtkContourFilter.

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
background_rgb = (0.2, 0.3, 0.4)

# Source: define a quadric implicit function (ellipsoid-like)
quadric_function = vtkQuadric()
quadric_function.SetCoefficients(1, 1, 1, 0, 0, 0, 0, 0, 0, -1)

# Sample: evaluate the quadric on a 50x50x50 volume grid
sample_function = vtkSampleFunction()
sample_function.SetImplicitFunction(quadric_function)
sample_function.SetModelBounds(-2, 2, -2, 2, -2, 2)
sample_function.SetSampleDimensions(50, 50, 50)
sample_function.ComputeNormalsOff()

# Filter: extract three iso-surfaces at different values
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(sample_function.GetOutputPort())
contour_filter.GenerateValues(3, -0.5, 0.5)

# Mapper: map the iso-surfaces to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour_filter.GetOutputPort())
mapper.SetScalarRange(-0.5, 0.5)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetOpacity(0.6)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("contour")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
