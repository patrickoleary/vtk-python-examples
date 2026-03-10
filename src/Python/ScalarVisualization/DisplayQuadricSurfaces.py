#!/usr/bin/env python

# Display quadric surfaces by sampling and contouring implicit functions.

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
black = (0.000, 0.000, 0.000)
alice_blue = (0.941, 0.973, 1.000)

# Quadric surface definitions: (coefficients, contour_value)
# F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9
surfaces = {
    "Sphere":                ((1, 1, 1, 0, 0, 0, 0, 0, 0, 0), 1.0),
    "EllipticParaboloid":    ((1, 1, 0, 0, 0, 0, 0, 0, -1, 0), 10.0),
    "HyperbolicParaboloid":  ((1, -1, 0, 0, 0, 0, 0, 0, 0, 0), 10.0),
    "Cylinder":              ((1, 1, 0, 0, 0, 0, 0, 0, 0, 0), 1.0),
    "HyperboloidOneSheet":   ((1, 1, -1, 0, 0, 0, 0, 0, 0, 0), 1.0),
    "HyperboloidTwoSheets":  ((1, 1, -1, 0, 0, 0, 0, 0, 0, 0), -1.0),
    "Ellipsoid":             ((1, 1, 2, 0, 0, 0, 0, 0, 0, 0), 1.0),
    "Cone":                  ((1, 1, -1, 0, 0, 0, 0, 0, 0, 0), 0.0),
    "Other":                 ((0.5, 1, 0.2, 0, 0.1, 0, 0, 0.2, 0, 0), 1.0),
}

# Select which surface to display
coefficients, contour_value = surfaces["EllipticParaboloid"]

# Source: define the quadric implicit function
quadric = vtkQuadric()
quadric.SetCoefficients(*coefficients)

# Source: sample the quadric on a regular grid
sample = vtkSampleFunction()
sample.SetSampleDimensions(50, 50, 50)
sample.SetImplicitFunction(quadric)
sample.SetModelBounds(-10, 11, -10, 10, -10, 10)

# Filter: extract the isosurface at the specified value
contours = vtkContourFilter()
contours.SetInputConnection(sample.GetOutputPort())
contours.GenerateValues(1, contour_value, contour_value)

# Mapper: map contour surface to graphics primitives
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contours.GetOutputPort())
contour_mapper.SetScalarRange(0.0, 1.2)

# Actor: display the contour surface
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Filter: bounding outline of the sampling volume
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
renderer.AddActor(contour_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(alice_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("DisplayQuadricSurfaces")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(-55)
renderer.GetActiveCamera().Elevation(15)

# Launch the interactive visualization
render_window_interactor.Start()
