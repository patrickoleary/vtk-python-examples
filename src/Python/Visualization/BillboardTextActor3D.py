#!/usr/bin/env python

# Place billboard text labels at random 3D positions next to sphere glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkBillboardTextActor3D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray = (0.184, 0.310, 0.310)
peacock = (0.200, 0.631, 0.788)
misty_rose = (1.000, 0.894, 0.882)
gold = (1.000, 0.843, 0.000)

# Random number generator with a fixed seed for reproducibility
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(5127)

# Source: generate sphere polygon data used for each glyph
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetRadius(1.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(dark_slate_gray)

# Origin marker: a sphere at (0, 0, 0)
origin_mapper = vtkPolyDataMapper()
origin_mapper.SetInputConnection(sphere_source.GetOutputPort())

origin_actor = vtkActor()
origin_actor.SetMapper(origin_mapper)
origin_actor.SetPosition(0.0, 0.0, 0.0)
origin_actor.GetProperty().SetColor(peacock)
renderer.AddActor(origin_actor)

# Place 10 labeled spheres at random positions
for i in range(10):
    px = rng.GetRangeValue(-10.0, 10.0)
    rng.Next()
    py = rng.GetRangeValue(-10.0, 10.0)
    rng.Next()
    pz = rng.GetRangeValue(-10.0, 10.0)
    rng.Next()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphere_source.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetPosition(px, py, pz)
    actor.GetProperty().SetColor(misty_rose)

    text_actor = vtkBillboardTextActor3D()
    text_actor.SetInput(f"{px:0.3g}, {py:0.3g}, {pz:0.3g}")
    text_actor.SetPosition(px, py, pz)
    text_actor.GetTextProperty().SetFontSize(12)
    text_actor.GetTextProperty().SetColor(gold)
    text_actor.GetTextProperty().SetJustificationToCentered()

    renderer.AddActor(actor)
    renderer.AddActor(text_actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("BillboardTextActor3D")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
