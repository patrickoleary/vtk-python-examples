#!/usr/bin/env python

# Demonstrate vtkDescriptiveStatistics to compute mean, standard deviation,
# and other statistics on random data, then display the data as a scatter
# plot with a text overlay showing the computed statistics.

import random

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkTable
from vtkmodules.vtkFiltersStatistics import vtkDescriptiveStatistics
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Generate random data
random.seed(42)
n = 200
values = vtkFloatArray()
values.SetName("Value")
values.SetNumberOfTuples(n)

points = vtkPoints()
for i in range(n):
    v = random.gauss(5.0, 1.5)
    values.SetValue(i, v)
    points.InsertNextPoint(v, random.gauss(0, 0.3), 0)

# Statistics: compute descriptive statistics
table = vtkTable()
table.AddColumn(values)

stats = vtkDescriptiveStatistics()
stats.SetInputData(0, table)
stats.AddColumn("Value")
stats.SetLearnOption(True)
stats.SetDeriveOption(True)
stats.SetAssessOption(False)
stats.Update()

# Compute stats from raw data for the text overlay
raw = [values.GetValue(i) for i in range(n)]
mean_val = sum(raw) / n
std_val = (sum((v - mean_val) ** 2 for v in raw) / n) ** 0.5
min_val = min(raw)
max_val = max(raw)

# Point cloud for visualization
polydata = vtkPolyData()
polydata.SetPoints(points)

# Source: small sphere glyph
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.05)
glyph_source.SetPhiResolution(8)
glyph_source.SetThetaResolution(8)

# Mapper: place glyphs at each data point
mapper = vtkGlyph3DMapper()
mapper.SetInputData(polydata)
mapper.SetSourceConnection(glyph_source.GetOutputPort())
mapper.ScalingOff()

# Actor: assign the glyph geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)

# Text overlay: display computed statistics
stats_text = (
    f"Mean: {mean_val:.2f}\n"
    f"Std Dev: {std_val:.2f}\n"
    f"Min: {min_val:.2f}\n"
    f"Max: {max_val:.2f}\n"
    f"N: {n}"
)
text_mapper = vtkTextMapper()
text_mapper.SetInput(stats_text)
text_mapper.GetTextProperty().SetFontSize(18)
text_mapper.GetTextProperty().SetColor(1.0, 1.0, 1.0)

text_actor = vtkActor2D()
text_actor.SetMapper(text_mapper)
text_actor.SetPosition(20, 20)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddViewProp(text_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("DescriptiveStatistics")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
