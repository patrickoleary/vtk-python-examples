#!/usr/bin/env python

# Demonstrate user shader replacements to color a dragon model by model-space normals.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkTriangleMeshPointNormals
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon with triangle mesh normals
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

norms = vtkTriangleMeshPointNormals()
norms.SetInputConnection(reader.GetOutputPort())
norms.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(norms.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.5)
actor.GetProperty().SetSpecularPower(20.0)
actor.GetProperty().SetOpacity(1.0)

# Shader replacements: pass model-space normal to fragment shader
# and use it to set diffuse color
sp = actor.GetShaderProperty()

# Vertex shader: declare and pass model-space normal
sp.AddVertexShaderReplacement(
    "//VTK::Normal::Dec", True,
    "//VTK::Normal::Dec\n"
    "  out vec3 myNormalMCVSOutput;\n",
    False,
)
sp.AddVertexShaderReplacement(
    "//VTK::Normal::Impl", True,
    "//VTK::Normal::Impl\n"
    "  myNormalMCVSOutput = normalMC;\n",
    False,
)

# Fragment shader: receive model-space normal and use as diffuse color
sp.AddFragmentShaderReplacement(
    "//VTK::Normal::Dec", True,
    "//VTK::Normal::Dec\n"
    "  in vec3 myNormalMCVSOutput;\n",
    False,
)
sp.AddFragmentShaderReplacement(
    "//VTK::Normal::Impl", True,
    "//VTK::Normal::Impl\n"
    "  diffuseColor = abs(myNormalMCVSOutput);\n",
    False,
)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("user shader")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
render_window.Render()
renderer.GetActiveCamera().SetPosition(-0.2, 0.4, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

interactor.Initialize()
interactor.Start()
