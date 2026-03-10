#!/usr/bin/env python

# Cut a hyper tree grid with an axis-aligned plane using
# vtkHyperTreeGridAxisCut.  The cut produces a 2D slice through the
# HTG, rendered colored by depth with the full HTG wireframe for context.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridAxisCut,
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

# Filter: cut the HTG with a plane normal to Y at position 1.5
cut = vtkHyperTreeGridAxisCut()
cut.SetInputConnection(source.GetOutputPort())
cut.SetPlaneNormalAxis(1)  # 1 = Y axis
cut.SetPlanePosition(1.5)

# Geometry: extract cut slice surface for rendering
cut_geometry = vtkHyperTreeGridGeometry()
cut_geometry.SetInputConnection(cut.GetOutputPort())

# Mapper: map the slice colored by Depth
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cut_geometry.GetOutputPort())
cut_mapper.SetScalarModeToUseCellFieldData()
cut_mapper.SelectColorArray("Depth")
cut_mapper.SetScalarRange(0.0, 4.0)

# Actor: assign the cut geometry
cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Context: render the full HTG surface as a translucent wireframe
full_geometry = vtkHyperTreeGridGeometry()
full_geometry.SetInputConnection(source.GetOutputPort())

context_mapper = vtkPolyDataMapper()
context_mapper.SetInputConnection(full_geometry.GetOutputPort())
context_mapper.ScalarVisibilityOff()

context_actor = vtkActor()
context_actor.SetMapper(context_mapper)
context_actor.GetProperty().SetColor(light_gray_rgb)
context_actor.GetProperty().SetOpacity(0.15)
context_actor.GetProperty().EdgeVisibilityOn()
context_actor.GetProperty().SetEdgeColor(0.6, 0.6, 0.6)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cut_actor)
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
render_window.SetWindowName("HyperTreeGridAxisCut")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
