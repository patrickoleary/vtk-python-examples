#!/usr/bin/env python

# Display eight basic geometric object sources in a 3×3 grid of viewports,
# each with its own renderer and label. Uses a for loop over source
# definitions to build the mappers, actors, and renderers.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkDiskSource,
    vtkLineSource,
    vtkRegularPolygonSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkTextActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# ---------------------------------------------------------------------------
# Source definitions: (label, source_instance)
# ---------------------------------------------------------------------------
source_defs = [
    ("Arrow", vtkArrowSource()),
    ("Cone", vtkConeSource()),
    ("Cube", vtkCubeSource()),
    ("Cylinder", vtkCylinderSource()),
    ("Disk", vtkDiskSource()),
    ("Line", vtkLineSource()),
    ("Regular Polygon", vtkRegularPolygonSource()),
    ("Sphere", vtkSphereSource()),
]

# ---------------------------------------------------------------------------
# Viewport grid: 3 columns × 3 rows, 8 sources fill positions 0–7
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 3

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(900, 900)
render_window.SetWindowName("GeometricObjectsDemo")

for idx, (label, source) in enumerate(source_defs):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    # Viewport: normalized coordinates [xmin, ymin, xmax, ymax]
    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # Mapper
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    # Actor
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(peach_puff_rgb)

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
