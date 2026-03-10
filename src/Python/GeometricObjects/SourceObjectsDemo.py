#!/usr/bin/env python

# Display nine VTK source objects in a 3 × 3 grid of viewports, each
# with its own renderer.  Every object has a peach puff front face and
# a tomato back-face, with a centred text label at the bottom.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkDiskSource,
    vtkLineSource,
    vtkPlaneSource,
    vtkPointSource,
    vtkSphereSource,
    vtkTextSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# ---------------------------------------------------------------------------
# Source definitions: (label, source_factory, factory_setup)
# factory_setup is a callable that configures the source after creation.
# ---------------------------------------------------------------------------
source_defs = [
    ("Sphere",      vtkSphereSource,   lambda s: (s.SetPhiResolution(21), s.SetThetaResolution(21))),
    ("Cone",        vtkConeSource,     lambda s: s.SetResolution(51)),
    ("Cylinder",    vtkCylinderSource, lambda s: s.SetResolution(51)),
    ("Cube",        vtkCubeSource,     lambda s: None),
    ("Plane",       vtkPlaneSource,    lambda s: None),
    ("Text",        vtkTextSource,     lambda s: (s.SetText("Hello"), s.BackingOff())),
    ("PointSource", vtkPointSource,    lambda s: s.SetNumberOfPoints(500)),
    ("Disk",        vtkDiskSource,     lambda s: s.SetCircumferentialResolution(51)),
    ("Line",        vtkLineSource,     lambda s: None),
]

# ---------------------------------------------------------------------------
# Viewport grid: 3 columns × 3 rows
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 3

# Shared back-face property
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

# Window: create before adding renderers
render_window = vtkRenderWindow()
render_window.SetSize(640, 640)
render_window.SetWindowName("SourceObjectsDemo")

for idx, (label, factory, setup) in enumerate(source_defs):
    col = idx % num_cols
    row = (num_rows - 1) - idx // num_cols

    xmin = col / num_cols
    xmax = (col + 1) / num_cols
    ymin = row / num_rows
    ymax = (row + 1) / num_rows

    # ---- Source: generate polygon data ----
    source = factory()
    setup(source)

    # ---- Mapper: map polygon data to graphics primitives ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    # ---- Actor: assign the mapped geometry with a tomato back-face ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(peach_puff_rgb)
    actor.SetBackfaceProperty(back_property)

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
    renderer.SetBackground(background_rgb)
    renderer.SetViewport(xmin, ymin, xmax, ymax)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1.3)

    render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
