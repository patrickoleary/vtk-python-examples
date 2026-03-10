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
# Cell definitions: (label, point_coords, cell_type_or_cell, faces_for_polyhedron)
# Each entry builds one unstructured grid for one viewport.
# ---------------------------------------------------------------------------
cells = []

# Hexagonal Prism — 12 points
hexagonal_prism_pts = [
    (-0.35, -0.35, 0.35), (0.35, -0.35, 0.35), (0.7, 0.0, 0.35),
    (0.35, 0.35, 0.35), (-0.35, 0.35, 0.35), (-0.7, 0.0, 0.35),
    (-0.35, -0.35, -0.35), (0.35, -0.35, -0.35), (0.7, 0.0, -0.35),
    (0.35, 0.35, -0.35), (-0.35, 0.35, -0.35), (-0.7, 0.0, -0.35),
]
cells.append(("Hexagonal Prism", hexagonal_prism_pts, vtkHexagonalPrism(), None))

# Hexahedron — 8 points
hexahedron_pts = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
]
cells.append(("Hexahedron", hexahedron_pts, vtkHexahedron(), None))

# Pentagonal Prism — 10 points
pentagonal_prism_pts = [
    (-0.375, -0.75, -0.75), (0.375, -0.75, -0.75), (0.75, 0.0, -0.75),
    (0.0, 0.75, -0.75), (-0.75, 0.0, -0.75),
    (-0.375, -0.75, 0.75), (0.375, -0.75, 0.75), (0.75, 0.0, 0.75),
    (0.0, 0.75, 0.75), (-0.75, 0.0, 0.75),
]
cells.append(("Pentagonal Prism", pentagonal_prism_pts, vtkPentagonalPrism(), None))

# Polyhedron (dodecahedron) — 20 points, 12 pentagonal faces
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
dodecahedron_pts = [
    (x * dodecahedron_scale, y * dodecahedron_scale, z * dodecahedron_scale)
    for x, y, z in dodecahedron_raw
]
dodecahedron_faces = [
    [0, 1, 2, 3, 4], [0, 5, 10, 6, 1], [1, 6, 11, 7, 2],
    [2, 7, 12, 8, 3], [3, 8, 13, 9, 4], [4, 9, 14, 5, 0],
    [15, 10, 5, 14, 19], [16, 11, 6, 10, 15], [17, 12, 7, 11, 16],
    [18, 13, 8, 12, 17], [19, 14, 9, 13, 18], [19, 18, 17, 16, 15],
]
cells.append(("Polyhedron\n(Dodecahedron)", dodecahedron_pts, VTK_POLYHEDRON, dodecahedron_faces))

# Pyramid — 5 points
pyramid_pts = [
    (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5), (0.0, 0.0, 0.5),
]
cells.append(("Pyramid", pyramid_pts, vtkPyramid(), None))

# Tetrahedron — 4 points
tetrahedron_pts = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
]
cells.append(("Tetrahedron", tetrahedron_pts, vtkTetra(), None))

# Voxel — 8 points (i varies fastest)
voxel_pts = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5),
]
cells.append(("Voxel", voxel_pts, vtkVoxel(), None))

# Wedge — 6 points
wedge_pts = [
    (-0.5, 0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.0, 0.5),
    (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.0, 0.5),
]
cells.append(("Wedge", wedge_pts, vtkWedge(), None))

# ---------------------------------------------------------------------------
# Viewport grid: 3 columns × 3 rows, 8 cells fill positions 0–7
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 3

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(900, 900)
render_window.SetWindowName("Cells3DDemo")

for idx, (label, point_coords, cell_or_type, faces) in enumerate(cells):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    # Viewport: normalized coordinates [xmin, ymin, xmax, ymax]
    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # Points
    points = vtkPoints()
    for pt in point_coords:
        points.InsertNextPoint(*pt)

    # Unstructured grid with one cell
    grid = vtkUnstructuredGrid()
    grid.SetPoints(points)

    if faces is not None:
        # Polyhedron: build face ID list
        faces_id_list = vtkIdList()
        faces_id_list.InsertNextId(len(faces))
        for face in faces:
            faces_id_list.InsertNextId(len(face))
            for pid in face:
                faces_id_list.InsertNextId(pid)
        grid.InsertNextCell(cell_or_type, faces_id_list)
    else:
        # Standard cell type
        cell = cell_or_type
        num_pts = len(point_coords)
        for i in range(num_pts):
            cell.GetPointIds().SetId(i, i)
        grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    # Mapper
    mapper = vtkDataSetMapper()
    mapper.SetInputData(grid)

    # Actor: tilt to show 3D shape
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(peach_puff_rgb)
    actor.RotateX(20.0)
    actor.RotateY(-20.0)

    # Label: 2D text pinned to bottom of viewport
    text_actor = vtkTextActor()
    text_actor.SetInput(label)
    text_actor.GetTextProperty().SetFontSize(16)
    text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
    text_actor.GetTextProperty().SetJustificationToCentered()
    text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
    text_actor.SetPosition(0.5, 0.01)

    # Renderer: one per viewport
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddViewProp(text_actor)
    renderer.SetBackground(dark_blue_background_rgb)
    renderer.SetViewport(xmin, ymin, xmax, ymax)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.3)

    render_window.AddRenderer(renderer)

# Empty renderer for the unused 9th viewport (bottom-right)
empty_renderer = vtkRenderer()
empty_renderer.SetBackground(dark_blue_background_rgb)
empty_renderer.SetViewport(2 / num_cols, 0, 1, 1 / num_rows)
render_window.AddRenderer(empty_renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
