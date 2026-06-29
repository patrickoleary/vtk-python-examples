#!/usr/bin/env python

# Demonstrate eight 3D linear cell types in a 3×3 grid of viewports,
# each with its own renderer and label. Uses a for loop over cell
# definitions to build the unstructured grids, mappers, actors, and
# renderers.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_POLYHEDRON,
    vtkHexagonalPrism,
    vtkHexahedron,
    vtkPentagonalPrism,
    vtkPyramid,
    vtkTetra,
    vtkUnstructuredGrid,
    vtkVoxel,
    vtkWedge,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkTextActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# ---------------------------------------------------------------------------
# Viewport grid: 3 columns × 3 rows, 8 cells fill positions 0–7
#   Row 2 (top):    Hexagonal Prism, Hexahedron, Pentagonal Prism
#   Row 1:          Polyhedron (Dodecahedron), Pyramid, Tetrahedron
#   Row 0 (bottom): Voxel, Wedge, (empty)
# ---------------------------------------------------------------------------

# --- Hexagonal Prism — Source, Mapper, Actor ------------------------------
hex_prism_points = vtkPoints()
for pt in [(-0.35, -0.35, 0.35), (0.35, -0.35, 0.35), (0.7, 0.0, 0.35),
           (0.35, 0.35, 0.35), (-0.35, 0.35, 0.35), (-0.7, 0.0, 0.35),
           (-0.35, -0.35, -0.35), (0.35, -0.35, -0.35), (0.7, 0.0, -0.35),
           (0.35, 0.35, -0.35), (-0.35, 0.35, -0.35), (-0.7, 0.0, -0.35)]:
    hex_prism_points.InsertNextPoint(*pt)

hex_prism_grid = vtkUnstructuredGrid()
hex_prism_grid.SetPoints(hex_prism_points)
hex_prism_cell = vtkHexagonalPrism()
for i in range(12):
    hex_prism_cell.GetPointIds().SetId(i, i)
hex_prism_grid.InsertNextCell(hex_prism_cell.GetCellType(), hex_prism_cell.GetPointIds())

hex_prism_mapper = vtkDataSetMapper()
hex_prism_mapper.SetInputData(hex_prism_grid)

hex_prism_actor = vtkActor()
hex_prism_actor.SetMapper(hex_prism_mapper)
hex_prism_actor.GetProperty().SetColor(peach_puff_rgb)
hex_prism_actor.RotateX(20.0)
hex_prism_actor.RotateY(-20.0)

hex_prism_text_actor = vtkTextActor()
hex_prism_text_actor.SetInput("Hexagonal Prism")
hex_prism_text_actor.GetTextProperty().SetFontSize(16)
hex_prism_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
hex_prism_text_actor.GetTextProperty().SetJustificationToCentered()
hex_prism_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
hex_prism_text_actor.SetPosition(0.5, 0.01)

# --- Hexahedron — Source, Mapper, Actor -----------------------------------
hexahedron_points = vtkPoints()
for pt in [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
           (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)]:
    hexahedron_points.InsertNextPoint(*pt)

hexahedron_grid = vtkUnstructuredGrid()
hexahedron_grid.SetPoints(hexahedron_points)
hexahedron_cell = vtkHexahedron()
for i in range(8):
    hexahedron_cell.GetPointIds().SetId(i, i)
hexahedron_grid.InsertNextCell(hexahedron_cell.GetCellType(), hexahedron_cell.GetPointIds())

hexahedron_mapper = vtkDataSetMapper()
hexahedron_mapper.SetInputData(hexahedron_grid)

hexahedron_actor = vtkActor()
hexahedron_actor.SetMapper(hexahedron_mapper)
hexahedron_actor.GetProperty().SetColor(peach_puff_rgb)
hexahedron_actor.RotateX(20.0)
hexahedron_actor.RotateY(-20.0)

hexahedron_text_actor = vtkTextActor()
hexahedron_text_actor.SetInput("Hexahedron")
hexahedron_text_actor.GetTextProperty().SetFontSize(16)
hexahedron_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
hexahedron_text_actor.GetTextProperty().SetJustificationToCentered()
hexahedron_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
hexahedron_text_actor.SetPosition(0.5, 0.01)

# --- Pentagonal Prism — Source, Mapper, Actor -----------------------------
pent_prism_points = vtkPoints()
for pt in [(-0.375, -0.75, -0.75), (0.375, -0.75, -0.75), (0.75, 0.0, -0.75),
           (0.0, 0.75, -0.75), (-0.75, 0.0, -0.75),
           (-0.375, -0.75, 0.75), (0.375, -0.75, 0.75), (0.75, 0.0, 0.75),
           (0.0, 0.75, 0.75), (-0.75, 0.0, 0.75)]:
    pent_prism_points.InsertNextPoint(*pt)

