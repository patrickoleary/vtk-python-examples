#!/usr/bin/env python

# Test vtkRendererSource capturing a renderer to a texture on a plane.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkPolyDataNormals,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkRendererSource,
    vtkTexture,
)

# Named colors helper
colors = vtkNamedColors()
bisque_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("bisque", bisque_rgb)

# Renderers
renderer_0 = vtkRenderer()
renderer_1 = vtkRenderer()

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("renderer source")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 256)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Read PLOT3D data for scalar coloring
pl3d_2 = vtkMultiBlockPLOT3DReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

pl3d_2.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d_2.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d_2.SetScalarFunctionNumber(153)
pl3d_2.Update()

output_2 = pl3d_2.GetOutput().GetBlock(0)

pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(120)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

output = pl3d.GetOutput().GetBlock(0)

# Iso-surface pipeline
iso = vtkContourFilter()
iso.SetInputData(output)
iso.SetValue(0, -100000)

probe_2 = vtkProbeFilter()
probe_2.SetInputConnection(iso.GetOutputPort())
probe_2.SetSourceData(output_2)

cast_2 = vtkCastToConcrete()
cast_2.SetInputConnection(probe_2.GetOutputPort())

normals = vtkPolyDataNormals()
normals.SetInputConnection(cast_2.GetOutputPort())
normals.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOn()
iso_mapper.SetScalarRange(output_2.GetPointData().GetScalars().GetRange())

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(bisque_rgb)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Left renderer - 3D scene
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(iso_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.ResetCamera()

camera_1 = renderer_0.GetActiveCamera()
camera_1.SetClippingRange(3.95297, 50)
camera_1.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera_1.SetPosition(2.7439, -37.3196, 38.7167)
camera_1.SetViewUp(-0.16123, 0.264271, 0.950876)

# Right renderer - plane with captured texture
plane = vtkPlaneSource()

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

screen = vtkActor()
screen.SetMapper(plane_mapper)

renderer_1.AddActor(screen)
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.GetActiveCamera().Azimuth(30)
renderer_1.GetActiveCamera().Elevation(30)
renderer_1.SetBackground(0.8, 0.4, 0.3)
renderer_0.ResetCameraClippingRange()
renderer_1.ResetCamera()
renderer_1.ResetCameraClippingRange()

render_window.Render()

# Capture renderer_0 to texture
renderer_source = vtkRendererSource()
renderer_source.SetInput(renderer_0)
renderer_source.DepthValuesOn()

texture = vtkTexture()
texture.SetInputConnection(renderer_source.GetOutputPort())

screen.SetTexture(texture)

interactor.Initialize()
interactor.Start()
