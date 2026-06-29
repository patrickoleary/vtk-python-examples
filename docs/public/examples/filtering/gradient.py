#!/usr/bin/env python

# Demonstrate vtkGradientFilter to compute gradient vectors of a scalar field
# on a structured grid, then visualize them as arrow glyphs.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersGeneral import vtkGradientFilter
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Build a 2D structured grid with a Gaussian scalar field
grid_nx, grid_ny = 20, 20
structured_grid = vtkStructuredGrid()
structured_grid.SetDimensions(grid_nx, grid_ny, 1)

points = vtkPoints()
height_scalars = vtkFloatArray()
height_scalars.SetName("Height")

for j in range(grid_ny):
    for i in range(grid_nx):
        x = i / (grid_nx - 1.0) * 4.0 - 2.0
        y = j / (grid_ny - 1.0) * 4.0 - 2.0
        z = math.exp(-(x * x + y * y))
        points.InsertNextPoint(x, y, 0)
        height_scalars.InsertNextValue(z)

structured_grid.SetPoints(points)
structured_grid.GetPointData().SetScalars(height_scalars)

# Filter: compute gradient of the scalar field
gradient_filter = vtkGradientFilter()
gradient_filter.SetInputData(structured_grid)
gradient_filter.SetInputScalars(0, "Height")
gradient_filter.SetResultArrayName("Gradient")

# Filter: extract surface geometry for the colored base
geometry_filter = vtkStructuredGridGeometryFilter()
geometry_filter.SetInputData(structured_grid)

# Mapper: map the surface to graphics primitives with scalar coloring
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(geometry_filter.GetOutputPort())
surface_mapper.SetScalarRange(structured_grid.GetScalarRange())

# Actor: assign the colored surface geometry
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Source: arrow glyph shape
arrow_source = vtkArrowSource()

# Filter: place arrow glyphs oriented along gradient vectors
glyph_filter = vtkGlyph3D()
glyph_filter.SetInputConnection(gradient_filter.GetOutputPort())
glyph_filter.SetSourceConnection(arrow_source.GetOutputPort())
glyph_filter.SetVectorModeToUseVector()
glyph_filter.SetInputArrayToProcess(1, 0, 0, 0, "Gradient")
glyph_filter.SetScaleFactor(0.5)
glyph_filter.OrientOn()

# Mapper: map the arrow glyphs to graphics primitives
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph_filter.GetOutputPort())
glyph_mapper.ScalarVisibilityOff()

# Actor: assign the arrow glyph geometry
glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(tomato_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gradient")
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
