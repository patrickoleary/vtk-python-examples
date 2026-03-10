#!/usr/bin/env python

# Demonstrate vtkKMeansStatistics to cluster a 2D point cloud into three
# groups and display each cluster in a different color.

import random

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkTable
from vtkmodules.vtkFiltersStatistics import vtkKMeansStatistics
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cluster_colors = [
    (230, 76, 76),    # red
    (76, 153, 230),   # blue
    (76, 204, 76),    # green
]
slate_gray_rgb = (0.439, 0.502, 0.565)

# Generate 3 clusters of 2D points
random.seed(42)
n_per_cluster = 100
centers = [(-2, -2), (2, 2), (-2, 2)]

x_arr = vtkFloatArray()
x_arr.SetName("X")
y_arr = vtkFloatArray()
y_arr.SetName("Y")

all_points = []
for cx, cy in centers:
    for _ in range(n_per_cluster):
        x = random.gauss(cx, 0.5)
        y = random.gauss(cy, 0.5)
        x_arr.InsertNextValue(x)
        y_arr.InsertNextValue(y)
        all_points.append((x, y))

# K-Means clustering
table = vtkTable()
table.AddColumn(x_arr)
table.AddColumn(y_arr)

kmeans = vtkKMeansStatistics()
kmeans.SetInputData(0, table)
kmeans.SetColumnStatus("X", 1)
kmeans.SetColumnStatus("Y", 1)
kmeans.RequestSelectedColumns()
kmeans.SetDefaultNumberOfClusters(3)
kmeans.SetLearnOption(True)
kmeans.SetDeriveOption(True)
kmeans.SetAssessOption(True)
kmeans.Update()

# Extract cluster assignments
output_table = kmeans.GetOutput()
n_total = len(all_points)

# Build colored point cloud
points = vtkPoints()
colors_array = vtkUnsignedCharArray()
colors_array.SetName("ClusterColor")
colors_array.SetNumberOfComponents(3)

for i in range(n_total):
    x, y = all_points[i]
    points.InsertNextPoint(x, y, 0)
    cluster_id = int(output_table.GetColumn(output_table.GetNumberOfColumns() - 1).GetValue(i))
    r, g, b = cluster_colors[cluster_id % 3]
    colors_array.InsertNextTuple3(r, g, b)

polydata = vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().SetScalars(colors_array)

# Source: small sphere glyph
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.08)
glyph_source.SetPhiResolution(8)
glyph_source.SetThetaResolution(8)

# Mapper: place glyphs at each point, colored by cluster
mapper = vtkGlyph3DMapper()
mapper.SetInputData(polydata)
mapper.SetSourceConnection(glyph_source.GetOutputPort())
mapper.ScalingOff()
mapper.SetColorModeToDirectScalars()

# Actor: assign the glyph geometry
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
render_window.SetWindowName("KMeansStatistics")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
