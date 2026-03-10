#!/usr/bin/env python

# Extract feature edges from a hyper tree grid using
# vtkHyperTreeGridFeatureEdges.  The edges highlight boundaries between
# cells of different refinement levels, rendered over a translucent
# HTG surface for context.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridFeatureEdges,
    vtkHyperTreeGridGeometry,
)
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_gray_rgb = (0.800, 0.800, 0.800)
crimson_rgb = (0.863, 0.078, 0.235)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a 3D hyper tree grid from a text descriptor
descriptor = (
    "RRR .R. .RR ..R ..R .R.|"
    "R.......................... "
    "........................... ........................... "
    ".............R............. ....RR.RR........R......... "
    ".....RRRR.....R.RR......... ........................... "
    "........................... "
    "...........................|"
    "........................... "
    "........................... ........................... "
    "...RR.RR.......RR.......... ........................... "
    "RR......................... ........................... "
    "........................... ........................... "
    "........................... ........................... "
    "........................... ........................... "
    "............RRR............|"
    "........................... "
    "........................... .......RR.................. "
    "........................... ........................... "
    "........................... ........................... "
    "........................... ........................... "
    "........................... "
    "...........................|"
    "........................... "
    "..........................."
)

source = vtkHyperTreeGridSource()
source.SetMaxDepth(6)
source.SetDimensions(4, 4, 3)
source.SetGridScale(1.5, 1.0, 0.7)
source.SetBranchFactor(4)
source.SetDescriptor(descriptor)
source.Update()
source.GetOutput().GetCellData().SetActiveScalars("Depth")

# Filter: extract feature edges from the HTG
feature_edges = vtkHyperTreeGridFeatureEdges()
feature_edges.SetInputConnection(source.GetOutputPort())

# Mapper: map the feature edges
edges_mapper = vtkPolyDataMapper()
edges_mapper.SetInputConnection(feature_edges.GetOutputPort())
edges_mapper.ScalarVisibilityOff()

# Actor: assign the feature edges with crimson color
edges_actor = vtkActor()
edges_actor.SetMapper(edges_mapper)
edges_actor.GetProperty().SetColor(crimson_rgb)
edges_actor.GetProperty().SetLineWidth(3)

# Context: render the full HTG surface as a translucent wireframe
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(source.GetOutputPort())

context_mapper = vtkPolyDataMapper()
context_mapper.SetInputConnection(geometry.GetOutputPort())
context_mapper.ScalarVisibilityOff()

context_actor = vtkActor()
context_actor.SetMapper(context_mapper)
context_actor.GetProperty().SetColor(light_gray_rgb)
context_actor.GetProperty().SetOpacity(0.25)
context_actor.GetProperty().EdgeVisibilityOn()
context_actor.GetProperty().SetEdgeColor(0.9, 0.9, 0.9)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(edges_actor)
renderer.AddActor(context_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(150)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HyperTreeGridFeatureEdges")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
