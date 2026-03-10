#!/usr/bin/env python

# Visualize a rectilinear grid with shrunk cells to reveal structure.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.000, 0.855, 0.725)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: create a 2x3x2 rectilinear grid
grid = vtkRectilinearGrid()
grid.SetDimensions(2, 3, 2)

x_array = vtkDoubleArray()
x_array.InsertNextValue(0.0)
x_array.InsertNextValue(2.0)

y_array = vtkDoubleArray()
y_array.InsertNextValue(0.0)
y_array.InsertNextValue(1.0)
y_array.InsertNextValue(2.0)

z_array = vtkDoubleArray()
z_array.InsertNextValue(0.0)
z_array.InsertNextValue(5.0)

grid.SetXCoordinates(x_array)
grid.SetYCoordinates(y_array)
grid.SetZCoordinates(z_array)

# ShrinkFilter: shrink each cell to reveal grid structure
shrink = vtkShrinkFilter()
shrink.SetInputData(grid)
shrink.SetShrinkFactor(0.8)

# Mapper: map the shrunk grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)
renderer.GetActiveCamera().Roll(10.0)
renderer.GetActiveCamera().Elevation(60.0)
renderer.GetActiveCamera().Azimuth(30.0)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("VisualizeRectilinearGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
