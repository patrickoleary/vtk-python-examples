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
# Viewport grid: 3 columns × 2 rows (6 slots, 5 used + 1 empty)
# ---------------------------------------------------------------------------
num_cols = 3
num_rows = 2

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
tetrahedron_source = vtkPlatonicSolidSource()
tetrahedron_source.SetSolidType(0)

cube_source = vtkPlatonicSolidSource()
cube_source.SetSolidType(1)

octahedron_source = vtkPlatonicSolidSource()
octahedron_source.SetSolidType(2)

icosahedron_source = vtkPlatonicSolidSource()
icosahedron_source.SetSolidType(3)

dodecahedron_source = vtkPlatonicSolidSource()
dodecahedron_source.SetSolidType(4)

# ---------------------------------------------------------------------------
# Mappers + Actors
# ---------------------------------------------------------------------------
tetrahedron_mapper = vtkPolyDataMapper()
tetrahedron_mapper.SetInputConnection(tetrahedron_source.GetOutputPort())
tetrahedron_mapper.SetLookupTable(lut)
tetrahedron_mapper.SetScalarRange(0, 19)
tetrahedron_actor = vtkActor()
tetrahedron_actor.SetMapper(tetrahedron_mapper)
tetrahedron_actor.RotateX(30)
tetrahedron_actor.RotateY(30)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())
cube_mapper.SetLookupTable(lut)
cube_mapper.SetScalarRange(0, 19)
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.RotateX(20)
cube_actor.RotateY(-30)

octahedron_mapper = vtkPolyDataMapper()
octahedron_mapper.SetInputConnection(octahedron_source.GetOutputPort())
octahedron_mapper.SetLookupTable(lut)
octahedron_mapper.SetScalarRange(0, 19)
octahedron_actor = vtkActor()
octahedron_actor.SetMapper(octahedron_mapper)
octahedron_actor.RotateX(25)
octahedron_actor.RotateY(20)

icosahedron_mapper = vtkPolyDataMapper()
icosahedron_mapper.SetInputConnection(icosahedron_source.GetOutputPort())
icosahedron_mapper.SetLookupTable(lut)
icosahedron_mapper.SetScalarRange(0, 19)
icosahedron_actor = vtkActor()
icosahedron_actor.SetMapper(icosahedron_mapper)
icosahedron_actor.RotateX(15)
icosahedron_actor.RotateY(-20)

dodecahedron_mapper = vtkPolyDataMapper()
dodecahedron_mapper.SetInputConnection(dodecahedron_source.GetOutputPort())
dodecahedron_mapper.SetLookupTable(lut)
dodecahedron_mapper.SetScalarRange(0, 19)
dodecahedron_actor = vtkActor()
dodecahedron_actor.SetMapper(dodecahedron_mapper)
dodecahedron_actor.RotateX(20)
dodecahedron_actor.RotateY(30)

# ---------------------------------------------------------------------------
# Text actors
# ---------------------------------------------------------------------------
tetrahedron_text = vtkTextActor()
tetrahedron_text.SetInput("Tetrahedron")
tetrahedron_text.GetTextProperty().SetFontSize(14)
tetrahedron_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
tetrahedron_text.GetTextProperty().SetJustificationToCentered()
tetrahedron_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
tetrahedron_text.SetPosition(0.5, 0.01)

cube_text = vtkTextActor()
cube_text.SetInput("Cube")
cube_text.GetTextProperty().SetFontSize(14)
cube_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
cube_text.GetTextProperty().SetJustificationToCentered()
cube_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
cube_text.SetPosition(0.5, 0.01)

octahedron_text = vtkTextActor()
octahedron_text.SetInput("Octahedron")
octahedron_text.GetTextProperty().SetFontSize(14)
octahedron_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
octahedron_text.GetTextProperty().SetJustificationToCentered()
octahedron_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
octahedron_text.SetPosition(0.5, 0.01)

