#!/usr/bin/env python

# Demonstrate hardcoded user vertex and fragment shaders with a custom uniform on a dragon model.

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

# Hardcoded vertex shader: distort vertex positions
sp = actor.GetShaderProperty()
sp.SetVertexShaderCode(
    "//VTK::System::Dec\n"
    "in vec4 vertexMC;\n"
    "//VTK::Normal::Dec\n"
    "uniform mat4 MCDCMatrix;\n"
    "void main () {\n"
    "  normalVCVSOutput = normalMatrix * normalMC;\n"
    "  vec4 tmpPos = MCDCMatrix * vertexMC;\n"
    "  gl_Position = tmpPos*vec4(0.2+0.8*abs(tmpPos.x),0.2+0.8*abs(tmpPos.y),1.0,1.0);\n"
    "}\n"
)

# Hardcoded fragment shader: use custom diffuse color uniform
sp.SetFragmentShaderCode(
    "//VTK::System::Dec\n"
    "//VTK::Output::Dec\n"
    "in vec3 normalVCVSOutput;\n"
    "uniform vec3 diffuseColorUniform;\n"
    "void main () {\n"
    "  float df = max(0.0, normalVCVSOutput.z);\n"
    "  float sf = pow(df, 20.0);\n"
    "  vec3 diffuse = df * diffuseColorUniform;\n"
    "  vec3 specular = sf * vec3(0.4,0.4,0.4);\n"
    "  gl_FragData[0] = vec4(0.3*abs(normalVCVSOutput) + 0.7*diffuse + specular, 1.0);\n"
    "}\n"
)

# Set the custom uniform via the shader property
sp.GetFragmentCustomUniforms().SetUniform3f("diffuseColorUniform", [0.4, 0.7, 0.6])

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.GradientBackgroundOn()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("user shader dragon")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
render_window.Render()
renderer.GetActiveCamera().SetPosition(-0.2, 0.4, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

interactor.Initialize()
interactor.Start()
