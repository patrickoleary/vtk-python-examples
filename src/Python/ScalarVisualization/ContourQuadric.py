#!/usr/bin/env python

# Contour surfaces of a sampled quadric function.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkQuadric
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
slate_gray = (0.439, 0.502, 0.565)
brown = (0.647, 0.165, 0.165)

# Source: define and sample a quadric implicit function
quadric = vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(50, 50, 50)
sample.SetImplicitFunction(quadric)

# Filter: extract five contour surfaces
contour = vtkContourFilter()
contour.SetInputConnection(sample.GetOutputPort())
contour.GenerateValues(5, 0, 1.2)

# Mapper: map contour surfaces to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(0, 1.2)

# Actor: display contour surfaces
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Filter: bounding outline of the sample volume
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

# Mapper: map outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(brown)
outline_actor.GetProperty().SetLineWidth(3.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(contour_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ContourQuadric")
render_window.SetSize(640, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