pent_prism_grid = vtkUnstructuredGrid()
pent_prism_grid.SetPoints(pent_prism_points)
pent_prism_cell = vtkPentagonalPrism()
for i in range(10):
    pent_prism_cell.GetPointIds().SetId(i, i)
pent_prism_grid.InsertNextCell(pent_prism_cell.GetCellType(), pent_prism_cell.GetPointIds())

pent_prism_mapper = vtkDataSetMapper()
pent_prism_mapper.SetInputData(pent_prism_grid)

pent_prism_actor = vtkActor()
pent_prism_actor.SetMapper(pent_prism_mapper)
pent_prism_actor.GetProperty().SetColor(peach_puff_rgb)
pent_prism_actor.RotateX(20.0)
pent_prism_actor.RotateY(-20.0)

pent_prism_text_actor = vtkTextActor()
pent_prism_text_actor.SetInput("Pentagonal Prism")
pent_prism_text_actor.GetTextProperty().SetFontSize(16)
pent_prism_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
pent_prism_text_actor.GetTextProperty().SetJustificationToCentered()
pent_prism_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pent_prism_text_actor.SetPosition(0.5, 0.01)

# --- Polyhedron (Dodecahedron) — Source, Mapper, Actor --------------------
dodecahedron_scale = 0.35
dodecahedron_raw = [
    (1.21412, 0, 1.58931), (0.375185, 1.1547, 1.58931),
    (-0.982247, 0.713644, 1.58931), (-0.982247, -0.713644, 1.58931),
    (0.375185, -1.1547, 1.58931), (1.96449, 0, 0.375185),
    (0.607062, 1.86835, 0.375185), (-1.58931, 1.1547, 0.375185),
    (-1.58931, -1.1547, 0.375185), (0.607062, -1.86835, 0.375185),
    (1.58931, 1.1547, -0.375185), (-0.607062, 1.86835, -0.375185),
    (-1.96449, 0, -0.375185), (-0.607062, -1.86835, -0.375185),
    (1.58931, -1.1547, -0.375185), (0.982247, 0.713644, -1.58931),
    (-0.375185, 1.1547, -1.58931), (-1.21412, 0, -1.58931),
    (-0.375185, -1.1547, -1.58931), (0.982247, -0.713644, -1.58931),
]
dodecahedron_faces = [
    [0, 1, 2, 3, 4], [0, 5, 10, 6, 1], [1, 6, 11, 7, 2],
    [2, 7, 12, 8, 3], [3, 8, 13, 9, 4], [4, 9, 14, 5, 0],
    [15, 10, 5, 14, 19], [16, 11, 6, 10, 15], [17, 12, 7, 11, 16],
    [18, 13, 8, 12, 17], [19, 14, 9, 13, 18], [19, 18, 17, 16, 15],
]

polyhedron_points = vtkPoints()
for x, y, z in dodecahedron_raw:
    polyhedron_points.InsertNextPoint(
        x * dodecahedron_scale, y * dodecahedron_scale, z * dodecahedron_scale
    )

polyhedron_grid = vtkUnstructuredGrid()
polyhedron_grid.SetPoints(polyhedron_points)
polyhedron_faces_id_list = vtkIdList()
polyhedron_faces_id_list.InsertNextId(len(dodecahedron_faces))
for face in dodecahedron_faces:
    polyhedron_faces_id_list.InsertNextId(len(face))
    for pid in face:
        polyhedron_faces_id_list.InsertNextId(pid)
polyhedron_grid.InsertNextCell(VTK_POLYHEDRON, polyhedron_faces_id_list)

polyhedron_mapper = vtkDataSetMapper()
polyhedron_mapper.SetInputData(polyhedron_grid)

polyhedron_actor = vtkActor()
polyhedron_actor.SetMapper(polyhedron_mapper)
polyhedron_actor.GetProperty().SetColor(peach_puff_rgb)
polyhedron_actor.RotateX(20.0)
polyhedron_actor.RotateY(-20.0)

polyhedron_text_actor = vtkTextActor()
polyhedron_text_actor.SetInput("Polyhedron\n(Dodecahedron)")
polyhedron_text_actor.GetTextProperty().SetFontSize(16)
polyhedron_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
polyhedron_text_actor.GetTextProperty().SetJustificationToCentered()
polyhedron_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
polyhedron_text_actor.SetPosition(0.5, 0.01)

