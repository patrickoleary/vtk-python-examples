#!/usr/bin/env python

# Demonstrate a standalone scalar bar annotation showing a color lookup
# table mapped to elevation on a sphere source.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a sphere
source = vtkSphereSource()
source.SetThetaResolution(30)
source.SetPhiResolution(30)

# Filter: compute elevation scalar values along the Z axis
elevation = vtkElevationFilter()
elevation.SetInputConnection(source.GetOutputPort())
elevation.SetLowPoint(0, 0, -0.5)
elevation.SetHighPoint(0, 0, 0.5)

# Lookup table: map scalar values to a blue-to-red color ramp
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.Build()

# Mapper: map polygon data to graphics primitives with scalar coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarRange(0.0, 1.0)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Scalar bar: display the color legend
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)
scalar_bar.SetTitle("Elevation")
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetOrientationToVertical()
scalar_bar.SetWidth(0.08)
scalar_bar.SetHeight(0.6)
scalar_bar.SetPosition(0.9, 0.2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(scalar_bar)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ScalarBarActor")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
