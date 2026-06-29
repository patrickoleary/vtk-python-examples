#!/usr/bin/env python

# Read BYU motor parts with texture coordinates and implicit texture mapping.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataNormals,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersTexture import vtkImplicitTextureCoords
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
named_colors = vtkNamedColors()

# Cutting planes
cutting_planes = vtkPlanes()
plane_points = vtkPoints()
plane_normals = vtkFloatArray()
plane_normals.SetNumberOfComponents(3)
plane_points.InsertPoint(0, 0.0, 0.0, 0.0)
plane_normals.InsertTuple3(0, 0.0, 0.0, 1.0)
plane_points.InsertPoint(1, 0.0, 0.0, 0.0)
plane_normals.InsertTuple3(1, -1.0, 0.0, 0.0)
cutting_planes.SetPoints(plane_points)
cutting_planes.SetNormals(plane_normals)

# Texture
texture_reader = vtkStructuredPointsReader()
texture_reader.SetFileName(os.path.join(data_dir, "texThres2.vtk"))
motor_texture = vtkTexture()
motor_texture.SetInputConnection(texture_reader.GetOutputPort())
motor_texture.InterpolateOff()
motor_texture.RepeatOff()

# Source - Part 1 (cold_grey, visible)
part1_reader = vtkBYUReader()
part1_reader.SetGeometryFileName(os.path.join(data_dir, "motor.g"))
part1_reader.SetPartNumber(1)

part1_normals = vtkPolyDataNormals()
part1_normals.SetInputConnection(part1_reader.GetOutputPort())

part1_tex_coords = vtkImplicitTextureCoords()
part1_tex_coords.SetInputConnection(part1_normals.GetOutputPort())
part1_tex_coords.SetRFunction(cutting_planes)

part1_mapper = vtkDataSetMapper()
part1_mapper.SetInputConnection(part1_tex_coords.GetOutputPort())

part1_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("cold_grey", part1_rgb)

part1_actor = vtkActor()
part1_actor.SetMapper(part1_mapper)
part1_actor.SetTexture(motor_texture)
part1_actor.GetProperty().SetColor(part1_rgb)

# Source - Part 2 (peacock, visible)
part2_reader = vtkBYUReader()
part2_reader.SetGeometryFileName(os.path.join(data_dir, "motor.g"))
part2_reader.SetPartNumber(2)

part2_normals = vtkPolyDataNormals()
part2_normals.SetInputConnection(part2_reader.GetOutputPort())

part2_tex_coords = vtkImplicitTextureCoords()
part2_tex_coords.SetInputConnection(part2_normals.GetOutputPort())
part2_tex_coords.SetRFunction(cutting_planes)

part2_mapper = vtkDataSetMapper()
part2_mapper.SetInputConnection(part2_tex_coords.GetOutputPort())

part2_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("peacock", part2_rgb)

part2_actor = vtkActor()
part2_actor.SetMapper(part2_mapper)
part2_actor.SetTexture(motor_texture)
part2_actor.GetProperty().SetColor(part2_rgb)

# Source - Part 3 (raw_sienna, hidden) — needs TriangleFilter
part3_reader = vtkBYUReader()
part3_reader.SetGeometryFileName(os.path.join(data_dir, "motor.g"))
part3_reader.SetPartNumber(3)

part3_triangles = vtkTriangleFilter()
part3_triangles.SetInputConnection(part3_reader.GetOutputPort())

part3_normals = vtkPolyDataNormals()
part3_normals.SetInputConnection(part3_triangles.GetOutputPort())

part3_tex_coords = vtkImplicitTextureCoords()
part3_tex_coords.SetInputConnection(part3_normals.GetOutputPort())
part3_tex_coords.SetRFunction(cutting_planes)

part3_mapper = vtkDataSetMapper()
part3_mapper.SetInputConnection(part3_tex_coords.GetOutputPort())

part3_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("raw_sienna", part3_rgb)

part3_actor = vtkActor()
part3_actor.SetMapper(part3_mapper)
part3_actor.SetTexture(motor_texture)
part3_actor.GetProperty().SetColor(part3_rgb)
part3_actor.VisibilityOff()

# Source - Part 4 (banana, visible)
part4_reader = vtkBYUReader()
part4_reader.SetGeometryFileName(os.path.join(data_dir, "motor.g"))
part4_reader.SetPartNumber(4)

part4_normals = vtkPolyDataNormals()
part4_normals.SetInputConnection(part4_reader.GetOutputPort())

part4_tex_coords = vtkImplicitTextureCoords()
part4_tex_coords.SetInputConnection(part4_normals.GetOutputPort())
part4_tex_coords.SetRFunction(cutting_planes)

part4_mapper = vtkDataSetMapper()
part4_mapper.SetInputConnection(part4_tex_coords.GetOutputPort())

part4_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("banana", part4_rgb)

part4_actor = vtkActor()
part4_actor.SetMapper(part4_mapper)
part4_actor.SetTexture(motor_texture)
part4_actor.GetProperty().SetColor(part4_rgb)

# Source - Part 5 (peach_puff, visible)
part5_reader = vtkBYUReader()
part5_reader.SetGeometryFileName(os.path.join(data_dir, "motor.g"))
part5_reader.SetPartNumber(5)

part5_normals = vtkPolyDataNormals()
part5_normals.SetInputConnection(part5_reader.GetOutputPort())

part5_tex_coords = vtkImplicitTextureCoords()
part5_tex_coords.SetInputConnection(part5_normals.GetOutputPort())
part5_tex_coords.SetRFunction(cutting_planes)

part5_mapper = vtkDataSetMapper()
part5_mapper.SetInputConnection(part5_tex_coords.GetOutputPort())

part5_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("peach_puff", part5_rgb)

part5_actor = vtkActor()
part5_actor.SetMapper(part5_mapper)
part5_actor.SetTexture(motor_texture)
part5_actor.GetProperty().SetColor(part5_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(part1_actor)
renderer.AddActor(part2_actor)
renderer.AddActor(part3_actor)
renderer.AddActor(part4_actor)
renderer.AddActor(part5_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("motor")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0.0286334, 0.0362996, 0.0379685)
camera.SetPosition(1.37067, 1.08629, -1.30349)
camera.SetViewAngle(17.673)
camera.SetClippingRange(1, 10)
camera.SetViewUp(-0.376306, -0.5085, -0.774482)
renderer.SetActiveCamera(camera)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
