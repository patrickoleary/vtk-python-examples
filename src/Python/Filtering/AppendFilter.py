#!/usr/bin/env python

# Combine a vtkPolyData point cloud and a vtkUnstructuredGrid using
# vtkAppendFilter and visualize the merged result with sphere glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkAppendFilter
from vtkmodules.vtkFiltersSources import (
    vtkPointSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
royal_blue_rgb = (0.255, 0.412, 0.882)

# Source 1: generate 5 random points as vtkPolyData
point_source = vtkPointSource()
point_source.SetNumberOfPoints(5)
point_source.Update()
polydata = point_source.GetOutput()

# Source 2: create 2 explicit points in a vtkUnstructuredGrid
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(0, 0, 1)
ug = vtkUnstructuredGrid()
ug.SetPoints(points)

# Filter: combine the two data sets into a single unstructured grid
append_filter = vtkAppendFilter()
append_filter.AddInputData(polydata)
append_filter.AddInputData(ug)
append_filter.Update()

# Mapper: map the combined data set to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(append_filter.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(5)

# Glyph: represent each combined point as a sphere
combined_points = append_filter.GetOutput().GetPoints()
bounds = combined_points.GetBounds()
max_len = max(bounds[i + 1] - bounds[i] for i in range(3))

sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.05 * max_len)

glyph_polydata = vtkPolyData()
glyph_polydata.SetPoints(combined_points)

glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputData(glyph_polydata)
glyph_mapper.SetSourceConnection(sphere_source.GetOutputPort())
glyph_mapper.ScalarVisibilityOff()
glyph_mapper.ScalingOff()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(royal_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("AppendFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
