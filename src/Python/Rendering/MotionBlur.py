#!/usr/bin/env python

# Demonstrate motion blur using vtkSimpleMotionBlurPass on the Armadillo
# mesh rendered with three different material properties.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkRenderStepsPass,
    vtkSimpleMotionBlurPass,
)

# Colors (normalized RGB)
a1_ambient = (1.0, 0.0, 0.0)
a1_diffuse = (1.0, 0.800, 0.302)
a2_ambient = (0.200, 0.200, 1.0)
a2_diffuse = (0.200, 1.0, 0.800)
a3_diffuse = (0.502, 0.651, 1.0)
white = (1.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0)
background = (0.302, 0.400, 0.600)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the Armadillo mesh
reader = vtkPLYReader()
reader.SetFileName(str(data_dir / "Armadillo.ply"))

# Mapper: map the mesh polygon data
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor 1: warm tones, offset position
actor1 = vtkActor()
actor1.SetMapper(mapper)
actor1.GetProperty().SetAmbientColor(a1_ambient)
actor1.GetProperty().SetDiffuseColor(a1_diffuse)
actor1.GetProperty().SetSpecular(0.0)
actor1.GetProperty().SetDiffuse(0.5)
actor1.GetProperty().SetAmbient(0.3)
actor1.SetPosition(-0.1, 0.0, -0.1)

# Actor 2: cool tones, centred
actor2 = vtkActor()
actor2.SetMapper(mapper)
actor2.GetProperty().SetAmbientColor(a2_ambient)
actor2.GetProperty().SetDiffuseColor(a2_diffuse)
actor2.GetProperty().SetSpecularColor(black)
actor2.GetProperty().SetSpecular(0.2)
actor2.GetProperty().SetDiffuse(0.9)
actor2.GetProperty().SetAmbient(0.1)
actor2.GetProperty().SetSpecularPower(10.0)

# Actor 3: bright specular highlights, offset position
actor3 = vtkActor()
actor3.SetMapper(mapper)
actor3.GetProperty().SetDiffuseColor(a3_diffuse)
actor3.GetProperty().SetSpecularColor(white)
actor3.GetProperty().SetSpecular(0.7)
actor3.GetProperty().SetDiffuse(0.4)
actor3.GetProperty().SetSpecularPower(60.0)
actor3.SetPosition(0.1, 0.0, 0.1)

# Render pass: motion blur pipeline
basic_passes = vtkRenderStepsPass()
motion = vtkSimpleMotionBlurPass()
motion.SetDelegatePass(basic_passes)

# Renderer: assemble the scene with the motion blur pass
renderer = vtkRenderer()
renderer.AddActor(actor1)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
renderer.SetBackground(background)
renderer.SetPass(motion)

# Window: display the rendered scene (disable multisampling for render passes)
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("MotionBlur")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Camera: position and perform 30 incremental rotations to accumulate blur
renderer.GetActiveCamera().SetPosition(0, 0, -1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(15.0)
renderer.GetActiveCamera().Zoom(1.2)
render_window.Render()

for _ in range(30):
    renderer.GetActiveCamera().Azimuth(10.0 / 30)
    renderer.GetActiveCamera().Elevation(10.0 / 30)
    render_window.Render()

# Launch the interactive visualization
interactor.Start()
