#!/usr/bin/env python

# Demonstrate vtkExtractCells to extract a subset of cells by ID from a
# sphere mesh, highlighting them in a different color.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkExtractCells
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
misty_rose_rgb = (1.000, 0.894, 0.882)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: sphere
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(20)
sphere_source.SetThetaResolution(20)
sphere_source.Update()

# Filter: extract every other cell to create a checkerboard pattern
extract_cells = vtkExtractCells()
extract_cells.SetInputConnection(sphere_source.GetOutputPort())
n_cells = sphere_source.GetOutput().GetNumberOfCells()
for i in range(0, n_cells, 2):
    extract_cells.AddCellRange(i, i)

# Filter: convert the unstructured grid output back to polydata
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(extract_cells.GetOutputPort())

# Mapper: map the extracted cells to graphics primitives
extract_mapper = vtkPolyDataMapper()
extract_mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor: assign the extracted cell geometry
extract_actor = vtkActor()
extract_actor.SetMapper(extract_mapper)
extract_actor.GetProperty().SetColor(tomato_rgb)

# Mapper: map the full sphere as wireframe context
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: wireframe context
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(misty_rose_rgb)
sphere_actor.GetProperty().SetRepresentationToWireframe()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(extract_actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract cells")
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
