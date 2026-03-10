#!/usr/bin/env python

# Compare Loop and Butterfly subdivision filters on a random-height mesh grid.

import numpy as np

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkTriangle,
)
from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkFiltersModeling import (
    vtkButterflySubdivisionFilter,
    vtkLoopSubdivisionFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
alice_blue_rgb = (0.941, 0.973, 1.000)

# Source: 32x32 random-height topography
size = 32
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(1)

topography = np.zeros([size, size])
for i in range(size):
    for j in range(size):
        topography[i][j] = rng.GetRangeValue(0, 5)
        rng.Next()

# Build triangle mesh and per-vertex colors
point_colors = vtkUnsignedCharArray()
point_colors.SetNumberOfComponents(3)
points = vtkPoints()
triangles = vtkCellArray()

count = 0
for i in range(size - 1):
    for j in range(size - 1):
        z1 = topography[i][j]
        z2 = topography[i][j + 1]
        z3 = topography[i + 1][j]

        points.InsertNextPoint(i, j, z1)
        points.InsertNextPoint(i, j + 1, z2)
        points.InsertNextPoint(i + 1, j, z3)

        tri1 = vtkTriangle()
        tri1.GetPointIds().SetId(0, count)
        tri1.GetPointIds().SetId(1, count + 1)
        tri1.GetPointIds().SetId(2, count + 2)
        triangles.InsertNextCell(tri1)

        z4 = topography[i][j + 1]
        z5 = topography[i + 1][j + 1]
        z6 = topography[i + 1][j]

        points.InsertNextPoint(i, j + 1, z4)
        points.InsertNextPoint(i + 1, j + 1, z5)
        points.InsertNextPoint(i + 1, j, z6)

        tri2 = vtkTriangle()
        tri2.GetPointIds().SetId(0, count + 3)
        tri2.GetPointIds().SetId(1, count + 4)
        tri2.GetPointIds().SetId(2, count + 5)
        triangles.InsertNextCell(tri2)

        count += 6

        r = [int(i / float(size) * 255), int(j / float(size) * 255), 0]
        point_colors.InsertNextTypedTuple(r)
        point_colors.InsertNextTypedTuple(r)
        point_colors.InsertNextTypedTuple(r)
        point_colors.InsertNextTypedTuple(r)
        point_colors.InsertNextTypedTuple(r)
        point_colors.InsertNextTypedTuple(r)

triangle_polydata = vtkPolyData()
triangle_polydata.SetPoints(points)
triangle_polydata.GetPointData().SetScalars(point_colors)
triangle_polydata.SetPolys(triangles)

# Filter: merge coincident points so subdivision works
clean = vtkCleanPolyData()
clean.SetInputData(triangle_polydata)

# Filter: Loop subdivision
loop_filter = vtkLoopSubdivisionFilter()
loop_filter.SetNumberOfSubdivisions(3)
loop_filter.SetInputConnection(clean.GetOutputPort())

# Filter: Butterfly subdivision
butterfly_filter = vtkButterflySubdivisionFilter()
butterfly_filter.SetNumberOfSubdivisions(3)
butterfly_filter.SetInputConnection(clean.GetOutputPort())

# Mapper & Actor: map original mesh to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputData(triangle_polydata)

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)

# Mapper & Actor: map Loop-subdivided mesh to graphics primitives
loop_mapper = vtkPolyDataMapper()
loop_mapper.SetInputConnection(loop_filter.GetOutputPort())

loop_actor = vtkActor()
loop_actor.SetMapper(loop_mapper)
loop_actor.SetPosition(32, 0, 0)

# Mapper & Actor: map Butterfly-subdivided mesh to graphics primitives
butterfly_mapper = vtkPolyDataMapper()
butterfly_mapper.SetInputConnection(butterfly_filter.GetOutputPort())

butterfly_actor = vtkActor()
butterfly_actor.SetMapper(butterfly_mapper)
butterfly_actor.SetPosition(64, 0, 0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(loop_actor)
renderer.AddActor(butterfly_actor)
renderer.SetBackground(alice_blue_rgb)
renderer.GetActiveCamera().Elevation(-45)
renderer.GetActiveCamera().Zoom(3)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(900, 300)
render_window.SetWindowName("SmoothMeshGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
