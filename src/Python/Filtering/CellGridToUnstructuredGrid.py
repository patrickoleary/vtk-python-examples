#!/usr/bin/env python

# Convert a DG cell grid to an unstructured grid using
# vtkCellGridToUnstructuredGrid. A vtkCellGridCellSource generates
# DG cells of several types and the converter produces standard VTK
# unstructured grids that can be rendered with conventional mappers.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCellGrid import (
    vtkCellGridCellSource,
    vtkCellGridToUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
gold_rgb = (1.000, 0.843, 0.000)
sea_green_rgb = (0.180, 0.545, 0.341)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

cell_types = ["vtkDGTet", "vtkDGHex", "vtkDGWdg", "vtkDGPyr"]
colors = [tomato_rgb, cornflower_blue_rgb, gold_rgb, sea_green_rgb]
offsets = [(-1.5, 0.0, 0.0), (-0.5, 0.0, 0.0), (0.5, 0.0, 0.0), (1.5, 0.0, 0.0)]

renderer = vtkRenderer()
renderer.SetBackground(slate_gray_background_rgb)

for cell_type, color, offset in zip(cell_types, colors, offsets):
    # Source: generate a single DG cell
    source = vtkCellGridCellSource()
    source.SetCellType(cell_type)

    # Converter: transform cell grid to unstructured grid
    converter = vtkCellGridToUnstructuredGrid()
    converter.SetInputConnection(source.GetOutputPort())

    # Mapper: map the unstructured grid
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(converter.GetOutputPort())

    # Actor: position and color each cell type
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
    actor.GetProperty().SetLineWidth(2)
    actor.SetPosition(offset)

    renderer.AddActor(actor)

renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("CellGridToUnstructuredGrid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
