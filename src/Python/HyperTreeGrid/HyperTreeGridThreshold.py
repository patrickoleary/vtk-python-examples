#!/usr/bin/env python

# Threshold cells of a hyper tree grid by their depth level using
# vtkHyperTreeGridThreshold and render the result alongside a
# translucent wireframe of the full HTG for context.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridGeometry,
    vtkHyperTreeGridThreshold,
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

# Filter: keep only cells at depth level 2 (the middle refinement level)
threshold = vtkHyperTreeGridThreshold()
threshold.SetInputConnection(source.GetOutputPort())
threshold.SetLowerThreshold(2.0)
threshold.SetUpperThreshold(2.0)

# Geometry: extract surface of the thresholded HTG
geometry_thresh = vtkHyperTreeGridGeometry()
geometry_thresh.SetInputConnection(threshold.GetOutputPort())

thresh_mapper = vtkPolyDataMapper()
thresh_mapper.SetInputConnection(geometry_thresh.GetOutputPort())
thresh_mapper.SetScalarModeToUseCellFieldData()
thresh_mapper.SelectColorArray("Depth")
thresh_mapper.SetScalarRange(0.0, 4.0)

thresh_actor = vtkActor()
thresh_actor.SetMapper(thresh_mapper)
thresh_actor.GetProperty().EdgeVisibilityOn()
thresh_actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Context: translucent wireframe of the full HTG
geometry_full = vtkHyperTreeGridGeometry()
geometry_full.SetInputConnection(source.GetOutputPort())

context_mapper = vtkPolyDataMapper()
context_mapper.SetInputConnection(geometry_full.GetOutputPort())
context_mapper.ScalarVisibilityOff()

context_actor = vtkActor()
context_actor.SetMapper(context_mapper)
context_actor.GetProperty().SetColor(light_gray_rgb)
context_actor.GetProperty().SetOpacity(0.15)
context_actor.GetProperty().EdgeVisibilityOn()
context_actor.GetProperty().SetEdgeColor(0.6, 0.6, 0.6)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(thresh_actor)
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
render_window.SetWindowName("HyperTreeGridThreshold")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
