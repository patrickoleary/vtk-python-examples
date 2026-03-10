#!/usr/bin/env python

# Display the bounding box outline of a hyper tree grid alongside its
# surface using vtkOutlineFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridGeometry
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_rgb = (1.000, 1.000, 1.000)
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

# Filter: extract the external surface of the HTG
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(source.GetOutputPort())

# Mapper and actor: surface colored by Depth
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(geometry.GetOutputPort())
surface_mapper.SetScalarModeToUseCellFieldData()
surface_mapper.SelectColorArray("Depth")
surface_mapper.SetScalarRange(0.0, 4.0)

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetOpacity(0.5)
surface_actor.GetProperty().EdgeVisibilityOn()
surface_actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Filter: compute the bounding box outline of the geometry
outline = vtkOutlineFilter()
outline.SetInputConnection(geometry.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(white_rgb)
outline_actor.GetProperty().SetLineWidth(3)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(150)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HyperTreeGridOutlineFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
