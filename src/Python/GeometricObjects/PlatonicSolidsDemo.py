#!/usr/bin/env python

# Display the five Platonic solids (tetrahedron, cube, octahedron,
# icosahedron, dodecahedron) in a 3 × 2 grid of viewports, each with
# its own renderer.  Each face is colored with a lookup table so
# adjacent faces are visually distinct.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkPlatonicSolidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Lookup table: each face of a vtkPlatonicSolidSource has a different cell
# scalar.  The colors are chosen so that adjacent faces are visually distinct.
lut = vtkLookupTable()
lut.SetNumberOfTableValues(20)
lut.SetTableRange(0.0, 19.0)
lut.Build()
lut.SetTableValue(0, 0.1, 0.1, 0.1)
lut.SetTableValue(1, 0, 0, 1)
lut.SetTableValue(2, 0, 1, 0)
lut.SetTableValue(3, 0, 1, 1)
lut.SetTableValue(4, 1, 0, 0)
lut.SetTableValue(5, 1, 0, 1)
lut.SetTableValue(6, 1, 1, 0)
lut.SetTableValue(7, 0.9, 0.7, 0.9)
lut.SetTableValue(8, 0.5, 0.5, 0.5)
lut.SetTableValue(9, 0.0, 0.0, 0.7)
lut.SetTableValue(10, 0.5, 0.7, 0.5)
lut.SetTableValue(11, 0, 0.7, 0.7)
lut.SetTableValue(12, 0.7, 0, 0)
lut.SetTableValue(13, 0.7, 0, 0.7)
lut.SetTableValue(14, 0.7, 0.7, 0)
lut.SetTableValue(15, 0, 0, 0.4)
lut.SetTableValue(16, 0, 0.4, 0)
lut.SetTableValue(17, 0, 0.4, 0.4)
lut.SetTableValue(18, 0.4, 0, 0)
lut.SetTableValue(19, 0.4, 0, 0.4)

# ---------------------------------------------------------------------------
# Solid definitions: (label, solid_type, rotate_x, rotate_y)
# ---------------------------------------------------------------------------
solid_defs = [
    ("Tetrahedron",  0, 30, 30),
    ("Cube",         1, 20, -30),
    ("Octahedron",   2, 25, 20),
    ("Icosahedron",  3, 15, -20),
    ("Dodecahedron", 4, 20, 30),
]

# ---------------------------------------------------------------------------
# Viewport grid: 3 columns × 2 rows (6 slots, 5 used + 1 empty)
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 2

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(900, 600)
render_window.SetWindowName("PlatonicSolidsDemo")

for idx, (label, solid_type, rot_x, rot_y) in enumerate(solid_defs):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # ---- Source: generate Platonic solid polygon data ----
    source = vtkPlatonicSolidSource()
    source.SetSolidType(solid_type)

    # ---- Mapper: map polygon data with face coloring via lookup table ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(0, 19)

    # ---- Actor: rotate for a 3D view ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.RotateX(rot_x)
    actor.RotateY(rot_y)

    # ---- Title label: 2D text pinned to bottom of viewport ----
    text_actor = vtkTextActor()
    text_actor.SetInput(label)
    text_actor.GetTextProperty().SetFontSize(14)
    text_actor.GetTextProperty().SetColor(1.0, 1.0, 1.0)
    text_actor.GetTextProperty().SetJustificationToCentered()
    text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
    text_actor.SetPosition(0.5, 0.01)

    # ---- Renderer for this viewport ----
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddViewProp(text_actor)
    renderer.SetBackground(slate_gray_background_rgb)
    renderer.SetViewport(xmin, ymin, xmax, ymax)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.4)

    render_window.AddRenderer(renderer)

# Fill the remaining empty viewport (bottom-right) with the background color
col = len(solid_defs) % num_cols
row = (num_rows - 1) - len(solid_defs) // num_cols
empty_renderer = vtkRenderer()
empty_renderer.SetBackground(slate_gray_background_rgb)
empty_renderer.SetViewport(col / num_cols, row / num_rows,
                           (col + 1) / num_cols, (row + 1) / num_rows)
render_window.AddRenderer(empty_renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
