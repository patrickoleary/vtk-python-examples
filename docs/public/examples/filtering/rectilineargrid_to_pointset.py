#!/usr/bin/env python

# Demonstrate vtkRectilinearGridToPointSet by creating a rectilinear grid
# with non-uniform spacing, converting it to a structured grid, and
# rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkFiltersGeneral import vtkRectilinearGridToPointSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a rectilinear grid with non-uniform spacing
x_coords = vtkDoubleArray()
for v in [0.0, 0.5, 1.5, 3.0, 5.0]:
    x_coords.InsertNextValue(v)

y_coords = vtkDoubleArray()
for v in [0.0, 1.0, 2.0, 4.0]:
    y_coords.InsertNextValue(v)

z_coords = vtkDoubleArray()
for v in [0.0, 0.5, 2.0]:
    z_coords.InsertNextValue(v)

rect_grid = vtkRectilinearGrid()
rect_grid.SetDimensions(5, 4, 3)
rect_grid.SetXCoordinates(x_coords)
rect_grid.SetYCoordinates(y_coords)
rect_grid.SetZCoordinates(z_coords)

# Convert to structured grid (point set)
rect_to_points = vtkRectilinearGridToPointSet()
rect_to_points.SetInputData(rect_grid)

# Extract surface for rendering
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(rect_to_points.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetEdgeVisibility(True)
actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("rectilineargrid to pointset")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