# --- Pyramid — Source, Mapper, Actor --------------------------------------
pyramid_points = vtkPoints()
for pt in [(0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
           (0.5, -0.5, -0.5), (0.0, 0.0, 0.5)]:
    pyramid_points.InsertNextPoint(*pt)

pyramid_grid = vtkUnstructuredGrid()
pyramid_grid.SetPoints(pyramid_points)
pyramid_cell = vtkPyramid()
for i in range(5):
    pyramid_cell.GetPointIds().SetId(i, i)
pyramid_grid.InsertNextCell(pyramid_cell.GetCellType(), pyramid_cell.GetPointIds())

pyramid_mapper = vtkDataSetMapper()
pyramid_mapper.SetInputData(pyramid_grid)

pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)
pyramid_actor.GetProperty().SetColor(peach_puff_rgb)
pyramid_actor.RotateX(20.0)
pyramid_actor.RotateY(-20.0)

pyramid_text_actor = vtkTextActor()
pyramid_text_actor.SetInput("Pyramid")
pyramid_text_actor.GetTextProperty().SetFontSize(16)
pyramid_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
pyramid_text_actor.GetTextProperty().SetJustificationToCentered()
pyramid_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
pyramid_text_actor.SetPosition(0.5, 0.01)

# --- Tetrahedron — Source, Mapper, Actor ----------------------------------
tetrahedron_points = vtkPoints()
for pt in [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, 0.5)]:
    tetrahedron_points.InsertNextPoint(*pt)

tetrahedron_grid = vtkUnstructuredGrid()
tetrahedron_grid.SetPoints(tetrahedron_points)
tetrahedron_cell = vtkTetra()
for i in range(4):
    tetrahedron_cell.GetPointIds().SetId(i, i)
tetrahedron_grid.InsertNextCell(tetrahedron_cell.GetCellType(), tetrahedron_cell.GetPointIds())

tetrahedron_mapper = vtkDataSetMapper()
tetrahedron_mapper.SetInputData(tetrahedron_grid)

tetrahedron_actor = vtkActor()
tetrahedron_actor.SetMapper(tetrahedron_mapper)
tetrahedron_actor.GetProperty().SetColor(peach_puff_rgb)
tetrahedron_actor.RotateX(20.0)
tetrahedron_actor.RotateY(-20.0)

tetrahedron_text_actor = vtkTextActor()
tetrahedron_text_actor.SetInput("Tetrahedron")
tetrahedron_text_actor.GetTextProperty().SetFontSize(16)
tetrahedron_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
tetrahedron_text_actor.GetTextProperty().SetJustificationToCentered()
tetrahedron_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
tetrahedron_text_actor.SetPosition(0.5, 0.01)

# --- Voxel — Source, Mapper, Actor ----------------------------------------
voxel_points = vtkPoints()
for pt in [(-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5),
           (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5)]:
    voxel_points.InsertNextPoint(*pt)

voxel_grid = vtkUnstructuredGrid()
voxel_grid.SetPoints(voxel_points)
voxel_cell = vtkVoxel()
for i in range(8):
    voxel_cell.GetPointIds().SetId(i, i)
voxel_grid.InsertNextCell(voxel_cell.GetCellType(), voxel_cell.GetPointIds())

voxel_mapper = vtkDataSetMapper()
voxel_mapper.SetInputData(voxel_grid)

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.GetProperty().SetColor(peach_puff_rgb)
voxel_actor.RotateX(20.0)
voxel_actor.RotateY(-20.0)

voxel_text_actor = vtkTextActor()
voxel_text_actor.SetInput("Voxel")
voxel_text_actor.GetTextProperty().SetFontSize(16)
voxel_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
voxel_text_actor.GetTextProperty().SetJustificationToCentered()
voxel_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
voxel_text_actor.SetPosition(0.5, 0.01)

# --- Wedge — Source, Mapper, Actor ----------------------------------------
wedge_points = vtkPoints()
for pt in [(-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.0, 0.5),
           (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.0, 0.5)]:
    wedge_points.InsertNextPoint(*pt)

wedge_grid = vtkUnstructuredGrid()
wedge_grid.SetPoints(wedge_points)
wedge_cell = vtkWedge()
for i in range(6):
    wedge_cell.GetPointIds().SetId(i, i)
wedge_grid.InsertNextCell(wedge_cell.GetCellType(), wedge_cell.GetPointIds())

wedge_mapper = vtkDataSetMapper()
wedge_mapper.SetInputData(wedge_grid)

wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)
wedge_actor.GetProperty().SetColor(peach_puff_rgb)
wedge_actor.RotateX(20.0)
wedge_actor.RotateY(-20.0)

