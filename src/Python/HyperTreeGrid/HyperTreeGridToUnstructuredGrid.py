#!/usr/bin/env python

# Convert a hyper tree grid to an unstructured grid using
# vtkHyperTreeGridToUnstructuredGrid and render both side by side.
# The left viewport shows the original HTG surface colored by Depth;
# the right shows the converted unstructured grid with shrunk cells.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridGeometry,
    vtkHyperTreeGridToUnstructuredGrid,
)
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
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

# ---- Left viewport: original HTG surface ----
htg_geometry = vtkHyperTreeGridGeometry()
htg_geometry.SetInputConnection(source.GetOutputPort())

htg_mapper = vtkPolyDataMapper()
htg_mapper.SetInputConnection(htg_geometry.GetOutputPort())
htg_mapper.SetScalarModeToUseCellFieldData()
htg_mapper.SelectColorArray("Depth")
htg_mapper.SetScalarRange(0.0, 4.0)

htg_actor = vtkActor()
htg_actor.SetMapper(htg_mapper)
htg_actor.GetProperty().EdgeVisibilityOn()
htg_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(htg_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()
left_renderer.GetActiveCamera().Azimuth(150)
left_renderer.GetActiveCamera().Elevation(30)
left_renderer.ResetCameraClippingRange()

# ---- Right viewport: converted unstructured grid with shrunk cells ----
to_ug = vtkHyperTreeGridToUnstructuredGrid()
to_ug.SetInputConnection(source.GetOutputPort())

shrink = vtkShrinkFilter()
shrink.SetInputConnection(to_ug.GetOutputPort())
shrink.SetShrinkFactor(0.8)

ug_mapper = vtkDataSetMapper()
ug_mapper.SetInputConnection(shrink.GetOutputPort())
ug_mapper.SetScalarModeToUseCellFieldData()
ug_mapper.SelectColorArray("Depth")
ug_mapper.SetScalarRange(0.0, 4.0)

ug_actor = vtkActor()
ug_actor.SetMapper(ug_mapper)
ug_actor.GetProperty().EdgeVisibilityOn()
ug_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(ug_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(1024, 480)
render_window.SetWindowName("HyperTreeGridToUnstructuredGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
