#!/usr/bin/env python

# Demonstrate PBR color multiplier with a base color texture on a cube.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Cube source
cube = vtkCubeSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cube.GetOutputPort())

# Albedo texture
albedo_reader = vtkPNGReader()
albedo_reader.SetFileName(os.path.join(data_dir, "vtk_Base_Color.png"))
albedo = vtkTexture()
albedo.UseSRGBColorSpaceOn()
albedo.InterpolateOn()
albedo.SetInputConnection(albedo_reader.GetOutputPort())

# PBR actor with color multiplier
actor = vtkActor()
actor.SetOrientation(0.0, 25.0, 0.0)
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToPBR()
actor.GetProperty().SetColor(1.0, 1.0, 0.0)
actor.GetProperty().SetOpacity(0.5)
actor.GetProperty().SetBaseColorTexture(albedo)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr color multiplier")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
# Pipeline exception: render needed before camera zoom for PBR
render_window.Render()
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
