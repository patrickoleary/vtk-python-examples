#!/usr/bin/env python

# Convert a vtkImageData to vtkPolyData using vtkImageDataGeometryFilter
# and render the result.  A 2D canvas image with colored rectangles is
# created procedurally as the input.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB and byte RGBA for canvas drawing)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
steel_blue_rgba = (70, 130, 180, 255)
pale_goldenrod_rgba = (238, 232, 170, 255)

# Source: create a 2D canvas image with colored rectangles
source = vtkImageCanvasSource2D()
source.SetScalarTypeToUnsignedChar()
source.SetNumberOfScalarComponents(3)
source.SetExtent(0, 100, 0, 100, 0, 0)
source.SetDrawColor(*steel_blue_rgba)
source.FillBox(0, 100, 0, 100)
source.SetDrawColor(*pale_goldenrod_rgba)
source.FillBox(10, 20, 10, 20)
source.FillBox(40, 50, 20, 30)
source.Update()

# Filter: convert image data to polydata
geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(source.GetOutputPort())

# Mapper: map polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageDataGeometryFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
