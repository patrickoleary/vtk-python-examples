#!/usr/bin/env python

# Highlight an arrow with a glowing outline using vtkOutlineGlowPass on a
# layered renderer on top of the main scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkOutlineGlowPass,
    vtkRenderStepsPass,
)

# Colors (normalized RGB)
lime_green = (0.196, 0.804, 0.196)
magenta = (1.0, 0.0, 1.0)
dark_slate_gray = (0.184, 0.310, 0.310)
dark_slate_blue = (0.282, 0.239, 0.545)

# Source: generate an arrow
arrow = vtkArrowSource()
arrow.Update()

# ---------- main layer (layer 0): the lit arrow ----------
main_mapper = vtkPolyDataMapper()
main_mapper.SetInputConnection(arrow.GetOutputPort())

main_actor = vtkActor()
main_actor.SetMapper(main_mapper)
main_actor.GetProperty().SetDiffuseColor(lime_green)

renderer = vtkRenderer()
renderer.AddActor(main_actor)
renderer.GradientBackgroundOn()
renderer.SetBackground(dark_slate_gray)
renderer.SetBackground2(dark_slate_blue)

# ---------- outline layer (layer 1): bright unlit silhouette ----------
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(arrow.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(magenta)
outline_actor.GetProperty().LightingOff()

# Render pass: outline glow applied to the highlight renderer
basic_passes = vtkRenderStepsPass()
glow_pass = vtkOutlineGlowPass()
glow_pass.SetDelegatePass(basic_passes)

renderer_outline = vtkRenderer()
renderer_outline.AddActor(outline_actor)
renderer_outline.SetLayer(1)
renderer_outline.SetPass(glow_pass)

# Camera: share the main camera with the outline layer
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Roll(45.0)
camera.Azimuth(-30.0)
camera.Elevation(-15.0)
renderer.ResetCamera()
renderer_outline.SetActiveCamera(camera)

# Window: display the rendered scene (disable multisampling for render passes)
render_window = vtkRenderWindow()
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer)
render_window.AddRenderer(renderer_outline)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("OutlineGlowPass")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
