#!/usr/bin/env python

# Compute and visualize the gradient of a scalar field on a hyper tree
# grid using vtkHyperTreeGridGradient.  The depth-level scalar produced
# by vtkHyperTreeGridSource is used as input; the gradient magnitude
# colors the surface.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridGeometry,
    vtkHyperTreeGridGradient,
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

# Filter: compute the gradient of the Depth scalar field
gradient = vtkHyperTreeGridGradient()
gradient.SetInputConnection(source.GetOutputPort())
gradient.SetInputArrayToProcess(0, 0, 0, 0, "Depth")

# Geometry: extract the surface with gradient data attached
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(gradient.GetOutputPort())

# Calculator: compute gradient magnitude from the Gradient vector
calculator = vtkArrayCalculator()
calculator.SetInputConnection(geometry.GetOutputPort())
calculator.SetAttributeTypeToCellData()
calculator.AddVectorVariable("g", "Gradient")
calculator.AddScalarVariable("d", "Depth", 0)
calculator.SetFunction("if(d > 1, mag(g), 0)")
calculator.SetResultArrayName("GradientMagnitude")

# Geometry for left viewport (Depth coloring, no gradient)
geometry_depth = vtkHyperTreeGridGeometry()
geometry_depth.SetInputConnection(source.GetOutputPort())

# Mapper 1: color by Depth (left viewport)
mapper_depth = vtkPolyDataMapper()
mapper_depth.SetInputConnection(geometry_depth.GetOutputPort())
mapper_depth.SetScalarModeToUseCellFieldData()
mapper_depth.SelectColorArray("Depth")
mapper_depth.SetScalarRange(0.0, 4.0)

# Actor 1: Depth-colored surface
actor_depth = vtkActor()
actor_depth.SetMapper(mapper_depth)
actor_depth.GetProperty().EdgeVisibilityOn()
actor_depth.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Greyscale LUT: dark (low gradient) to bright (high gradient at refinement zones)
calculator.Update()
grad_range = calculator.GetOutput().GetCellData().GetArray("GradientMagnitude").GetRange()
grey_lut = vtkLookupTable()
grey_lut.SetRange(grad_range)
grey_lut.SetValueRange(0.2, 1.0)
grey_lut.SetSaturationRange(0.0, 0.0)
grey_lut.SetHueRange(0.0, 0.0)
grey_lut.SetNumberOfTableValues(256)
grey_lut.SetScaleToLog10()
grey_lut.Build()

# Mapper 2: color by GradientMagnitude with greyscale (right viewport)
mapper_grad = vtkPolyDataMapper()
mapper_grad.SetInputConnection(calculator.GetOutputPort())
mapper_grad.SetScalarModeToUseCellFieldData()
mapper_grad.SelectColorArray("GradientMagnitude")
mapper_grad.SetScalarRange(grad_range)
mapper_grad.SetLookupTable(grey_lut)

# Actor 2: Gradient-magnitude-colored surface
actor_grad = vtkActor()
actor_grad.SetMapper(mapper_grad)
actor_grad.GetProperty().EdgeVisibilityOn()
actor_grad.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Renderer 1: left viewport — Depth coloring
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_depth)
renderer_left.SetBackground(slate_gray_background_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().Azimuth(150)
renderer_left.GetActiveCamera().Elevation(30)
renderer_left.ResetCameraClippingRange()

# Renderer 2: right viewport — GradientMagnitude coloring
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_grad)
renderer_right.SetBackground(slate_gray_background_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1024, 480)
render_window.SetWindowName("HyperTreeGridGradient")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
