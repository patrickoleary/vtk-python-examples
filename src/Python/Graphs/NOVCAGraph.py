#!/usr/bin/env python

# Build a graph as a vtkUnstructuredGrid with vertex degree scalars, then
# render it. Vertices are colored by degree and edges are drawn as lines.

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
    VTK_LINE,
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGBA for LUT, RGB for scene)
light_blue_rgba = (0.678, 0.847, 0.902, 1.0)
cornflower_blue_rgba = (0.392, 0.584, 0.929, 1.0)
gold_rgba = (1.0, 0.843, 0.0, 1.0)
orange_rgba = (1.0, 0.647, 0.0, 1.0)
tomato_rgba = (0.980, 0.502, 0.447, 1.0)
gray_rgb = (0.502, 0.502, 0.502)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Vertex degree array: number of edges incident on each vertex
degree = vtkIntArray()
degree.SetNumberOfComponents(1)
degree.SetName("Degree")
degree.SetNumberOfTuples(7)
degree.SetValue(0, 2)
degree.SetValue(1, 1)
degree.SetValue(2, 3)
degree.SetValue(3, 3)
degree.SetValue(4, 4)
degree.SetValue(5, 2)
degree.SetValue(6, 1)

# Points: vertex coordinates on a grid
points = vtkPoints()
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(2, 1, 0)
points.InsertNextPoint(2, 0, 0)
points.InsertNextPoint(3, 0, 0)

# Edges: eight line cells connecting the vertices
lines = vtkCellArray()
edges = [
    (0, 1), (0, 2), (2, 3), (2, 4),
    (3, 4), (3, 5), (4, 5), (4, 6),
]
for a, b in edges:
    lines.InsertNextCell(2)
    lines.InsertCellPoint(a)
    lines.InsertCellPoint(b)

# UnstructuredGrid: assemble the graph
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.SetCells(VTK_LINE, lines)
grid.GetPointData().SetScalars(degree)

# LookupTable: color vertices by degree (1=cold, 4=hot)
lut = vtkLookupTable()
lut.SetNumberOfTableValues(5)
lut.SetTableRange(0, 4)
lut.SetTableValue(0, light_blue_rgba)
lut.SetTableValue(1, cornflower_blue_rgba)
lut.SetTableValue(2, gold_rgba)
lut.SetTableValue(3, orange_rgba)
lut.SetTableValue(4, tomato_rgba)
lut.Build()

# Edge mapper and actor: draw the line cells
edge_mapper = vtkDataSetMapper()
edge_mapper.SetInputData(grid)
edge_mapper.ScalarVisibilityOff()

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(gray_rgb)
edge_actor.GetProperty().SetLineWidth(2.0)

# Glyph mapper and actor: draw spheres at vertices colored by degree
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.12)
glyph_source.SetPhiResolution(16)
glyph_source.SetThetaResolution(16)

glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputData(grid)
glyph_mapper.SetSourceConnection(glyph_source.GetOutputPort())
glyph_mapper.SetScalarModeToUsePointData()
glyph_mapper.SetColorModeToMapScalars()
glyph_mapper.SetLookupTable(lut)
glyph_mapper.SetScalarRange(0, 4)
glyph_mapper.ScalingOff()

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("NOVCAGraph")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
