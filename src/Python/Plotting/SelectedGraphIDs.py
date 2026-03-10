#!/usr/bin/env python

# Graph layout visualization of a random tree using the explicit VTK pipeline.
# Vertices are colored by ID and edges by weight using a force-directed layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkGraphToPolyData,
    vtkSphereSource,
)
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: generate a random tree with 100 vertices
source = vtkRandomGraphSource()
source.DirectedOff()
source.SetNumberOfVertices(100)
source.SetEdgeProbability(0)
source.SetUseEdgeProbability(True)
source.SetStartWithTree(True)
source.IncludeEdgeWeightsOn()

# Layout: force-directed 2D layout strategy
strategy = vtkSimple2DLayoutStrategy()
strategy.SetInitialTemperature(5)

layout = vtkGraphLayout()
layout.SetInputConnection(source.GetOutputPort())
layout.SetLayoutStrategy(strategy)

# Convert graph to polydata for rendering
graph_to_poly = vtkGraphToPolyData()
graph_to_poly.SetInputConnection(layout.GetOutputPort())
graph_to_poly.Update()

# Edge actor: render graph edges as lines colored by edge weight
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_poly.GetOutputPort())
edge_mapper.SetScalarModeToUseCellFieldData()
edge_mapper.SelectColorArray("edge weight")
edge_mapper.ScalarVisibilityOn()

edge_lut = vtkLookupTable()
edge_lut.SetHueRange(0.1, 0.1)
edge_lut.SetSaturationRange(0.2, 1.0)
edge_lut.SetValueRange(0.5, 1.0)
edge_lut.Build()
edge_mapper.SetLookupTable(edge_lut)
edge_range = graph_to_poly.GetOutput().GetCellData().GetArray("edge weight")
if edge_range:
    edge_mapper.SetScalarRange(edge_range.GetRange())

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetLineWidth(2)

# Vertex actor: render graph vertices as spheres colored by vertex ID
vertex_source = vtkSphereSource()
vertex_source.SetRadius(0.15)
vertex_source.SetPhiResolution(8)
vertex_source.SetThetaResolution(8)

glyph = vtkGlyph3D()
glyph.SetInputConnection(graph_to_poly.GetOutputPort())
glyph.SetSourceConnection(vertex_source.GetOutputPort())
glyph.SetScaleModeToDataScalingOff()

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(glyph.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("vertex id")
vertex_mapper.ScalarVisibilityOn()

vertex_lut = vtkLookupTable()
vertex_lut.SetHueRange(0.0, 0.67)
vertex_lut.SetSaturationRange(0.8, 0.8)
vertex_lut.SetValueRange(0.8, 0.8)
vertex_lut.SetNumberOfColors(100)
vertex_lut.Build()
vertex_mapper.SetLookupTable(vertex_lut)
vertex_mapper.SetScalarRange(0, 99)

vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.SetBackground(slate_gray_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 640)
render_window.SetWindowName("SelectedGraphIDs")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
