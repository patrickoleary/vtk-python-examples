#!/usr/bin/env python

# Mirror a hyper tree grid across an axis using
# vtkHyperTreeGridAxisReflection and render the original and reflected
# copies together.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridAxisReflection,
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

# Filter: reflect the HTG across the X axis (plane at X minimum)
reflection = vtkHyperTreeGridAxisReflection()
reflection.SetInputConnection(source.GetOutputPort())
reflection.SetPlaneToXMin()

# Geometry: extract surfaces for both original and reflected HTG
geometry_original = vtkHyperTreeGridGeometry()
geometry_original.SetInputConnection(source.GetOutputPort())

geometry_reflected = vtkHyperTreeGridGeometry()
geometry_reflected.SetInputConnection(reflection.GetOutputPort())

# Mapper: map both surfaces to graphics primitives, colored by Depth
mapper_original = vtkPolyDataMapper()
mapper_original.SetInputConnection(geometry_original.GetOutputPort())
mapper_original.SetScalarModeToUseCellFieldData()
mapper_original.SelectColorArray("Depth")
mapper_original.SetScalarRange(0.0, 4.0)

mapper_reflected = vtkPolyDataMapper()
mapper_reflected.SetInputConnection(geometry_reflected.GetOutputPort())
mapper_reflected.SetScalarModeToUseCellFieldData()
mapper_reflected.SelectColorArray("Depth")
mapper_reflected.SetScalarRange(0.0, 4.0)

# Actor: original and reflected both colored by depth
actor_original = vtkActor()
actor_original.SetMapper(mapper_original)
actor_original.GetProperty().EdgeVisibilityOn()
actor_original.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

actor_reflected = vtkActor()
actor_reflected.SetMapper(mapper_reflected)
actor_reflected.GetProperty().EdgeVisibilityOn()
actor_reflected.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor_original)
renderer.AddActor(actor_reflected)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(150)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HyperTreeGridAxisReflection")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
