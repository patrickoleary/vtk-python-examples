#!/usr/bin/env python

# Visualize a procedural vector field using oriented and scaled arrow glyphs.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
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

# Source: build an 8x8x8 structured grid with a radial + rotational vector field
nx, ny, nz = 8, 8, 8

points = vtkPoints()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetName("Vectors")

scalars = vtkFloatArray()
scalars.SetNumberOfComponents(1)
scalars.SetName("Magnitude")

for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            x = i / (nx - 1.0) * 4.0 - 2.0
            y = j / (ny - 1.0) * 4.0 - 2.0
            z = k / (nz - 1.0) * 4.0 - 2.0
            points.InsertNextPoint(x, y, z)
            vx = -y
            vy = x
            vz = 0.5 * z
            mag = math.sqrt(vx * vx + vy * vy + vz * vz)
            vectors.InsertNextTuple3(vx, vy, vz)
            scalars.InsertNextValue(mag)

sg = vtkStructuredGrid()
sg.SetDimensions(nx, ny, nz)
sg.SetPoints(points)
sg.GetPointData().SetVectors(vectors)
sg.GetPointData().SetScalars(scalars)

# Source: arrow glyph geometry
arrow = vtkArrowSource()
arrow.SetTipResolution(16)
arrow.SetShaftResolution(16)

# Filter: orient and scale arrows by the vector field
glyph = vtkGlyph3D()
glyph.SetInputData(sg)
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetVectorModeToUseVector()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.3)
glyph.OrientOn()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())
glyph_mapper.SetScalarRange(sg.GetScalarRange())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

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
renderer.AddActor(glyph_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ArrowGlyphs")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
