#!/usr/bin/env python

# Extract cell centers from a hyper tree grid using
# vtkHyperTreeGridCellCenters and render them as sphere glyphs
# alongside a translucent wireframe of the full HTG.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridCellCenters,
    vtkHyperTreeGridGeometry,
)
from vtkmodules.vtkFiltersSources import (
    vtkHyperTreeGridSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
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

# Filter: extract cell centers as a point set
cell_centers = vtkHyperTreeGridCellCenters()
cell_centers.SetInputConnection(source.GetOutputPort())

# Calculator: compute InverseDepth = (5 - Depth) so coarse cells get large glyphs
calculator = vtkArrayCalculator()
calculator.SetInputConnection(cell_centers.GetOutputPort())
calculator.AddScalarVariable("d", "Depth", 0)
calculator.SetFunction("5 - d")
calculator.SetResultArrayName("InverseDepth")
calculator.SetAttributeTypeToPointData()

# Glyph: place a sphere at each cell center, sized by inverse depth
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetPhiResolution(8)
sphere.SetThetaResolution(8)

glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputConnection(calculator.GetOutputPort())
glyph_mapper.SetSourceConnection(sphere.GetOutputPort())
glyph_mapper.SetScalarModeToUsePointFieldData()
glyph_mapper.SelectColorArray("Depth")
glyph_mapper.SetScalarRange(0.0, 4.0)
glyph_mapper.SetScaleArray("InverseDepth")
glyph_mapper.SetScaleModeToScaleByMagnitude()
glyph_mapper.SetScaleFactor(0.008)

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Context: translucent wireframe of the full HTG
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(source.GetOutputPort())

context_mapper = vtkPolyDataMapper()
context_mapper.SetInputConnection(geometry.GetOutputPort())
context_mapper.ScalarVisibilityOff()

context_actor = vtkActor()
context_actor.SetMapper(context_mapper)
context_actor.GetProperty().SetColor(light_gray_rgb)
context_actor.GetProperty().SetOpacity(0.15)
context_actor.GetProperty().EdgeVisibilityOn()
context_actor.GetProperty().SetEdgeColor(0.6, 0.6, 0.6)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
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
render_window.SetWindowName("HyperTreeGridCellCenters")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
