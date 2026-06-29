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
# Source, mapper, actor: Arrow
# ---------------------------------------------------------------------------
arrow_source = vtkArrowSource()
arrow_mapper = vtkPolyDataMapper()
arrow_mapper.SetInputConnection(arrow_source.GetOutputPort())
arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)
arrow_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Cone
# ---------------------------------------------------------------------------
cone_source = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Cube
# ---------------------------------------------------------------------------
cube_source = vtkCubeSource()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Cylinder
# ---------------------------------------------------------------------------
cylinder_source = vtkCylinderSource()
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Disk
# ---------------------------------------------------------------------------
disk_source = vtkDiskSource()
disk_mapper = vtkPolyDataMapper()
disk_mapper.SetInputConnection(disk_source.GetOutputPort())
disk_actor = vtkActor()
disk_actor.SetMapper(disk_mapper)
disk_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Line
# ---------------------------------------------------------------------------
line_source = vtkLineSource()
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(line_source.GetOutputPort())
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Regular Polygon
# ---------------------------------------------------------------------------
polygon_source = vtkRegularPolygonSource()
polygon_mapper = vtkPolyDataMapper()
polygon_mapper.SetInputConnection(polygon_source.GetOutputPort())
polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)
polygon_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Source, mapper, actor: Sphere
# ---------------------------------------------------------------------------
sphere_source = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(peach_puff_rgb)

# ---------------------------------------------------------------------------
# Text actors (labels)
# ---------------------------------------------------------------------------
arrow_text_actor = vtkTextActor()
arrow_text_actor.SetInput("Arrow")
arrow_text_actor.GetTextProperty().SetFontSize(16)
arrow_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
arrow_text_actor.GetTextProperty().SetJustificationToCentered()
arrow_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
arrow_text_actor.SetPosition(0.5, 0.01)

cone_text_actor = vtkTextActor()
cone_text_actor.SetInput("Cone")
cone_text_actor.GetTextProperty().SetFontSize(16)
cone_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
cone_text_actor.GetTextProperty().SetJustificationToCentered()
cone_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cone_text_actor.SetPosition(0.5, 0.01)

cube_text_actor = vtkTextActor()
cube_text_actor.SetInput("Cube")
cube_text_actor.GetTextProperty().SetFontSize(16)
cube_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
cube_text_actor.GetTextProperty().SetJustificationToCentered()
cube_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cube_text_actor.SetPosition(0.5, 0.01)

cylinder_text_actor = vtkTextActor()
cylinder_text_actor.SetInput("Cylinder")
cylinder_text_actor.GetTextProperty().SetFontSize(16)
cylinder_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
cylinder_text_actor.GetTextProperty().SetJustificationToCentered()
cylinder_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cylinder_text_actor.SetPosition(0.5, 0.01)

disk_text_actor = vtkTextActor()
disk_text_actor.SetInput("Disk")
disk_text_actor.GetTextProperty().SetFontSize(16)
disk_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
disk_text_actor.GetTextProperty().SetJustificationToCentered()
disk_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
disk_text_actor.SetPosition(0.5, 0.01)

line_text_actor = vtkTextActor()
line_text_actor.SetInput("Line")
line_text_actor.GetTextProperty().SetFontSize(16)
line_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
line_text_actor.GetTextProperty().SetJustificationToCentered()
line_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
line_text_actor.SetPosition(0.5, 0.01)

polygon_text_actor = vtkTextActor()
polygon_text_actor.SetInput("Regular Polygon")
polygon_text_actor.GetTextProperty().SetFontSize(16)
polygon_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
polygon_text_actor.GetTextProperty().SetJustificationToCentered()
polygon_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
polygon_text_actor.SetPosition(0.5, 0.01)

sphere_text_actor = vtkTextActor()
sphere_text_actor.SetInput("Sphere")
sphere_text_actor.GetTextProperty().SetFontSize(16)
sphere_text_actor.GetTextProperty().SetColor(0.98, 0.98, 0.82)
sphere_text_actor.GetTextProperty().SetJustificationToCentered()
sphere_text_actor.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
sphere_text_actor.SetPosition(0.5, 0.01)

