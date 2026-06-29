#!/usr/bin/env python

# Demonstrate vtkProgrammableAttributeDataFilter by computing the cosine
# of the angle between pressure gradient and velocity vector fields from
# a PLOT3D dataset, visualized with hedgehog glyphs and a dot product
# scalar field on a contour surface.

import math
import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkHedgeHog,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableAttributeDataFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the pressure gradient vector field
pl3d_gradient = vtkMultiBlockPLOT3DReader()
pl3d_gradient.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d_gradient.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d_gradient.SetScalarFunctionNumber(100)
pl3d_gradient.SetVectorFunctionNumber(210)
pl3d_gradient.Update()
pl3d_g_output = pl3d_gradient.GetOutput().GetBlock(0)

# Read the velocity vector field
pl3d_velocity = vtkMultiBlockPLOT3DReader()
pl3d_velocity.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d_velocity.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d_velocity.SetScalarFunctionNumber(100)
pl3d_velocity.SetVectorFunctionNumber(200)
pl3d_velocity.Update()
pl3d_v_output = pl3d_velocity.GetOutput().GetBlock(0)

# Contour the scalar field
contour = vtkContourFilter()
contour.SetInputData(pl3d_g_output)
contour.SetValue(0, 0.225)

# Probe gradient and velocity onto the contour surface
probe_gradient = vtkProbeFilter()
probe_gradient.SetInputConnection(contour.GetOutputPort())
probe_gradient.SetSourceData(pl3d_g_output)

probe_velocity = vtkProbeFilter()
probe_velocity.SetInputConnection(contour.GetOutputPort())
probe_velocity.SetSourceData(pl3d_v_output)

# Hedgehog for velocity field
velocity = vtkHedgeHog()
velocity.SetInputConnection(probe_velocity.GetOutputPort())
velocity.SetScaleFactor(0.0015)

# Hedgehog for pressure gradient field
pressure_gradient = vtkHedgeHog()
pressure_gradient.SetInputConnection(probe_gradient.GetOutputPort())
pressure_gradient.SetScaleFactor(0.00002)

# Programmable filter to compute dot product between the two vector fields.
# The def is required by vtkProgrammableAttributeDataFilter.SetExecuteMethod().
dot_product = vtkProgrammableAttributeDataFilter()
dot_product.SetInputConnection(probe_velocity.GetOutputPort())
dot_product.AddInput(probe_velocity.GetOutput())
dot_product.AddInput(probe_gradient.GetOutput())


def execute_dot():
    inputs = dot_product.GetInputList()
    input0 = inputs.GetDataSet(0)
    input1 = inputs.GetDataSet(1)
    num_pts = input0.GetNumberOfPoints()
    vectors0 = input0.GetPointData().GetVectors()
    vectors1 = input1.GetPointData().GetVectors()
    scalars = vtkFloatArray()
    for i in range(num_pts):
        v0x, v0y, v0z = vectors0.GetTuple3(i)
        v1x, v1y, v1z = vectors1.GetTuple3(i)
        l0 = math.sqrt(v0x * v0x + v0y * v0y + v0z * v0z)
        l1 = math.sqrt(v1x * v1x + v1y * v1y + v1z * v1z)
        if l0 > 0.0 and l1 > 0.0:
            d = (v0x * v1x + v0y * v1y + v0z * v1z) / (l0 * l1)
        else:
            d = 0.0
        scalars.InsertValue(i, d)
    dot_product.GetOutput().GetPointData().SetScalars(scalars)


dot_product.SetExecuteMethod(execute_dot)

# Velocity hedgehog mapper/actor
velocity_mapper = vtkPolyDataMapper()
velocity_mapper.SetInputConnection(velocity.GetOutputPort())
velocity_mapper.ScalarVisibilityOff()

velocity_actor = vtkLODActor()
velocity_actor.SetMapper(velocity_mapper)
velocity_actor.SetNumberOfCloudPoints(1000)
velocity_actor.GetProperty().SetColor(1, 0, 0)

# Pressure gradient hedgehog mapper/actor
pressure_gradient_mapper = vtkPolyDataMapper()
pressure_gradient_mapper.SetInputConnection(pressure_gradient.GetOutputPort())
pressure_gradient_mapper.ScalarVisibilityOff()

pressure_gradient_actor = vtkLODActor()
pressure_gradient_actor.SetMapper(pressure_gradient_mapper)
pressure_gradient_actor.SetNumberOfCloudPoints(1000)
pressure_gradient_actor.GetProperty().SetColor(0, 1, 0)

# Dot product mapper/actor
dot_mapper = vtkPolyDataMapper()
dot_mapper.SetInputConnection(dot_product.GetOutputPort())
dot_mapper.SetScalarRange(-1, 1)

dot_actor = vtkLODActor()
dot_actor.SetMapper(dot_mapper)
dot_actor.SetNumberOfCloudPoints(1000)

# Outline from the original dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.Update()
pl3d_output = pl3d.GetOutput().GetBlock(0)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(pl3d_output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(velocity_actor)
renderer.AddActor(pressure_gradient_actor)
renderer.AddActor(dot_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)
render_window.SetWindowName("multidimensional solution")

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.95297, 50)
camera.SetFocalPoint(9.71821, 0.458166, 29.3999)
camera.SetPosition(-21.6807, -22.6387, 35.9759)
camera.SetViewUp(-0.0158865, 0.293715, 0.955761)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
