#!/usr/bin/env python

# Visualize a procedural vector field as a hedgehog plot on a structured grid.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
white = (1.0, 1.0, 1.0)

# Source: build a 15x15x15 structured grid with a swirling vector field
nx, ny, nz = 15, 15, 15

points = vtkPoints()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetName("Vectors")

for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            x = i / (nx - 1.0) * 2.0 - 1.0
            y = j / (ny - 1.0) * 2.0 - 1.0
            z = k / (nz - 1.0) * 2.0 - 1.0
            points.InsertNextPoint(x, y, z)
            r = math.sqrt(x * x + y * y + z * z) + 1e-10
            vx = -y / r
            vy = x / r
            vz = 0.5 * math.sin(math.pi * z)
            vectors.InsertNextTuple3(vx, vy, vz)

sg = vtkStructuredGrid()
sg.SetDimensions(nx, ny, nz)
sg.SetPoints(points)
sg.GetPointData().SetVectors(vectors)

# Filter: hedgehog glyph — draws a line segment at each point along the vector
hedgehog = vtkHedgeHog()
hedgehog.SetInputData(sg)
hedgehog.SetScaleFactor(0.1)

hedgehog_mapper = vtkPolyDataMapper()
hedgehog_mapper.SetInputConnection(hedgehog.GetOutputPort())

hedgehog_actor = vtkActor()
hedgehog_actor.SetMapper(hedgehog_mapper)

# Filter: outline around the grid
outline = vtkOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(white)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(hedgehog_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Hedgehog")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
