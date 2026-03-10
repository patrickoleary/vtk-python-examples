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

part_colors = [cold_grey, peacock, raw_sienna, banana, peach_puff]

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

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(alice_blue)

# Build pipelines for each motor part
number_of_parts = 5
for i in range(number_of_parts):
    # ---- Reader: load motor part geometry ----
    byu_reader = vtkBYUReader()
    byu_reader.SetGeometryFileName(motor_file)
    byu_reader.SetPartNumber(i + 1)

    # ---- Filter: compute normals ----
    normals = vtkPolyDataNormals()
    normals.SetInputConnection(byu_reader.GetOutputPort())

    # ---- Filter: generate implicit texture coordinates ----
    tex_coords = vtkImplicitTextureCoords()
    tex_coords.SetInputConnection(normals.GetOutputPort())
    tex_coords.SetRFunction(planes)

    # ---- Mapper: map textured geometry to graphics primitives ----
    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(tex_coords.GetOutputPort())

    # ---- Actor: display the motor part ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
    actor.GetProperty().SetColor(part_colors[i])

    renderer.AddActor(actor)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetFocalPoint(0.0286334, 0.0362996, 0.0379685)
camera.SetPosition(1.37067, 1.08629, -1.30349)
camera.SetViewAngle(17.673)
camera.SetClippingRange(1, 10)
camera.SetViewUp(-0.376306, -0.5085, -0.774482)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Motor")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
