#!/usr/bin/env python

# Demonstrate sphere-mapped environment reflection on a bunny using shader replacements and skybox.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Scene light
light = vtkLight()
light.SetLightTypeToSceneLight()
light.SetPosition(1.0, 7.0, 1.0)

# Sphere map texture (2D)
texture = vtkTexture()
texture.InterpolateOn()

img_reader = vtkJPEGReader()
img_reader.SetFileName(os.path.join(data_dir, "wintersun.jpg"))
texture.SetInputConnection(img_reader.GetOutputPort())

# Bunny with normals
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "bunny.ply"))

norms = vtkPolyDataNormals()
norms.SetInputConnection(reader.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(norms.GetOutputPort())

actor = vtkActor()
actor.SetScale(6.0, 6.0, 6.0)
actor.GetProperty().SetSpecular(0.8)
actor.GetProperty().SetSpecularPower(20)
actor.GetProperty().SetDiffuse(0.1)
actor.GetProperty().SetAmbient(0.1)
actor.GetProperty().SetDiffuseColor(1.0, 0.0, 0.4)
actor.GetProperty().SetAmbientColor(0.4, 0.0, 1.0)
actor.SetTexture(texture)
actor.SetMapper(mapper)

# Shader replacements for sphere-mapped environment reflection
sp = actor.GetShaderProperty()
sp.AddVertexShaderReplacement(
    "//VTK::PositionVC::Dec", True,
    "//VTK::PositionVC::Dec\n"
    "out vec3 TexCoords;\n",
    False,
)
sp.AddVertexShaderReplacement(
    "//VTK::PositionVC::Impl", True,
    "//VTK::PositionVC::Impl\n"
    "vec3 camPos = -MCVCMatrix[3].xyz * mat3(MCVCMatrix);\n"
    "TexCoords.xyz = reflect(vertexMC.xyz - camPos, normalize(normalMC));\n",
    False,
)
sp.AddFragmentShaderReplacement(
    "//VTK::Light::Dec", True,
    "//VTK::Light::Dec\n"
    "in vec3 TexCoords;\n",
    False,
)
sp.AddFragmentShaderReplacement(
    "//VTK::Light::Impl", True,
    "//VTK::Light::Impl\n"
    "  float phix = length(vec2(TexCoords.x, TexCoords.z));\n"
    "  vec3 skyColor = texture(actortexture, vec2(0.5*atan(TexCoords.z, TexCoords.x)/3.1415927 + 0.5, atan(TexCoords.y,phix)/3.1415927 + 0.5)).xyz;\n"
    "  gl_FragData[0] = vec4(ambientColor + diffuse + specular + specularColor*skyColor, opacity);\n",
    False,
)

# Skybox with sphere projection
skybox = vtkSkybox()
skybox.SetProjectionToSphere()
skybox.SetTexture(texture)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)
renderer.AddActor(skybox)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("sphere map")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)
renderer.GetActiveCamera().SetPosition(0.0, 0.55, 2.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.55, 0.0)
renderer.GetActiveCamera().SetViewAngle(60.0)
renderer.GetActiveCamera().Zoom(1.1)
renderer.GetActiveCamera().Elevation(5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
