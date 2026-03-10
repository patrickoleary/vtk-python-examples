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
sphere = vtkSphereSource()
sphere.SetPhiResolution(20)
sphere.SetThetaResolution(20)
sphere.Update()

# Filter: extract every other cell to create a checkerboard pattern
extract = vtkExtractCells()
extract.SetInputConnection(sphere.GetOutputPort())
n_cells = sphere.GetOutput().GetNumberOfCells()
for i in range(0, n_cells, 2):
    extract.AddCellRange(i, i)

# Filter: convert the unstructured grid output back to polydata
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(extract.GetOutputPort())

# Mapper: map the extracted cells to graphics primitives
extract_mapper = vtkPolyDataMapper()
extract_mapper.SetInputConnection(surface.GetOutputPort())

# Actor: assign the extracted cell geometry
extract_actor = vtkActor()
extract_actor.SetMapper(extract_mapper)
extract_actor.GetProperty().SetColor(tomato_rgb)

# Mapper: map the full sphere as wireframe context
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

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

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ExtractCells")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
