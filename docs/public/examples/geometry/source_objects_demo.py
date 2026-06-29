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
# Viewport grid: 3 columns × 3 rows
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 3

# Shared back-face property
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(21)
sphere_source.SetThetaResolution(21)

cone_source = vtkConeSource()
cone_source.SetResolution(51)

cylinder_source = vtkCylinderSource()
cylinder_source.SetResolution(51)

cube_source = vtkCubeSource()

plane_source = vtkPlaneSource()

text_source = vtkTextSource()
text_source.SetText("Hello")
text_source.BackingOff()

point_source = vtkPointSource()
point_source.SetNumberOfPoints(500)

disk_source = vtkDiskSource()
disk_source.SetCircumferentialResolution(51)

line_source = vtkLineSource()

# ---------------------------------------------------------------------------
# Mappers + Actors
# ---------------------------------------------------------------------------
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(peach_puff_rgb)
sphere_actor.SetBackfaceProperty(back_property)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(peach_puff_rgb)
cone_actor.SetBackfaceProperty(back_property)

cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(peach_puff_rgb)
cylinder_actor.SetBackfaceProperty(back_property)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(peach_puff_rgb)
cube_actor.SetBackfaceProperty(back_property)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane_source.GetOutputPort())
plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(peach_puff_rgb)
plane_actor.SetBackfaceProperty(back_property)

text_mapper = vtkPolyDataMapper()
text_mapper.SetInputConnection(text_source.GetOutputPort())
text_actor = vtkActor()
text_actor.SetMapper(text_mapper)
text_actor.GetProperty().SetColor(peach_puff_rgb)
text_actor.SetBackfaceProperty(back_property)

point_mapper = vtkPolyDataMapper()
point_mapper.SetInputConnection(point_source.GetOutputPort())
point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetColor(peach_puff_rgb)
point_actor.SetBackfaceProperty(back_property)

disk_mapper = vtkPolyDataMapper()
disk_mapper.SetInputConnection(disk_source.GetOutputPort())
disk_actor = vtkActor()
disk_actor.SetMapper(disk_mapper)
disk_actor.GetProperty().SetColor(peach_puff_rgb)
disk_actor.SetBackfaceProperty(back_property)

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(line_source.GetOutputPort())
line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(peach_puff_rgb)
line_actor.SetBackfaceProperty(back_property)

# ---------------------------------------------------------------------------
# Text actors (labels)
# ---------------------------------------------------------------------------
sphere_text = vtkTextActor()
sphere_text.SetInput("Sphere")
sphere_text.GetTextProperty().SetFontSize(14)
sphere_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
sphere_text.GetTextProperty().SetJustificationToCentered()
sphere_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
sphere_text.SetPosition(0.5, 0.01)

cone_text = vtkTextActor()
cone_text.SetInput("Cone")
cone_text.GetTextProperty().SetFontSize(14)
cone_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
cone_text.GetTextProperty().SetJustificationToCentered()
cone_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cone_text.SetPosition(0.5, 0.01)

cylinder_text = vtkTextActor()
cylinder_text.SetInput("Cylinder")
cylinder_text.GetTextProperty().SetFontSize(14)
cylinder_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
cylinder_text.GetTextProperty().SetJustificationToCentered()
cylinder_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cylinder_text.SetPosition(0.5, 0.01)

cube_text = vtkTextActor()
cube_text.SetInput("Cube")
cube_text.GetTextProperty().SetFontSize(14)
cube_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
cube_text.GetTextProperty().SetJustificationToCentered()
cube_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cube_text.SetPosition(0.5, 0.01)

plane_text = vtkTextActor()
plane_text.SetInput("Plane")
plane_text.GetTextProperty().SetFontSize(14)
plane_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
plane_text.GetTextProperty().SetJustificationToCentered()
plane_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
plane_text.SetPosition(0.5, 0.01)

text_label = vtkTextActor()
text_label.SetInput("Text")
text_label.GetTextProperty().SetFontSize(14)
text_label.GetTextProperty().SetColor(1.0, 1.0, 1.0)
text_label.GetTextProperty().SetJustificationToCentered()
text_label.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
text_label.SetPosition(0.5, 0.01)

point_text = vtkTextActor()
point_text.SetInput("PointSource")
point_text.GetTextProperty().SetFontSize(14)
point_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
point_text.GetTextProperty().SetJustificationToCentered()
point_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
point_text.SetPosition(0.5, 0.01)

disk_text = vtkTextActor()
disk_text.SetInput("Disk")
disk_text.GetTextProperty().SetFontSize(14)
disk_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
disk_text.GetTextProperty().SetJustificationToCentered()
disk_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
disk_text.SetPosition(0.5, 0.01)

