#!/usr/bin/env python

# Demonstrate cubemap reflection with skybox, scene light, and shader replacements on a bunny.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonMath import vtkMatrix3x3
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkImagingCore import vtkImageFlip
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

# Cubemap texture from skybox subdirectory
texture = vtkTexture()
texture.CubeMapOn()
texture.InterpolateOn()
texture.RepeatOff()
texture.EdgeClampOn()

# Face 0: +X
jpg_px = vtkJPEGReader()
jpg_px.SetFileName(os.path.join(data_dir, "skybox/posx.jpg"))
flip_px = vtkImageFlip()
flip_px.SetInputConnection(jpg_px.GetOutputPort())
flip_px.SetFilteredAxis(1)
texture.SetInputConnection(0, flip_px.GetOutputPort())

# Face 1: -X
jpg_nx = vtkJPEGReader()
jpg_nx.SetFileName(os.path.join(data_dir, "skybox/negx.jpg"))
flip_nx = vtkImageFlip()
flip_nx.SetInputConnection(jpg_nx.GetOutputPort())
flip_nx.SetFilteredAxis(1)
texture.SetInputConnection(1, flip_nx.GetOutputPort())

# Face 2: +Y
jpg_py = vtkJPEGReader()
jpg_py.SetFileName(os.path.join(data_dir, "skybox/posy.jpg"))
flip_py = vtkImageFlip()
flip_py.SetInputConnection(jpg_py.GetOutputPort())
flip_py.SetFilteredAxis(1)
texture.SetInputConnection(2, flip_py.GetOutputPort())

# Face 3: -Y
jpg_ny = vtkJPEGReader()
jpg_ny.SetFileName(os.path.join(data_dir, "skybox/negy.jpg"))
flip_ny = vtkImageFlip()
flip_ny.SetInputConnection(jpg_ny.GetOutputPort())
flip_ny.SetFilteredAxis(1)
texture.SetInputConnection(3, flip_ny.GetOutputPort())

# Face 4: +Z
jpg_pz = vtkJPEGReader()
jpg_pz.SetFileName(os.path.join(data_dir, "skybox/posz.jpg"))
flip_pz = vtkImageFlip()
flip_pz.SetInputConnection(jpg_pz.GetOutputPort())
flip_pz.SetFilteredAxis(1)
texture.SetInputConnection(4, flip_pz.GetOutputPort())

# Face 5: -Z
jpg_nz = vtkJPEGReader()
jpg_nz.SetFileName(os.path.join(data_dir, "skybox/negz.jpg"))
flip_nz = vtkImageFlip()
flip_nz.SetInputConnection(jpg_nz.GetOutputPort())
flip_nz.SetFilteredAxis(1)
texture.SetInputConnection(5, flip_nz.GetOutputPort())

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

# Shader replacements for cubemap reflection blending
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
    "  vec3 cubeColor = texture(actortexture, normalize(TexCoords)).xyz;\n"
    "//VTK::Light::Impl\n"
    "  gl_FragData[0] = vec4(ambientColor + diffuse + specular + specularColor*cubeColor, opacity);\n",
    False,
)

# Skybox
skybox = vtkSkybox()
skybox.SetTexture(texture)

# Environment rotation matrix (180 deg Y)
transform = vtkTransform()
transform.Identity()
transform.RotateY(-180)
mat4 = transform.GetMatrix()
rot_mat = vtkMatrix3x3()
rot_mat.SetElement(0, 0, mat4.GetElement(0, 0))
rot_mat.SetElement(0, 1, mat4.GetElement(0, 1))
rot_mat.SetElement(0, 2, mat4.GetElement(0, 2))
rot_mat.SetElement(1, 0, mat4.GetElement(1, 0))
rot_mat.SetElement(1, 1, mat4.GetElement(1, 1))
rot_mat.SetElement(1, 2, mat4.GetElement(1, 2))
rot_mat.SetElement(2, 0, mat4.GetElement(2, 0))
rot_mat.SetElement(2, 1, mat4.GetElement(2, 1))
rot_mat.SetElement(2, 2, mat4.GetElement(2, 2))

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)
renderer.AddActor(skybox)
renderer.SetEnvironmentRotationMatrix(rot_mat)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cube map reflection bunny")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)
renderer.GetActiveCamera().SetPosition(0.0, 0.55, 2.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.55, 0.0)
renderer.GetActiveCamera().SetViewAngle(60.0)
renderer.GetActiveCamera().Zoom(1.1)
renderer.GetActiveCamera().Elevation(5)
renderer.GetActiveCamera().Roll(-10)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
