#!/usr/bin/env python

# Compute visible leaf cell sizes in a hyper tree grid using
# vtkHyperTreeGridGenerateFields and color the surface by
# the computed cell-size array.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridGenerateFields,
    vtkHyperTreeGridGeometry,
)
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
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

# Filter: compute the visible leaf cell sizes
generate_fields = vtkHyperTreeGridGenerateFields()
generate_fields.SetInputConnection(source.GetOutputPort())
generate_fields.SetComputeCellSizeArray(True)
generate_fields.Update()

size_array_name = generate_fields.GetCellSizeArrayName()
cell_data = generate_fields.GetOutput().GetCellData()

# Geometry: extract the surface for rendering
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(generate_fields.GetOutputPort())

# LUT: blue (small cells) → red (large cells)
lut = vtkColorTransferFunction()
size_range = cell_data.GetArray(size_array_name).GetRange()
lut.AddRGBPoint(size_range[0], 0.231, 0.298, 0.753)
lut.AddRGBPoint(0.5 * (size_range[0] + size_range[1]), 0.865, 0.865, 0.865)
lut.AddRGBPoint(size_range[1], 0.706, 0.016, 0.149)

# Mapper: map the surface colored by cell size
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray(size_array_name)
mapper.SetScalarRange(size_range)
mapper.SetLookupTable(lut)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(150)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("HyperTreeGridVisibleLeavesSize")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
