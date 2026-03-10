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
nx, ny = 20, 20
grid = vtkStructuredGrid()
grid.SetDimensions(nx, ny, 1)

points = vtkPoints()
scalars = vtkFloatArray()
scalars.SetName("Height")

for j in range(ny):
    for i in range(nx):
        x = i / (nx - 1.0) * 4.0 - 2.0
        y = j / (ny - 1.0) * 4.0 - 2.0
        z = math.exp(-(x * x + y * y))
        points.InsertNextPoint(x, y, 0)
        scalars.InsertNextValue(z)

grid.SetPoints(points)
grid.GetPointData().SetScalars(scalars)

# Filter: compute gradient of the scalar field
gradient = vtkGradientFilter()
gradient.SetInputData(grid)
gradient.SetInputScalars(0, "Height")
gradient.SetResultArrayName("Gradient")

# Filter: extract surface geometry for the colored base
surface = vtkStructuredGridGeometryFilter()
surface.SetInputData(grid)

# Mapper: map the surface to graphics primitives with scalar coloring
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(surface.GetOutputPort())
surface_mapper.SetScalarRange(grid.GetScalarRange())

# Actor: assign the colored surface geometry
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Source: arrow glyph shape
arrow = vtkArrowSource()

# Filter: place arrow glyphs oriented along gradient vectors
glyphs = vtkGlyph3D()
glyphs.SetInputConnection(gradient.GetOutputPort())
glyphs.SetSourceConnection(arrow.GetOutputPort())
glyphs.SetVectorModeToUseVector()
glyphs.SetInputArrayToProcess(1, 0, 0, 0, "Gradient")
glyphs.SetScaleFactor(0.5)
glyphs.OrientOn()

# Mapper: map the arrow glyphs to graphics primitives
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyphs.GetOutputPort())
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

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("GradientFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
