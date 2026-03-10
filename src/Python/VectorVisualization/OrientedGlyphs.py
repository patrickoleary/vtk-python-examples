#!/usr/bin/env python

# Place arrow glyphs oriented by surface normals on a sphere.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold = (1.000, 0.843, 0.000)
dark_green = (0.000, 0.392, 0.000)

# Source: generate a sphere with point normals
sphere = vtkSphereSource()
sphere.Update()

# Source: arrow geometry for the glyphs
arrow = vtkArrowSource()

# Filter: place arrows oriented along surface normals
glyph = vtkGlyph3D()
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetInputData(sphere.GetOutput())
glyph.SetScaleFactor(0.2)
glyph.Update()

# Mapper: map glyph data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_green)
renderer.GetActiveCamera().SetPosition(-0.399941, -1.070475, 2.931458)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.GetActiveCamera().SetViewUp(-0.028450, 0.940195, 0.339448)
renderer.GetActiveCamera().SetDistance(3.146318)
renderer.GetActiveCamera().SetClippingRange(1.182293, 5.626211)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("OrientedGlyphs")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
