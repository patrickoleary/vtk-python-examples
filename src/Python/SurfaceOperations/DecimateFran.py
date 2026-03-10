#!/usr/bin/env python

# Decimation of a laser-digitized face mesh compared side-by-side with the original.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkPolyDataNormals,
)
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
papaya_whip = (1.000, 0.937, 0.835)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
mesh_file = str(data_dir / "fran_cut.vtk")
texture_file = str(data_dir / "fran_cut.png")

# Reader: load the face mesh from a Cyberware laser digitizer scan
fran = vtkPolyDataReader()
fran.SetFileName(mesh_file)

# Reader: load the corresponding face texture
texture_reader = vtkPNGReader()
texture_reader.SetFileName(texture_file)

texture = vtkTexture()
texture.InterpolateOn()
texture.SetInputConnection(texture_reader.GetOutputPort())

# Filter: decimate the mesh by 90% while preserving topology
deci = vtkDecimatePro()
deci.SetInputConnection(fran.GetOutputPort())
deci.SetTargetReduction(0.9)
deci.PreserveTopologyOn()

# Filter: compute normals on the decimated mesh
decimated_normals = vtkPolyDataNormals()
decimated_normals.SetInputConnection(deci.GetOutputPort())
decimated_normals.FlipNormalsOn()
decimated_normals.SetFeatureAngle(60)

# Filter: compute normals on the original mesh
original_normals = vtkPolyDataNormals()
original_normals.SetInputConnection(fran.GetOutputPort())
original_normals.FlipNormalsOn()
original_normals.SetFeatureAngle(60)

# Mapper: map the decimated mesh to graphics primitives
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimated_normals.GetOutputPort())

# Actor: display the decimated mesh with texture
decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetAmbient(0.5)
decimated_actor.GetProperty().SetDiffuse(0.5)
decimated_actor.SetTexture(texture)

# Mapper: map the original mesh to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(original_normals.GetOutputPort())

# Actor: display the original mesh with texture
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetAmbient(0.5)
original_actor.GetProperty().SetDiffuse(0.5)
original_actor.SetTexture(texture)

# Camera: shared between both viewports
cam = vtkCamera()
cam.SetClippingRange(0.0475572, 2.37786)
cam.SetFocalPoint(0.052665, -0.129454, -0.0573973)
cam.SetPosition(0.327637, -0.116299, -0.256418)
cam.SetViewUp(-0.0225386, 0.999137, 0.034901)

# Renderer: left viewport shows the original mesh
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(original_actor)
renderer_left.SetBackground(wheat)
renderer_left.SetActiveCamera(cam)

# Renderer: right viewport shows the decimated mesh
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(decimated_actor)
renderer_right.SetBackground(papaya_whip)
renderer_right.SetActiveCamera(cam)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetWindowName("DecimateFran")
render_window.SetSize(800, 400)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
