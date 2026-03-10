#!/usr/bin/env python

# Create a rectilinear grid and extract a plane using a geometry filter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
banana_rgb = (0.890, 0.812, 0.341)
beige_rgb = (0.961, 0.961, 0.863)

# Source: define coordinates along each axis
x = [-1.22396, -1.17188, -1.11979, -1.06771, -1.01562, -0.963542, -0.911458,
     -0.859375, -0.807292, -0.755208, -0.703125, -0.651042, -0.598958,
     -0.546875, -0.494792, -0.442708, -0.390625, -0.338542, -0.286458,
     -0.234375, -0.182292, -0.130209, -0.078125, -0.026042, 0.0260415,
     0.078125, 0.130208, 0.182291, 0.234375, 0.286458, 0.338542, 0.390625,
     0.442708, 0.494792, 0.546875, 0.598958, 0.651042, 0.703125, 0.755208,
     0.807292, 0.859375, 0.911458, 0.963542, 1.01562, 1.06771, 1.11979,
     1.17188]
y = [-1.25, -1.17188, -1.09375, -1.01562, -0.9375, -0.859375, -0.78125,
     -0.703125, -0.625, -0.546875, -0.46875, -0.390625, -0.3125, -0.234375,
     -0.15625, -0.078125, 0, 0.078125, 0.15625, 0.234375, 0.3125, 0.390625,
     0.46875, 0.546875, 0.625, 0.703125, 0.78125, 0.859375, 0.9375, 1.01562,
     1.09375, 1.17188, 1.25]
z = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1, 1.1, 1.2,
     1.3, 1.4, 1.5, 1.6, 1.7, 1.75, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5,
     2.6, 2.7, 2.75, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.75,
     3.8, 3.9]

x_coords = vtkDoubleArray()
for val in x:
    x_coords.InsertNextValue(val)

y_coords = vtkDoubleArray()
for val in y:
    y_coords.InsertNextValue(val)

z_coords = vtkDoubleArray()
for val in z:
    z_coords.InsertNextValue(val)

# RectilinearGrid: assemble the grid from coordinate arrays
rgrid = vtkRectilinearGrid()
rgrid.SetDimensions(len(x), len(y), len(z))
rgrid.SetXCoordinates(x_coords)
rgrid.SetYCoordinates(y_coords)
rgrid.SetZCoordinates(z_coords)

# GeometryFilter: extract a plane (constant y=16) from the grid
plane = vtkRectilinearGridGeometryFilter()
plane.SetInputData(rgrid)
plane.SetExtent(0, len(x) - 1, 16, 16, 0, len(z) - 1)

# Mapper: map the extracted plane to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(plane.GetOutputPort())

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(banana_rgb)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(beige_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
