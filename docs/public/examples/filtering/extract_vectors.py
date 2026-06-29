#!/usr/bin/env python

# Demonstrate vtkExtractVectorComponents extracting Vx, Vy, Vz
# components from PLOT3D combustor data, contouring each component
# separately.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkPolyDataNormals,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractVectorComponents
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D combustor data
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
output = plot3d_reader.GetOutput().GetBlock(0)

# Extract Vx component and contour
vx = vtkExtractVectorComponents()
vx.SetInputData(output)
vx.Update()

iso_vx = vtkContourFilter()
iso_vx.SetInputData(vx.GetVxComponent())
iso_vx.SetValue(0, 0.38)

normals_vx = vtkPolyDataNormals()
normals_vx.SetInputConnection(iso_vx.GetOutputPort())
normals_vx.SetFeatureAngle(45)

iso_vx_mapper = vtkPolyDataMapper()
iso_vx_mapper.SetInputConnection(normals_vx.GetOutputPort())
iso_vx_mapper.ScalarVisibilityOff()

iso_vx_actor = vtkActor()
iso_vx_actor.SetMapper(iso_vx_mapper)
iso_vx_actor.GetProperty().SetColor(1, 0.7, 0.6)
iso_vx_actor.AddPosition(0, 12, 0)

# Extract Vy component and contour
vy = vtkExtractVectorComponents()
vy.SetInputData(output)
vy.Update()

iso_vy = vtkContourFilter()
iso_vy.SetInputData(vy.GetVyComponent())
iso_vy.SetValue(0, 0.38)

normals_vy = vtkPolyDataNormals()
normals_vy.SetInputConnection(iso_vy.GetOutputPort())
normals_vy.SetFeatureAngle(45)

iso_vy_mapper = vtkPolyDataMapper()
iso_vy_mapper.SetInputConnection(normals_vy.GetOutputPort())
iso_vy_mapper.ScalarVisibilityOff()

iso_vy_actor = vtkActor()
iso_vy_actor.SetMapper(iso_vy_mapper)
iso_vy_actor.GetProperty().SetColor(0.7, 1, 0.6)

# Extract Vz component and contour
vz = vtkExtractVectorComponents()
vz.SetInputData(output)
vz.Update()

iso_vz = vtkContourFilter()
iso_vz.SetInputData(vz.GetVzComponent())
iso_vz.SetValue(0, 0.38)

normals_vz = vtkPolyDataNormals()
normals_vz.SetInputConnection(iso_vz.GetOutputPort())
normals_vz.SetFeatureAngle(45)

iso_vz_mapper = vtkPolyDataMapper()
iso_vz_mapper.SetInputConnection(normals_vz.GetOutputPort())
iso_vz_mapper.ScalarVisibilityOff()

iso_vz_actor = vtkActor()
iso_vz_actor.SetMapper(iso_vz_mapper)
iso_vz_actor.GetProperty().SetColor(0.4, 0.5, 1)
iso_vz_actor.AddPosition(0, -12, 0)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_vx_actor)
renderer.AddActor(iso_vy_actor)
renderer.AddActor(iso_vz_actor)
renderer.SetBackground(0.8, 0.8, 0.8)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 320)
render_window.SetWindowName("extract vectors")

# Scene
renderer.GetActiveCamera().SetPosition(-63.3093, -1.55444, 64.3922)
renderer.GetActiveCamera().SetFocalPoint(8.255, 0.0499763, 29.7631)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