line_text = vtkTextActor()
line_text.SetInput("Line")
line_text.GetTextProperty().SetFontSize(14)
line_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
line_text.GetTextProperty().SetJustificationToCentered()
line_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
line_text.SetPosition(0.5, 0.01)

# ---------------------------------------------------------------------------
# Renderers (row 2 = top, row 0 = bottom; left to right)
# ---------------------------------------------------------------------------
sphere_renderer = vtkRenderer()
sphere_renderer.AddActor(sphere_actor)
sphere_renderer.AddViewProp(sphere_text)
sphere_renderer.SetBackground(background_rgb)
sphere_renderer.SetViewport(0 / num_cols, 2 / num_rows, 1 / num_cols, 3 / num_rows)

cone_renderer = vtkRenderer()
cone_renderer.AddActor(cone_actor)
cone_renderer.AddViewProp(cone_text)
cone_renderer.SetBackground(background_rgb)
cone_renderer.SetViewport(1 / num_cols, 2 / num_rows, 2 / num_cols, 3 / num_rows)

cylinder_renderer = vtkRenderer()
cylinder_renderer.AddActor(cylinder_actor)
cylinder_renderer.AddViewProp(cylinder_text)
cylinder_renderer.SetBackground(background_rgb)
cylinder_renderer.SetViewport(2 / num_cols, 2 / num_rows, 3 / num_cols, 3 / num_rows)

cube_renderer = vtkRenderer()
cube_renderer.AddActor(cube_actor)
cube_renderer.AddViewProp(cube_text)
cube_renderer.SetBackground(background_rgb)
cube_renderer.SetViewport(0 / num_cols, 1 / num_rows, 1 / num_cols, 2 / num_rows)

plane_renderer = vtkRenderer()
plane_renderer.AddActor(plane_actor)
plane_renderer.AddViewProp(plane_text)
plane_renderer.SetBackground(background_rgb)
plane_renderer.SetViewport(1 / num_cols, 1 / num_rows, 2 / num_cols, 2 / num_rows)

text_renderer = vtkRenderer()
text_renderer.AddActor(text_actor)
text_renderer.AddViewProp(text_label)
text_renderer.SetBackground(background_rgb)
text_renderer.SetViewport(2 / num_cols, 1 / num_rows, 3 / num_cols, 2 / num_rows)

point_renderer = vtkRenderer()
point_renderer.AddActor(point_actor)
point_renderer.AddViewProp(point_text)
point_renderer.SetBackground(background_rgb)
point_renderer.SetViewport(0 / num_cols, 0 / num_rows, 1 / num_cols, 1 / num_rows)

disk_renderer = vtkRenderer()
disk_renderer.AddActor(disk_actor)
disk_renderer.AddViewProp(disk_text)
disk_renderer.SetBackground(background_rgb)
disk_renderer.SetViewport(1 / num_cols, 0 / num_rows, 2 / num_cols, 1 / num_rows)

line_renderer = vtkRenderer()
line_renderer.AddActor(line_actor)
line_renderer.AddViewProp(line_text)
line_renderer.SetBackground(background_rgb)
line_renderer.SetViewport(2 / num_cols, 0 / num_rows, 3 / num_cols, 1 / num_rows)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(sphere_renderer)
render_window.AddRenderer(cone_renderer)
render_window.AddRenderer(cylinder_renderer)
render_window.AddRenderer(cube_renderer)
render_window.AddRenderer(plane_renderer)
render_window.AddRenderer(text_renderer)
render_window.AddRenderer(point_renderer)
render_window.AddRenderer(disk_renderer)
render_window.AddRenderer(line_renderer)
render_window.SetWindowName("source objects demo")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 640)

# Interactor
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure cameras
sphere_renderer.ResetCamera()
sphere_renderer.GetActiveCamera().Zoom(1.3)
cone_renderer.ResetCamera()
cone_renderer.GetActiveCamera().Zoom(1.3)
cylinder_renderer.ResetCamera()
cylinder_renderer.GetActiveCamera().Zoom(1.3)
cube_renderer.ResetCamera()
cube_renderer.GetActiveCamera().Zoom(1.3)
plane_renderer.ResetCamera()
plane_renderer.GetActiveCamera().Zoom(1.3)
text_renderer.ResetCamera()
text_renderer.GetActiveCamera().Zoom(1.3)
point_renderer.ResetCamera()
point_renderer.GetActiveCamera().Zoom(1.3)
disk_renderer.ResetCamera()
disk_renderer.GetActiveCamera().Zoom(1.3)
line_renderer.ResetCamera()
line_renderer.GetActiveCamera().Zoom(1.3)

render_window_interactor.Initialize()
render_window_interactor.Start()
