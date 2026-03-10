#!/usr/bin/env python

# Render a sphere, capture the render window to a PostScript image
# file using vtkPostScriptWriter, then display the rendered scene.

import os
import tempfile

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkPostScriptWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter,
)

# Colors (normalized RGB)
light_steel_blue_rgb = (0.690, 0.769, 0.871)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# Output path: write to a temporary file
ps_path = os.path.join(tempfile.gettempdir(), "WriteImagePostScript.ps")

# Source: generate a sphere
source = vtkSphereSource()
source.SetCenter(0, 0, 0)
source.SetRadius(5.0)
source.SetPhiResolution(30)
source.SetThetaResolution(30)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(light_steel_blue_rgb)
actor.SetBackfaceProperty(back_property)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("WriteImagePostScript")
render_window.Render()

# Writer: capture the render window to a PostScript file
window_to_image = vtkWindowToImageFilter()
window_to_image.SetInput(render_window)
window_to_image.SetInputBufferTypeToRGB()
window_to_image.ReadFrontBufferOff()
window_to_image.Update()

writer = vtkPostScriptWriter()
writer.SetFileName(ps_path)
writer.SetInputConnection(window_to_image.GetOutputPort())
writer.Write()
print(f"Wrote: {ps_path}")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
