#!/usr/bin/env python

# Texture clipping of a motor model using a transparent texture map.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
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

# Colors (normalized RGB)
cold_grey = (0.600, 0.600, 0.600)
peacock = (0.200, 0.631, 0.788)
raw_sienna = (0.780, 0.380, 0.082)
banana = (0.890, 0.812, 0.341)
peach_puff = (1.000, 0.855, 0.725)
alice_blue = (0.941, 0.973, 1.000)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
texture_file = str(data_dir / "texThres2.vtk")
motor_file = str(data_dir / "motor.g")

# Implicit function: cutting planes for texture clipping
planes = vtkPlanes()
plane_points = vtkPoints()
plane_normals = vtkFloatArray()
plane_normals.SetNumberOfComponents(3)
plane_points.InsertPoint(0, 0.0, 0.0, 0.0)
plane_normals.InsertTuple3(0, 0.0, 0.0, 1.0)
plane_points.InsertPoint(1, 0.0, 0.0, 0.0)
plane_normals.InsertTuple3(1, -1.0, 0.0, 0.0)
planes.SetPoints(plane_points)
planes.SetNormals(plane_normals)

# Reader: load the texture map
tex_reader = vtkStructuredPointsReader()
tex_reader.SetFileName(texture_file)

texture = vtkTexture()
texture.SetInputConnection(tex_reader.GetOutputPort())
texture.InterpolateOff()
texture.RepeatOff()

# Reader: load motor part 1 geometry
part_0_reader = vtkBYUReader()
part_0_reader.SetGeometryFileName(motor_file)
part_0_reader.SetPartNumber(1)

# Filter: compute normals for part 1
part_0_normals = vtkPolyDataNormals()
part_0_normals.SetInputConnection(part_0_reader.GetOutputPort())

# Filter: generate implicit texture coordinates for part 1
part_0_tex_coords = vtkImplicitTextureCoords()
part_0_tex_coords.SetInputConnection(part_0_normals.GetOutputPort())
part_0_tex_coords.SetRFunction(planes)

# Mapper: map textured geometry to graphics primitives for part 1
part_0_mapper = vtkDataSetMapper()
part_0_mapper.SetInputConnection(part_0_tex_coords.GetOutputPort())

# Actor: display motor part 1
part_0_actor = vtkActor()
part_0_actor.SetMapper(part_0_mapper)
part_0_actor.SetTexture(texture)
part_0_actor.GetProperty().SetColor(cold_grey)

# Reader: load motor part 2 geometry
part_1_reader = vtkBYUReader()
part_1_reader.SetGeometryFileName(motor_file)
part_1_reader.SetPartNumber(2)

# Filter: compute normals for part 2
part_1_normals = vtkPolyDataNormals()
part_1_normals.SetInputConnection(part_1_reader.GetOutputPort())

# Filter: generate implicit texture coordinates for part 2
part_1_tex_coords = vtkImplicitTextureCoords()
part_1_tex_coords.SetInputConnection(part_1_normals.GetOutputPort())
part_1_tex_coords.SetRFunction(planes)

# Mapper: map textured geometry to graphics primitives for part 2
part_1_mapper = vtkDataSetMapper()
part_1_mapper.SetInputConnection(part_1_tex_coords.GetOutputPort())

# Actor: display motor part 2
part_1_actor = vtkActor()
part_1_actor.SetMapper(part_1_mapper)
part_1_actor.SetTexture(texture)
part_1_actor.GetProperty().SetColor(peacock)

# Reader: load motor part 3 geometry
part_2_reader = vtkBYUReader()
part_2_reader.SetGeometryFileName(motor_file)
part_2_reader.SetPartNumber(3)

# Filter: compute normals for part 3
part_2_normals = vtkPolyDataNormals()
part_2_normals.SetInputConnection(part_2_reader.GetOutputPort())

# Filter: generate implicit texture coordinates for part 3
part_2_tex_coords = vtkImplicitTextureCoords()
part_2_tex_coords.SetInputConnection(part_2_normals.GetOutputPort())
part_2_tex_coords.SetRFunction(planes)

# Mapper: map textured geometry to graphics primitives for part 3
part_2_mapper = vtkDataSetMapper()
part_2_mapper.SetInputConnection(part_2_tex_coords.GetOutputPort())

# Actor: display motor part 3
part_2_actor = vtkActor()
part_2_actor.SetMapper(part_2_mapper)
part_2_actor.SetTexture(texture)
part_2_actor.GetProperty().SetColor(raw_sienna)

# Reader: load motor part 4 geometry
part_3_reader = vtkBYUReader()
part_3_reader.SetGeometryFileName(motor_file)
part_3_reader.SetPartNumber(4)

# Filter: compute normals for part 4
part_3_normals = vtkPolyDataNormals()
part_3_normals.SetInputConnection(part_3_reader.GetOutputPort())

# Filter: generate implicit texture coordinates for part 4
part_3_tex_coords = vtkImplicitTextureCoords()
part_3_tex_coords.SetInputConnection(part_3_normals.GetOutputPort())
part_3_tex_coords.SetRFunction(planes)

# Mapper: map textured geometry to graphics primitives for part 4
part_3_mapper = vtkDataSetMapper()
part_3_mapper.SetInputConnection(part_3_tex_coords.GetOutputPort())

# Actor: display motor part 4
part_3_actor = vtkActor()
part_3_actor.SetMapper(part_3_mapper)
part_3_actor.SetTexture(texture)
part_3_actor.GetProperty().SetColor(banana)

# Reader: load motor part 5 geometry
part_4_reader = vtkBYUReader()
part_4_reader.SetGeometryFileName(motor_file)
part_4_reader.SetPartNumber(5)

# Filter: compute normals for part 5
part_4_normals = vtkPolyDataNormals()
part_4_normals.SetInputConnection(part_4_reader.GetOutputPort())

# Filter: generate implicit texture coordinates for part 5
part_4_tex_coords = vtkImplicitTextureCoords()
part_4_tex_coords.SetInputConnection(part_4_normals.GetOutputPort())
part_4_tex_coords.SetRFunction(planes)

# Mapper: map textured geometry to graphics primitives for part 5
part_4_mapper = vtkDataSetMapper()
part_4_mapper.SetInputConnection(part_4_tex_coords.GetOutputPort())

# Actor: display motor part 5
part_4_actor = vtkActor()
part_4_actor.SetMapper(part_4_mapper)
part_4_actor.SetTexture(texture)
part_4_actor.GetProperty().SetColor(peach_puff)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(part_0_actor)
renderer.AddActor(part_1_actor)
renderer.AddActor(part_2_actor)
renderer.AddActor(part_3_actor)
renderer.AddActor(part_4_actor)
renderer.SetBackground(alice_blue)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("motor")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 512)

# Scene: configure the camera
camera = vtkCamera()
camera.SetFocalPoint(0.0286334, 0.0362996, 0.0379685)
camera.SetPosition(1.37067, 1.08629, -1.30349)
camera.SetViewAngle(17.673)
camera.SetClippingRange(1, 10)
camera.SetViewUp(-0.376306, -0.5085, -0.774482)
renderer.SetActiveCamera(camera)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
