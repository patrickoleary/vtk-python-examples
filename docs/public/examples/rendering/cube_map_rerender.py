#!/usr/bin/env python

# Demonstrate cubemap re-rendering after adding shader replacements mid-pipeline.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkImagingCore import vtkImageFlip
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Cubemap texture
texture = vtkTexture()
texture.CubeMapOn()

# Face 0: +X
jpg_px = vtkJPEGReader()
jpg_px.SetFileName(os.path.join(data_dir, "skybox-px.jpg"))
flip_px = vtkImageFlip()
flip_px.SetInputConnection(jpg_px.GetOutputPort())
flip_px.SetFilteredAxis(1)
texture.SetInputConnection(0, flip_px.GetOutputPort())

# Face 1: -X
jpg_nx = vtkJPEGReader()
jpg_nx.SetFileName(os.path.join(data_dir, "skybox-nx.jpg"))
flip_nx = vtkImageFlip()
flip_nx.SetInputConnection(jpg_nx.GetOutputPort())
flip_nx.SetFilteredAxis(1)
texture.SetInputConnection(1, flip_nx.GetOutputPort())

# Face 2: +Y
jpg_py = vtkJPEGReader()
jpg_py.SetFileName(os.path.join(data_dir, "skybox-py.jpg"))
flip_py = vtkImageFlip()
flip_py.SetInputConnection(jpg_py.GetOutputPort())
flip_py.SetFilteredAxis(1)
texture.SetInputConnection(2, flip_py.GetOutputPort())

# Face 3: -Y
jpg_ny = vtkJPEGReader()
jpg_ny.SetFileName(os.path.join(data_dir, "skybox-ny.jpg"))
flip_ny = vtkImageFlip()
flip_ny.SetInputConnection(jpg_ny.GetOutputPort())
flip_ny.SetFilteredAxis(1)
texture.SetInputConnection(3, flip_ny.GetOutputPort())

# Face 4: +Z
jpg_pz = vtkJPEGReader()
jpg_pz.SetFileName(os.path.join(data_dir, "skybox-pz.jpg"))
flip_pz = vtkImageFlip()
flip_pz.SetInputConnection(jpg_pz.GetOutputPort())
flip_pz.SetFilteredAxis(1)
texture.SetInputConnection(4, flip_pz.GetOutputPort())

# Face 5: -Z
jpg_nz = vtkJPEGReader()
jpg_nz.SetFileName(os.path.join(data_dir, "skybox-nz.jpg"))
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
actor.SetTexture(texture)
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cube map rerender")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)

# First render without shader replacements (pipeline exception)
render_window.Render()

# Add shader replacements for cubemap reflection
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
sp.SetFragmentShaderCode(
    "//VTK::System::Dec\n"
    "//VTK::Output::Dec\n"
    "in vec3 TexCoords;\n"
    "uniform samplerCube texture_0;\n"
    "void main () {\n"
    "  gl_FragData[0] = texture(texture_0, TexCoords);\n"
    "}\n"
)

# Re-render with shader replacements (pipeline exception)
render_window.Render()

interactor.Initialize()
interactor.Start()
