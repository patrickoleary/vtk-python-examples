#!/usr/bin/env python

# Demonstrate vtkSuperquadricSource with toroidal mode, textured with
# an earth PPM image, rendered with the standard VTK pipeline.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Superquadric source
superquadric = vtkSuperquadricSource()
superquadric.SetPhiResolution(20)
superquadric.SetThetaResolution(25)
superquadric.SetPhiRoundness(1.0)
superquadric.SetThetaRoundness(0.7)
superquadric.SetToroidal(1)
superquadric.SetThickness(0.3)
superquadric.SetScale(1, 1, 1)

# Texture from earth PPM
pnm_reader = vtkPNMReader()
pnm_reader.SetFileName(os.path.join(data_dir, "earth.ppm"))

texture = vtkTexture()
texture.SetInputConnection(pnm_reader.GetOutputPort())
texture.InterpolateOn()

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(superquadric.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)
actor.GetProperty().SetDiffuseColor(0.5, 0.8, 0.8)
actor.GetProperty().SetAmbient(0.2)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.25, 0.2, 0.2)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(550, 450)
render_window.SetWindowName("squad viewer")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.2)
renderer.GetActiveCamera().Elevation(40)
renderer.GetActiveCamera().Azimuth(-20)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
