#!/usr/bin/env python

# Create a random topography mesh, smooth it with loop subdivision,
# trace a spline line on the surface using vtkCellLocator intersections.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
import numpy as np
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSpline
from vtkmodules.vtkCommonCore import (
    mutable,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkCellLocator,
    vtkPolyData,
    vtkTriangle,
)
from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkFiltersModeling import vtkLoopSubdivisionFilter
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
cornsilk_rgb = (1.0, 0.973, 0.863)

# Topography: generate a 32 x 32 random height field
size = 32
np.random.seed(3)
topography = np.random.randint(0, 5, (size, size))

# Mesh: build triangulated surface from the height field with per-vertex color
vertex_colors = vtkUnsignedCharArray()
vertex_colors.SetNumberOfComponents(3)
points = vtkPoints()
triangles = vtkCellArray()

count = 0
for i in range(size - 1):
    for j in range(size - 1):
        z1 = topography[i][j]
        z2 = topography[i][j + 1]
        z3 = topography[i + 1][j]

        points.InsertNextPoint(i, j, z1)
        points.InsertNextPoint(i, (j + 1), z2)
        points.InsertNextPoint((i + 1), j, z3)

        triangle = vtkTriangle()
        triangle.GetPointIds().SetId(0, count)
        triangle.GetPointIds().SetId(1, count + 1)
        triangle.GetPointIds().SetId(2, count + 2)
        triangles.InsertNextCell(triangle)

        z1 = topography[i][j + 1]
        z2 = topography[i + 1][j + 1]
        z3 = topography[i + 1][j]

        points.InsertNextPoint(i, (j + 1), z1)
        points.InsertNextPoint((i + 1), (j + 1), z2)
        points.InsertNextPoint((i + 1), j, z3)

        triangle = vtkTriangle()
        triangle.GetPointIds().SetId(0, count + 3)
        triangle.GetPointIds().SetId(1, count + 4)
        triangle.GetPointIds().SetId(2, count + 5)
        triangles.InsertNextCell(triangle)

        count += 6

        r = [int(i / float(size) * 255), int(j / float(size) * 255), 0]
        for _ in range(6):
            vertex_colors.InsertNextTypedTuple(r)

# PolyData: assemble the triangulated mesh
triangle_polydata = vtkPolyData()
triangle_polydata.SetPoints(points)
triangle_polydata.GetPointData().SetScalars(vertex_colors)
triangle_polydata.SetPolys(triangles)

# Filter: clean the polydata so that edges are shared
clean = vtkCleanPolyData()
clean.SetInputData(triangle_polydata)

# Filter: smooth the mesh with loop subdivision
smooth = vtkLoopSubdivisionFilter()
smooth.SetNumberOfSubdivisions(3)
smooth.SetInputConnection(clean.GetOutputPort())
smooth.Update()

# Mapper: map the smoothed mesh to graphics primitives
terrain_mapper = vtkPolyDataMapper()
terrain_mapper.SetInputConnection(smooth.GetOutputPort())

# Actor: assign the terrain mesh
terrain_actor = vtkActor()
terrain_actor.SetMapper(terrain_mapper)
terrain_actor.GetProperty().SetInterpolationToFlat()

# Cell locator: find intersections between vertical lines and the surface
locator = vtkCellLocator()
locator.SetDataSet(smooth.GetOutput())
locator.BuildLocator()

maxloop = 1000
dist = 20.0 / maxloop
tolerance = 0.001

# Intersection: cast vertical lines and collect surface intersection points
intersection_points = vtkPoints()
for i in range(maxloop):
    p1 = [2 + i * dist, 16, -1]
    p2 = [2 + i * dist, 16, 6]

    t = mutable(0)
    pos = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = mutable(0)
    locator.IntersectWithLine(p1, p2, tolerance, t, pos, pcoords, sub_id)

    pos[2] += 0.01
    intersection_points.InsertNextPoint(pos)

# Spline: fit a parametric spline through the intersection points
spline = vtkParametricSpline()
spline.SetPoints(intersection_points)
spline_source = vtkParametricFunctionSource()
spline_source.SetUResolution(maxloop)
spline_source.SetParametricFunction(spline)

# Mapper: map the spline to graphics primitives
spline_mapper = vtkPolyDataMapper()
spline_mapper.SetInputConnection(spline_source.GetOutputPort())

# Actor: assign the spline line
spline_actor = vtkActor()
spline_actor.SetMapper(spline_mapper)
spline_actor.GetProperty().SetColor(red_rgb)
spline_actor.GetProperty().SetLineWidth(3)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(terrain_actor)
renderer.AddActor(spline_actor)
renderer.SetBackground(cornsilk_rgb)
renderer.GetActiveCamera().SetPosition(-32.471276, 53.258788, 61.209332)
renderer.GetActiveCamera().SetFocalPoint(15.500000, 15.500000, 2.000000)
renderer.GetActiveCamera().SetViewUp(0.348057, -0.636740, 0.688055)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("LineOnMesh")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
