#!/usr/bin/env python

# Koch snowflake fractal: outline (left) and triangulated fill (right).

from math import cos, pi, sin, sqrt

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
    vtkTriangle,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
misty_rose_rgb = (1.0, 0.894, 0.882)

# Recursion depth for the Koch curve
LEVEL = 6

# Seed points: equilateral triangle (closed — first == last)
points = vtkPoints()
for i in range(4):
    points.InsertNextPoint(cos(2.0 * pi * i / 3), sin(2.0 * pi * i / 3), 0.0)

# Build the Koch curve by recursive edge subdivision
for _iteration in range(LEVEL):
    temp = vtkPoints()
    temp.InsertNextPoint(*points.GetPoint(0))
    for j in range(1, points.GetNumberOfPoints()):
        x0, y0, z0 = points.GetPoint(j - 1)
        x1, y1, z1 = points.GetPoint(j)
        t = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        nx = (x1 - x0) / t
        ny = (y1 - y0) / t
        temp.InsertNextPoint(x0 + nx * t / 3, y0 + ny * t / 3, 0.0)
        temp.InsertNextPoint(
            x0 + nx * t / 2 + ny * t * sqrt(3) / 6,
            y0 + ny * t / 2 - nx * t * sqrt(3) / 6,
            0.0,
        )
        temp.InsertNextPoint(x0 + nx * 2 * t / 3, y0 + ny * 2 * t / 3, 0.0)
        temp.InsertNextPoint(x0 + nx * t, y0 + ny * t, 0.0)
    points = temp

# Outline: polyline from the Koch curve points
lines = vtkCellArray()
pl = vtkPolyLine()
pl.GetPointIds().SetNumberOfIds(points.GetNumberOfPoints())
for i in range(points.GetNumberOfPoints()):
    pl.GetPointIds().SetId(i, i)
lines.InsertNextCell(pl)

outline_pd = vtkPolyData()
outline_pd.SetLines(lines)
outline_pd.SetPoints(points)

# Triangulation: recursive subdivision of the Koch snowflake interior
indices = list(range(outline_pd.GetPoints().GetNumberOfPoints() + 1))
triangles = vtkCellArray()
stride = (len(indices) - 1) // 3

data = vtkIntArray()
data.SetNumberOfComponents(1)
data.SetName("Iteration Level")

# Starting triangle
t0 = vtkTriangle()
t0.GetPointIds().SetId(0, 0)
t0.GetPointIds().SetId(1, stride)
t0.GetPointIds().SetId(2, 2 * stride)
triangles.InsertNextCell(t0)
data.InsertNextValue(0)


def subdivide_triangles(idx, cellarray, level, scalar_data):
    if len(idx) >= 3:
        s = len(idx) // 4
        idx.append(idx[-1] + 1)
        tri = vtkTriangle()
        tri.GetPointIds().SetId(0, idx[s])
        tri.GetPointIds().SetId(1, idx[2 * s])
        tri.GetPointIds().SetId(2, idx[3 * s])
        cellarray.InsertNextCell(tri)
        scalar_data.InsertNextValue(level)
        subdivide_triangles(idx[0:s], cellarray, level + 1, scalar_data)
        subdivide_triangles(idx[s : 2 * s], cellarray, level + 1, scalar_data)
        subdivide_triangles(idx[2 * s : 3 * s], cellarray, level + 1, scalar_data)
        subdivide_triangles(idx[3 * s : -1], cellarray, level + 1, scalar_data)


subdivide_triangles(indices[0 : stride + 1], triangles, 1, data)
subdivide_triangles(indices[stride : 2 * stride + 1], triangles, 1, data)
subdivide_triangles(indices[2 * stride : -1], triangles, 1, data)

triangle_pd = vtkPolyData()
triangle_pd.SetPoints(outline_pd.GetPoints())
triangle_pd.SetPolys(triangles)
triangle_pd.GetCellData().SetScalars(data)

# LookupTable: blue hue, saturation varies by iteration level
lut = vtkLookupTable()
lut.SetNumberOfTableValues(256)
lut.SetHueRange(0.6, 0.6)
lut.SetSaturationRange(0.0, 1.0)
lut.Build()

# Mapper/Actor: outline (left viewport)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputData(outline_pd)

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Mapper/Actor: triangulated fill (right viewport)
triangle_mapper = vtkPolyDataMapper()
triangle_mapper.SetInputData(triangle_pd)
triangle_mapper.SetScalarRange(0.0, LEVEL)
triangle_mapper.SetLookupTable(lut)

triangle_actor = vtkActor()
triangle_actor.SetMapper(triangle_mapper)

# Renderer: outline (left)
outline_ren = vtkRenderer()
outline_ren.AddActor(outline_actor)
outline_ren.SetViewport(0.0, 0.0, 0.5, 1.0)
outline_ren.SetBackground(cornflower_blue_rgb)

# Renderer: triangles (right, shared camera)
triangle_ren = vtkRenderer()
triangle_ren.AddActor(triangle_actor)
triangle_ren.SetViewport(0.5, 0.0, 1.0, 1.0)
triangle_ren.SetBackground(misty_rose_rgb)
triangle_ren.SetActiveCamera(outline_ren.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(outline_ren)
render_window.AddRenderer(triangle_ren)
render_window.SetSize(800, 400)
render_window.SetWindowName("KochSnowflake")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

outline_ren.ResetCamera()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
