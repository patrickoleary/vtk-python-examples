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

# Source: generate a DG tetrahedron
tet_source = vtkCellGridCellSource()
tet_source.SetCellType("vtkDGTet")

# Converter: transform tet cell grid to unstructured grid
tet_converter = vtkCellGridToUnstructuredGrid()
tet_converter.SetInputConnection(tet_source.GetOutputPort())

# Mapper: map the tet unstructured grid
tet_mapper = vtkDataSetMapper()
tet_mapper.SetInputConnection(tet_converter.GetOutputPort())

# Actor: position and color the tetrahedron
tet_actor = vtkActor()
tet_actor.SetMapper(tet_mapper)
tet_actor.GetProperty().SetColor(tomato_rgb)
tet_actor.GetProperty().EdgeVisibilityOn()
tet_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
tet_actor.GetProperty().SetLineWidth(2)
tet_actor.SetPosition(-1.5, 0.0, 0.0)

# Source: generate a DG hexahedron
hex_source = vtkCellGridCellSource()
hex_source.SetCellType("vtkDGHex")

# Converter: transform hex cell grid to unstructured grid
hex_converter = vtkCellGridToUnstructuredGrid()
hex_converter.SetInputConnection(hex_source.GetOutputPort())

# Mapper: map the hex unstructured grid
hex_mapper = vtkDataSetMapper()
hex_mapper.SetInputConnection(hex_converter.GetOutputPort())

# Actor: position and color the hexahedron
hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)
hex_actor.GetProperty().SetColor(cornflower_blue_rgb)
hex_actor.GetProperty().EdgeVisibilityOn()
hex_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
hex_actor.GetProperty().SetLineWidth(2)
hex_actor.SetPosition(-0.5, 0.0, 0.0)

# Source: generate a DG wedge
wdg_source = vtkCellGridCellSource()
wdg_source.SetCellType("vtkDGWdg")

# Converter: transform wedge cell grid to unstructured grid
wdg_converter = vtkCellGridToUnstructuredGrid()
wdg_converter.SetInputConnection(wdg_source.GetOutputPort())

# Mapper: map the wedge unstructured grid
wdg_mapper = vtkDataSetMapper()
wdg_mapper.SetInputConnection(wdg_converter.GetOutputPort())

# Actor: position and color the wedge
wdg_actor = vtkActor()
wdg_actor.SetMapper(wdg_mapper)
wdg_actor.GetProperty().SetColor(gold_rgb)
wdg_actor.GetProperty().EdgeVisibilityOn()
wdg_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
wdg_actor.GetProperty().SetLineWidth(2)
wdg_actor.SetPosition(0.5, 0.0, 0.0)

# Source: generate a DG pyramid
pyr_source = vtkCellGridCellSource()
pyr_source.SetCellType("vtkDGPyr")

# Converter: transform pyramid cell grid to unstructured grid
pyr_converter = vtkCellGridToUnstructuredGrid()
pyr_converter.SetInputConnection(pyr_source.GetOutputPort())

# Mapper: map the pyramid unstructured grid
pyr_mapper = vtkDataSetMapper()
pyr_mapper.SetInputConnection(pyr_converter.GetOutputPort())

# Actor: position and color the pyramid
pyr_actor = vtkActor()
pyr_actor.SetMapper(pyr_mapper)
pyr_actor.GetProperty().SetColor(sea_green_rgb)
pyr_actor.GetProperty().EdgeVisibilityOn()
pyr_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)
pyr_actor.GetProperty().SetLineWidth(2)
pyr_actor.SetPosition(1.5, 0.0, 0.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(tet_actor)
renderer.AddActor(hex_actor)
renderer.AddActor(wdg_actor)
renderer.AddActor(pyr_actor)
renderer.SetBackground(slate_gray_background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cellgrid to unstructuredgrid")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 400)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
