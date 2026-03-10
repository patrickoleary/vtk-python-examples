#!/usr/bin/env python

# Demonstrate vtkPCAStatistics to compute principal component axes of a 3D
# point cloud and display the axes as arrows overlaid on the data.

import random

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkTable
from vtkmodules.vtkFiltersStatistics import vtkPCAStatistics
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
tomato_rgb = (0.980, 0.502, 0.447)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Generate an elongated 3D Gaussian point cloud
random.seed(42)
n = 300
x_arr = vtkFloatArray()
x_arr.SetName("X")
y_arr = vtkFloatArray()
y_arr.SetName("Y")
z_arr = vtkFloatArray()
z_arr.SetName("Z")

points = vtkPoints()
for i in range(n):
    x = random.gauss(0, 2.0)
    y = random.gauss(0, 0.5) + 0.5 * x
    z = random.gauss(0, 0.3)
    x_arr.InsertNextValue(x)
    y_arr.InsertNextValue(y)
    z_arr.InsertNextValue(z)
    points.InsertNextPoint(x, y, z)

# PCA: compute principal components
table = vtkTable()
table.AddColumn(x_arr)
table.AddColumn(y_arr)
table.AddColumn(z_arr)

pca = vtkPCAStatistics()
pca.SetInputData(0, table)
pca.SetColumnStatus("X", 1)
pca.SetColumnStatus("Y", 1)
pca.SetColumnStatus("Z", 1)
pca.RequestSelectedColumns()
pca.SetLearnOption(True)
pca.SetDeriveOption(True)
pca.SetAssessOption(False)
pca.Update()

# Point cloud visualization
polydata = vtkPolyData()
polydata.SetPoints(points)

glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.06)
glyph_source.SetPhiResolution(8)
glyph_source.SetThetaResolution(8)

mapper = vtkGlyph3DMapper()
mapper.SetInputData(polydata)
mapper.SetSourceConnection(glyph_source.GetOutputPort())
mapper.ScalingOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornflower_blue_rgb)
actor.GetProperty().SetOpacity(0.6)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PCAStatistics")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