wedge_text_actor = vtkTextActor()
wedge_text_actor.SetInput("Wedge")
wedge_text_actor.GetTextProperty().SetFontSize(16)
wedge_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
wedge_text_actor.GetTextProperty().SetJustificationToCentered()
wedge_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
wedge_text_actor.SetPosition(0.5, 0.01)

# --- Renderers: one per viewport ------------------------------------------
hex_prism_renderer = vtkRenderer()
hex_prism_renderer.AddActor(hex_prism_actor)
hex_prism_renderer.AddViewProp(hex_prism_text_actor)
hex_prism_renderer.SetBackground(dark_blue_background_rgb)
hex_prism_renderer.SetViewport(0.0, 2.0 / 3.0, 1.0 / 3.0, 1.0)

hexahedron_renderer = vtkRenderer()
hexahedron_renderer.AddActor(hexahedron_actor)
hexahedron_renderer.AddViewProp(hexahedron_text_actor)
hexahedron_renderer.SetBackground(dark_blue_background_rgb)
hexahedron_renderer.SetViewport(1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0, 1.0)

pent_prism_renderer = vtkRenderer()
pent_prism_renderer.AddActor(pent_prism_actor)
pent_prism_renderer.AddViewProp(pent_prism_text_actor)
pent_prism_renderer.SetBackground(dark_blue_background_rgb)
pent_prism_renderer.SetViewport(2.0 / 3.0, 2.0 / 3.0, 1.0, 1.0)

polyhedron_renderer = vtkRenderer()
polyhedron_renderer.AddActor(polyhedron_actor)
polyhedron_renderer.AddViewProp(polyhedron_text_actor)
polyhedron_renderer.SetBackground(dark_blue_background_rgb)
polyhedron_renderer.SetViewport(0.0, 1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)

pyramid_renderer = vtkRenderer()
pyramid_renderer.AddActor(pyramid_actor)
pyramid_renderer.AddViewProp(pyramid_text_actor)
pyramid_renderer.SetBackground(dark_blue_background_rgb)
pyramid_renderer.SetViewport(1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)

tetrahedron_renderer = vtkRenderer()
tetrahedron_renderer.AddActor(tetrahedron_actor)
tetrahedron_renderer.AddViewProp(tetrahedron_text_actor)
tetrahedron_renderer.SetBackground(dark_blue_background_rgb)
tetrahedron_renderer.SetViewport(2.0 / 3.0, 1.0 / 3.0, 1.0, 2.0 / 3.0)

voxel_renderer = vtkRenderer()
voxel_renderer.AddActor(voxel_actor)
voxel_renderer.AddViewProp(voxel_text_actor)
voxel_renderer.SetBackground(dark_blue_background_rgb)
voxel_renderer.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0 / 3.0)

wedge_renderer = vtkRenderer()
wedge_renderer.AddActor(wedge_actor)
wedge_renderer.AddViewProp(wedge_text_actor)
wedge_renderer.SetBackground(dark_blue_background_rgb)
wedge_renderer.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0 / 3.0)

empty_renderer = vtkRenderer()
empty_renderer.SetBackground(dark_blue_background_rgb)
empty_renderer.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0 / 3.0)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(hex_prism_renderer)
render_window.AddRenderer(hexahedron_renderer)
render_window.AddRenderer(pent_prism_renderer)
render_window.AddRenderer(polyhedron_renderer)
render_window.AddRenderer(pyramid_renderer)
render_window.AddRenderer(tetrahedron_renderer)
render_window.AddRenderer(voxel_renderer)
render_window.AddRenderer(wedge_renderer)
render_window.AddRenderer(empty_renderer)
render_window.SetWindowName("cells3d demo")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 900)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure cameras for each viewport
hex_prism_renderer.ResetCamera()
hex_prism_renderer.GetActiveCamera().Zoom(1.3)
hexahedron_renderer.ResetCamera()
hexahedron_renderer.GetActiveCamera().Zoom(1.3)
pent_prism_renderer.ResetCamera()
pent_prism_renderer.GetActiveCamera().Zoom(1.3)
polyhedron_renderer.ResetCamera()
polyhedron_renderer.GetActiveCamera().Zoom(1.3)
pyramid_renderer.ResetCamera()
pyramid_renderer.GetActiveCamera().Zoom(1.3)
tetrahedron_renderer.ResetCamera()
tetrahedron_renderer.GetActiveCamera().Zoom(1.3)
voxel_renderer.ResetCamera()
voxel_renderer.GetActiveCamera().Zoom(1.3)
wedge_renderer.ResetCamera()
wedge_renderer.GetActiveCamera().Zoom(1.3)

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
