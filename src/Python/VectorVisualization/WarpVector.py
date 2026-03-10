#!/usr/bin/env python

# Warp a flat structured grid by a procedural vector field to show displacement.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue = (0.392, 0.584, 0.929)
white = (1.0, 1.0, 1.0)

# Source: build a 30x30x1 flat grid with a radial displacement vector field
nx, ny, nz = 30, 30, 1

points = vtkPoints()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetName("Displacement")

scalars = vtkFloatArray()
scalars.SetNumberOfComponents(1)
scalars.SetName("Height")

for j in range(ny):
    for i in range(nx):
        x = i / (nx - 1.0) * 4.0 - 2.0
        y = j / (ny - 1.0) * 4.0 - 2.0
        z = 0.0
        points.InsertNextPoint(x, y, z)
        r = math.sqrt(x * x + y * y) + 1e-10
        height = math.exp(-r * r) * math.cos(2.0 * math.pi * r / 2.0)
        vectors.InsertNextTuple3(0.0, 0.0, height)
        scalars.InsertNextValue(height)

sg = vtkStructuredGrid()
sg.SetDimensions(nx, ny, nz)
sg.SetPoints(points)
sg.GetPointData().SetVectors(vectors)
sg.GetPointData().SetScalars(scalars)

# Filter: extract the surface of the structured grid
surface = vtkStructuredGridGeometryFilter()
surface.SetInputData(sg)

# Filter: warp the flat surface by the displacement vector
warp = vtkWarpVector()
warp.SetInputConnection(surface.GetOutputPort())
warp.SetScaleFactor(1.0)

# Filter: recompute normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())
normals.SetFeatureAngle(60)

warp_mapper = vtkPolyDataMapper()
warp_mapper.SetInputConnection(normals.GetOutputPort())
warp_mapper.SetScalarRange(sg.GetScalarRange())

warp_actor = vtkActor()
warp_actor.SetMapper(warp_mapper)

# Filter: outline around the original grid
outline = vtkOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(white)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(warp_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(cornflower_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("WarpVector")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
