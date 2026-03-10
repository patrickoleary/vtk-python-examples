#!/usr/bin/env python

# Display all 21 parametric surfaces arranged in a 5 × 5 grid of viewports,
# each with its own renderer.  Each surface is normalized, centered, and
# labelled with a 2D text title pinned to the bottom of the viewport.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import (
    vtkParametricBohemianDome,
    vtkParametricBour,
    vtkParametricBoy,
    vtkParametricCatalanMinimal,
    vtkParametricConicSpiral,
    vtkParametricCrossCap,
    vtkParametricDini,
    vtkParametricEllipsoid,
    vtkParametricEnneper,
    vtkParametricFigure8Klein,
    vtkParametricHenneberg,
    vtkParametricKlein,
    vtkParametricKuen,
    vtkParametricMobius,
    vtkParametricPluckerConoid,
    vtkParametricPseudosphere,
    vtkParametricRandomHills,
    vtkParametricRoman,
    vtkParametricSpline,
    vtkParametricSuperEllipsoid,
    vtkParametricSuperToroid,
    vtkParametricTorus,
)
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
navajo_white_rgb = (1.0, 0.871, 0.678)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# ---------------------------------------------------------------------------
# Build parametric function instances (alphabetical order).
# Some require custom parameter settings.
# ---------------------------------------------------------------------------
bohemian_dome = vtkParametricBohemianDome()
bohemian_dome.SetA(5.0)
bohemian_dome.SetB(1.0)
bohemian_dome.SetC(2.0)

ellipsoid = vtkParametricEllipsoid()
ellipsoid.SetXRadius(0.5)
ellipsoid.SetYRadius(2.0)

kuen = vtkParametricKuen()
kuen.SetDeltaV0(0.001)

mobius = vtkParametricMobius()
mobius.SetRadius(2.0)
mobius.SetMinimumV(-0.5)
mobius.SetMaximumV(0.5)

random_hills = vtkParametricRandomHills()
random_hills.AllowRandomGenerationOn()
random_hills.SetRandomSeed(1)
random_hills.SetNumberOfHills(30)

spline = vtkParametricSpline()
spline_points = vtkPoints()
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
for _ in range(10):
    xyz = [0.0] * 3
    for j in range(3):
        xyz[j] = rng.GetRangeValue(-1.0, 1.0)
        rng.Next()
    spline_points.InsertNextPoint(xyz)
spline.SetPoints(spline_points)

super_ellipsoid = vtkParametricSuperEllipsoid()
super_ellipsoid.SetN1(0.5)
super_ellipsoid.SetN2(0.4)

super_toroid = vtkParametricSuperToroid()
super_toroid.SetN1(0.5)
super_toroid.SetN2(3.0)

# ---------------------------------------------------------------------------
# Surface definitions: (label, parametric_function)
# ---------------------------------------------------------------------------
surface_defs = [
    ("BohemianDome",    bohemian_dome),
    ("Bour",            vtkParametricBour()),
    ("Boy",             vtkParametricBoy()),
    ("CatalanMinimal",  vtkParametricCatalanMinimal()),
    ("ConicSpiral",     vtkParametricConicSpiral()),
    ("CrossCap",        vtkParametricCrossCap()),
    ("Dini",            vtkParametricDini()),
    ("Ellipsoid",       ellipsoid),
    ("Enneper",         vtkParametricEnneper()),
    ("Figure8Klein",    vtkParametricFigure8Klein()),
    ("Henneberg",       vtkParametricHenneberg()),
    ("Klein",           vtkParametricKlein()),
    ("Kuen",            kuen),
    ("Mobius",          mobius),
    ("PluckerConoid",   vtkParametricPluckerConoid()),
    ("Pseudosphere",    vtkParametricPseudosphere()),
    ("RandomHills",     random_hills),
    ("Roman",           vtkParametricRoman()),
    ("Spline",          spline),
    ("SuperEllipsoid",  super_ellipsoid),
    ("SuperToroid",     super_toroid),
    ("Torus",           vtkParametricTorus()),
]

# ---------------------------------------------------------------------------
# Viewport grid: 5 columns × 5 rows (25 cells, 21 filled)
# ---------------------------------------------------------------------------
num_cols = 5
num_rows = 5

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(1200, 1200)
render_window.SetWindowName("ParametricObjectsDemo")

for idx, (label, parametric_fn) in enumerate(surface_defs):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    # Viewport rectangle
    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # ---- Source: sample parametric function ----
    source = vtkParametricFunctionSource()
    source.SetParametricFunction(parametric_fn)
    source.SetUResolution(51)
    source.SetVResolution(51)
    source.SetWResolution(51)
    source.Update()

    # Normalize scale so every surface fits the same cell size
    bounds = source.GetOutput().GetBounds()
    max_dim = max(bounds[1] - bounds[0],
                  bounds[3] - bounds[2],
                  bounds[5] - bounds[4])
    scale = 3.0 / max_dim if max_dim > 0 else 1.0
    cx = (bounds[0] + bounds[1]) / 2.0
    cy = (bounds[2] + bounds[3]) / 2.0
    cz = (bounds[4] + bounds[5]) / 2.0

    # ---- Mapper → Actor ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(navajo_white_rgb)
    actor.SetScale(scale, scale, scale)
    actor.SetPosition(-cx * scale, -cy * scale, -cz * scale)

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
    renderer.SetBackground(midnight_blue_rgb)
    renderer.SetViewport(xmin, ymin, xmax, ymax)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.3)

    render_window.AddRenderer(renderer)

# Fill remaining empty cells with background-only renderers
for idx in range(len(surface_defs), num_cols * num_rows):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols
    empty_renderer = vtkRenderer()
    empty_renderer.SetBackground(midnight_blue_rgb)
    empty_renderer.SetViewport(col / num_cols, row / num_rows,
                               (col + 1) / num_cols, (row + 1) / num_rows)
    render_window.AddRenderer(empty_renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
