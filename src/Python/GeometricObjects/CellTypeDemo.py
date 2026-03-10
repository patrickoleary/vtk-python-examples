#!/usr/bin/env python

# Demonstrate vtkCellTypeSource for all supported cell types: 1D lines,
# 2D triangles and quads, and 3D tetrahedra, hexahedra, wedges, and
# pyramids — both linear and quadratic variants. Each cell is generated,
# perturbed, shrunk, tessellated, and displayed in a labeled 4×4 grid
# of viewports, each with its own renderer.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_CUBIC_LINE,
    VTK_HEXAHEDRON,
    VTK_LINE,
    VTK_PYRAMID,
    VTK_QUAD,
    VTK_QUADRATIC_EDGE,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_PYRAMID,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TETRA,
    VTK_QUADRATIC_TRIANGLE,
    VTK_QUADRATIC_WEDGE,
    VTK_TETRA,
    VTK_TRIANGLE,
    VTK_WEDGE,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkShrinkFilter,
    vtkTessellatorFilter,
)
from vtkmodules.vtkFiltersSources import vtkCellTypeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkTextActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# ---------------------------------------------------------------------------
# Cell definitions: (label, VTK_CELL_TYPE, tessellate, rotate_3d)
# Organized by row:
#   Row 0 (top):    1D — Line, Quadratic Edge, Cubic Line
#   Row 1:          2D — Triangle, Quadratic Triangle, Quad, Quadratic Quad
#   Row 2:          3D — Tetra, Quadratic Tetra, Hexahedron, Quadratic Hexahedron
#   Row 3 (bottom): 3D — Wedge, Quadratic Wedge, Pyramid, Quadratic Pyramid
# ---------------------------------------------------------------------------
cell_defs = [
    # Row 0: 1D cells
    ("Line", VTK_LINE, True, False),
    ("Quadratic Edge", VTK_QUADRATIC_EDGE, True, False),
    ("Cubic Line", VTK_CUBIC_LINE, True, False),
    # Row 1: 2D cells
    ("Triangle", VTK_TRIANGLE, True, False),
    ("Quadratic Triangle", VTK_QUADRATIC_TRIANGLE, True, False),
    ("Quad", VTK_QUAD, True, False),
    ("Quadratic Quad", VTK_QUADRATIC_QUAD, True, False),
    # Row 2: 3D cells
    ("Tetra", VTK_TETRA, True, True),
    ("Quadratic Tetra", VTK_QUADRATIC_TETRA, True, True),
    ("Hexahedron", VTK_HEXAHEDRON, True, True),
    ("Quadratic Hexahedron", VTK_QUADRATIC_HEXAHEDRON, True, True),
    # Row 3: 3D cells
    ("Wedge", VTK_WEDGE, True, True),
    ("Quadratic Wedge", VTK_QUADRATIC_WEDGE, False, True),
    ("Pyramid", VTK_PYRAMID, True, True),
    ("Quadratic Pyramid", VTK_QUADRATIC_PYRAMID, False, True),
]

# ---------------------------------------------------------------------------
# Viewport grid: 4 columns × 4 rows, 15 cells fill positions 0–14
# Row 0 uses only 3 of 4 columns; rows 1–3 use all 4.
# ---------------------------------------------------------------------------
num_cols = 4
num_rows = 4

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(1200, 900)
render_window.SetWindowName("CellTypeDemo")

for idx, (label, cell_type, tessellate, rotate_3d) in enumerate(cell_defs):
    # Map index to grid position accounting for the gap in row 0
    if idx < 3:
        col = idx
        row = num_rows - 1
    else:
        grid_idx = idx + 1
        col = grid_idx % num_cols
        row = (num_rows - 1) - grid_idx // num_cols

    # Viewport: normalized coordinates [xmin, ymin, xmax, ymax]
    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # Source: generate cells of the given type
    source = vtkCellTypeSource()
    source.SetCellType(cell_type)
    source.Update()

    # Perturb points so cell edges are visible after tessellation
    original_points = source.GetOutput().GetPoints()
    points = vtkPoints()
    points.SetNumberOfPoints(source.GetOutput().GetNumberOfPoints())
    rng = vtkMinimalStandardRandomSequence()
    rng.SetSeed(5070)
    for i in range(points.GetNumberOfPoints()):
        perturbation = [0.0, 0.0, 0.0]
        for j in range(3):
            rng.Next()
            perturbation[j] = rng.GetRangeValue(-0.1, 0.1)
        current = [0.0, 0.0, 0.0]
        original_points.GetPoint(i, current)
        points.SetPoint(i,
                        current[0] + perturbation[0],
                        current[1] + perturbation[1],
                        current[2] + perturbation[2])
    source.GetOutput().SetPoints(points)

    # Cell ID array for scalar coloring
    num_cells = source.GetOutput().GetNumberOfCells()
    id_array = vtkIntArray()
    id_array.SetNumberOfTuples(num_cells)
    for i in range(num_cells):
        id_array.InsertTuple1(i, i + 1)
    id_array.SetName("Ids")
    source.GetOutput().GetCellData().AddArray(id_array)
    source.GetOutput().GetCellData().SetActiveScalars("Ids")

    # Shrink: separate cells visually
    shrink = vtkShrinkFilter()
    shrink.SetInputConnection(source.GetOutputPort())
    shrink.SetShrinkFactor(0.8)

    # Tessellate (optional): subdivide higher-order cells into linear primitives
    if tessellate:
        tessellator = vtkTessellatorFilter()
        tessellator.SetInputConnection(shrink.GetOutputPort())
        tessellator.SetMaximumNumberOfSubdivisions(3)
        mapper_input = tessellator.GetOutputPort()
    else:
        mapper_input = shrink.GetOutputPort()

    # Mapper: color by cell ID
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(mapper_input)
    mapper.SetScalarRange(0, num_cells + 1)
    mapper.SetScalarModeToUseCellData()
    mapper.SetResolveCoincidentTopologyToPolygonOffset()

    # Actor
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    if rotate_3d:
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

# Empty renderer for the unused 16th viewport (top-right)
empty_renderer = vtkRenderer()
empty_renderer.SetBackground(dark_blue_background_rgb)
empty_renderer.SetViewport(3 / num_cols, (num_rows - 1) / num_rows, 1, 1)
render_window.AddRenderer(empty_renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
