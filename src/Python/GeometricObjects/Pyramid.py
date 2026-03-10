#!/usr/bin/env python

# Construct and render a pyramid using vtkPyramid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkPyramid,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
silver_background_rgb = (0.75, 0.75, 0.75)

# Data: five points — a square base and an apex
points = vtkPoints()
points.InsertNextPoint(1.0, 1.0, 1.0)
points.InsertNextPoint(-1.0, 1.0, 1.0)
points.InsertNextPoint(-1.0, -1.0, 1.0)
points.InsertNextPoint(1.0, -1.0, 1.0)
points.InsertNextPoint(0.0, 0.0, 0.0)

# Cell: a pyramid referencing the 5 points
pyramid = vtkPyramid()
pyramid.GetPointIds().SetId(0, 0)
pyramid.GetPointIds().SetId(1, 1)
pyramid.GetPointIds().SetId(2, 2)
pyramid.GetPointIds().SetId(3, 3)
pyramid.GetPointIds().SetId(4, 4)

# Unstructured grid: store the pyramid cell
unstructured_grid = vtkUnstructuredGrid()
unstructured_grid.SetPoints(points)
unstructured_grid.InsertNextCell(pyramid.GetCellType(), pyramid.GetPointIds())

# Mapper: map the unstructured grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(unstructured_grid)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(180)
renderer.GetActiveCamera().Elevation(-20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Pyramid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
