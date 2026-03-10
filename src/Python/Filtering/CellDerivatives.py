#!/usr/bin/env python

# Demonstrate vtkCellDerivatives to compute vorticity from a procedural
# velocity field on a structured grid, then color the surface by vorticity
# magnitude.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersGeneral import vtkCellDerivatives
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Build a 2D structured grid with a swirling velocity field
nx, ny = 30, 30
grid = vtkStructuredGrid()
grid.SetDimensions(nx, ny, 1)

points = vtkPoints()
vectors = vtkFloatArray()
vectors.SetName("Velocity")
vectors.SetNumberOfComponents(3)

for j in range(ny):
    for i in range(nx):
        x = i / (nx - 1.0) * 4.0 - 2.0
        y = j / (ny - 1.0) * 4.0 - 2.0
        points.InsertNextPoint(x, y, 0)
        vx = -y * math.exp(-(x * x + y * y) / 2.0)
        vy = x * math.exp(-(x * x + y * y) / 2.0)
        vectors.InsertNextTuple3(vx, vy, 0)

grid.SetPoints(points)
grid.GetPointData().SetVectors(vectors)

# Filter: compute cell derivatives (vorticity)
derivatives = vtkCellDerivatives()
derivatives.SetInputData(grid)
derivatives.SetVectorModeToComputeVorticity()

# Filter: extract surface geometry
surface = vtkStructuredGridGeometryFilter()
surface.SetInputConnection(derivatives.GetOutputPort())

# Mapper: map the surface to graphics primitives with vorticity coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("Vorticity")
mapper.SetScalarRange(0, 1)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CellDerivatives")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