icosahedron_text = vtkTextActor()
icosahedron_text.SetInput("Icosahedron")
icosahedron_text.GetTextProperty().SetFontSize(14)
icosahedron_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
icosahedron_text.GetTextProperty().SetJustificationToCentered()
icosahedron_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
icosahedron_text.SetPosition(0.5, 0.01)

dodecahedron_text = vtkTextActor()
dodecahedron_text.SetInput("Dodecahedron")
dodecahedron_text.GetTextProperty().SetFontSize(14)
dodecahedron_text.GetTextProperty().SetColor(1.0, 1.0, 1.0)
dodecahedron_text.GetTextProperty().SetJustificationToCentered()
dodecahedron_text.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
dodecahedron_text.SetPosition(0.5, 0.01)

# ---------------------------------------------------------------------------
# Renderers (row 1 = top, row 0 = bottom; left to right)
# ---------------------------------------------------------------------------
tetrahedron_renderer = vtkRenderer()
tetrahedron_renderer.AddActor(tetrahedron_actor)
tetrahedron_renderer.AddViewProp(tetrahedron_text)
tetrahedron_renderer.SetBackground(slate_gray_background_rgb)
tetrahedron_renderer.SetViewport(0 / num_cols, 1 / num_rows, 1 / num_cols, 2 / num_rows)

cube_renderer = vtkRenderer()
cube_renderer.AddActor(cube_actor)
cube_renderer.AddViewProp(cube_text)
cube_renderer.SetBackground(slate_gray_background_rgb)
cube_renderer.SetViewport(1 / num_cols, 1 / num_rows, 2 / num_cols, 2 / num_rows)

octahedron_renderer = vtkRenderer()
octahedron_renderer.AddActor(octahedron_actor)
octahedron_renderer.AddViewProp(octahedron_text)
octahedron_renderer.SetBackground(slate_gray_background_rgb)
octahedron_renderer.SetViewport(2 / num_cols, 1 / num_rows, 3 / num_cols, 2 / num_rows)

icosahedron_renderer = vtkRenderer()
icosahedron_renderer.AddActor(icosahedron_actor)
icosahedron_renderer.AddViewProp(icosahedron_text)
icosahedron_renderer.SetBackground(slate_gray_background_rgb)
icosahedron_renderer.SetViewport(0 / num_cols, 0 / num_rows, 1 / num_cols, 1 / num_rows)

dodecahedron_renderer = vtkRenderer()
dodecahedron_renderer.AddActor(dodecahedron_actor)
dodecahedron_renderer.AddViewProp(dodecahedron_text)
dodecahedron_renderer.SetBackground(slate_gray_background_rgb)
dodecahedron_renderer.SetViewport(1 / num_cols, 0 / num_rows, 2 / num_cols, 1 / num_rows)

empty_renderer = vtkRenderer()
empty_renderer.SetBackground(slate_gray_background_rgb)
empty_renderer.SetViewport(2 / num_cols, 0 / num_rows, 3 / num_cols, 1 / num_rows)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(tetrahedron_renderer)
render_window.AddRenderer(cube_renderer)
render_window.AddRenderer(octahedron_renderer)
render_window.AddRenderer(icosahedron_renderer)
render_window.AddRenderer(dodecahedron_renderer)
render_window.AddRenderer(empty_renderer)
render_window.SetWindowName("platonic solids demo")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 600)

# Interactor
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure cameras
tetrahedron_renderer.ResetCamera()
tetrahedron_renderer.GetActiveCamera().Zoom(1.4)
cube_renderer.ResetCamera()
cube_renderer.GetActiveCamera().Zoom(1.4)
octahedron_renderer.ResetCamera()
octahedron_renderer.GetActiveCamera().Zoom(1.4)
icosahedron_renderer.ResetCamera()
icosahedron_renderer.GetActiveCamera().Zoom(1.4)
dodecahedron_renderer.ResetCamera()
dodecahedron_renderer.GetActiveCamera().Zoom(1.4)

render_window_interactor.Initialize()
render_window_interactor.Start()