# ---------------------------------------------------------------------------
# Renderers (3×3 grid, 8 sources fill positions 0–7, position 8 is empty)
# ---------------------------------------------------------------------------
arrow_renderer = vtkRenderer()
arrow_renderer.AddActor(arrow_actor)
arrow_renderer.AddViewProp(arrow_text_actor)
arrow_renderer.SetBackground(dark_blue_background_rgb)
arrow_renderer.SetViewport(0.0, 2.0 / 3.0, 1.0 / 3.0, 1.0)

cone_renderer = vtkRenderer()
cone_renderer.AddActor(cone_actor)
cone_renderer.AddViewProp(cone_text_actor)
cone_renderer.SetBackground(dark_blue_background_rgb)
cone_renderer.SetViewport(1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0, 1.0)

cube_renderer = vtkRenderer()
cube_renderer.AddActor(cube_actor)
cube_renderer.AddViewProp(cube_text_actor)
cube_renderer.SetBackground(dark_blue_background_rgb)
cube_renderer.SetViewport(2.0 / 3.0, 2.0 / 3.0, 1.0, 1.0)

cylinder_renderer = vtkRenderer()
cylinder_renderer.AddActor(cylinder_actor)
cylinder_renderer.AddViewProp(cylinder_text_actor)
cylinder_renderer.SetBackground(dark_blue_background_rgb)
cylinder_renderer.SetViewport(0.0, 1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)

disk_renderer = vtkRenderer()
disk_renderer.AddActor(disk_actor)
disk_renderer.AddViewProp(disk_text_actor)
disk_renderer.SetBackground(dark_blue_background_rgb)
disk_renderer.SetViewport(1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)

line_renderer = vtkRenderer()
line_renderer.AddActor(line_actor)
line_renderer.AddViewProp(line_text_actor)
line_renderer.SetBackground(dark_blue_background_rgb)
line_renderer.SetViewport(2.0 / 3.0, 1.0 / 3.0, 1.0, 2.0 / 3.0)

polygon_renderer = vtkRenderer()
polygon_renderer.AddActor(polygon_actor)
polygon_renderer.AddViewProp(polygon_text_actor)
polygon_renderer.SetBackground(dark_blue_background_rgb)
polygon_renderer.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0 / 3.0)

sphere_renderer = vtkRenderer()
sphere_renderer.AddActor(sphere_actor)
sphere_renderer.AddViewProp(sphere_text_actor)
sphere_renderer.SetBackground(dark_blue_background_rgb)
sphere_renderer.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0 / 3.0)

empty_renderer = vtkRenderer()
empty_renderer.SetBackground(dark_blue_background_rgb)
empty_renderer.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0 / 3.0)

# ---------------------------------------------------------------------------
# Render window
# ---------------------------------------------------------------------------
render_window = vtkRenderWindow()
render_window.AddRenderer(arrow_renderer)
render_window.AddRenderer(cone_renderer)
render_window.AddRenderer(cube_renderer)
render_window.AddRenderer(cylinder_renderer)
render_window.AddRenderer(disk_renderer)
render_window.AddRenderer(line_renderer)
render_window.AddRenderer(polygon_renderer)
render_window.AddRenderer(sphere_renderer)
render_window.AddRenderer(empty_renderer)
render_window.SetWindowName("geometric objects demo")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 900)

# ---------------------------------------------------------------------------
# Interactor
# ---------------------------------------------------------------------------
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# ---------------------------------------------------------------------------
# Scene: configure the cameras
# ---------------------------------------------------------------------------
arrow_renderer.ResetCamera()
arrow_renderer.GetActiveCamera().Zoom(1.3)

cone_renderer.ResetCamera()
cone_renderer.GetActiveCamera().Zoom(1.3)

cube_renderer.ResetCamera()
cube_renderer.GetActiveCamera().Zoom(1.3)

cylinder_renderer.ResetCamera()
cylinder_renderer.GetActiveCamera().Zoom(1.3)

disk_renderer.ResetCamera()
disk_renderer.GetActiveCamera().Zoom(1.3)

line_renderer.ResetCamera()
line_renderer.GetActiveCamera().Zoom(1.3)

polygon_renderer.ResetCamera()
polygon_renderer.GetActiveCamera().Zoom(1.3)

sphere_renderer.ResetCamera()
sphere_renderer.GetActiveCamera().Zoom(1.3)

# ---------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------
render_window_interactor.Initialize()
render_window_interactor.Start()
