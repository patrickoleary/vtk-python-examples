#!/usr/bin/env python

# Display all Plot3D vector functions in a 2x2 grid of renderers with hedgehogs.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
    vtkTextProperty,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

vector_labels = ["Velocity", "Vorticity", "Momentum", "Pressure_Gradient"]
vector_functions = [200, 201, 202, 210]

camera = vtkCamera()
light = vtkLight()

# Shared text property
text_prop = vtkTextProperty()
text_prop.SetFontSize(10)
text_prop.SetFontFamilyToArial()
text_prop.SetColor(0.3, 1, 1)

# Source - Velocity (200)
velocity_reader = vtkMultiBlockPLOT3DReader()
velocity_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
velocity_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
velocity_reader.SetVectorFunctionNumber(200)
velocity_reader.Update()
velocity_output = velocity_reader.GetOutput().GetBlock(0)

velocity_geometry = vtkStructuredGridGeometryFilter()
velocity_geometry.SetInputData(velocity_output)
velocity_geometry.SetExtent(25, 25, 0, 100, 0, 100)

velocity_hog = vtkHedgeHog()
velocity_hog.SetInputConnection(velocity_geometry.GetOutputPort())
velocity_hog.SetScaleFactor(1.0 / velocity_output.GetPointData().GetVectors().GetMaxNorm())

# Mapper - Velocity
velocity_mapper = vtkPolyDataMapper()
velocity_mapper.SetInputConnection(velocity_hog.GetOutputPort())

# Actor - Velocity
velocity_actor = vtkActor()
velocity_actor.SetMapper(velocity_mapper)

velocity_text_mapper = vtkTextMapper()
velocity_text_mapper.SetInput("Velocity")
velocity_text_mapper.SetTextProperty(text_prop)

velocity_text_actor = vtkActor2D()
velocity_text_actor.SetMapper(velocity_text_mapper)
velocity_text_actor.SetPosition(2, 5)

# Source - Vorticity (201)
vorticity_reader = vtkMultiBlockPLOT3DReader()
vorticity_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
vorticity_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
vorticity_reader.SetVectorFunctionNumber(201)
vorticity_reader.Update()
vorticity_output = vorticity_reader.GetOutput().GetBlock(0)

vorticity_geometry = vtkStructuredGridGeometryFilter()
vorticity_geometry.SetInputData(vorticity_output)
vorticity_geometry.SetExtent(25, 25, 0, 100, 0, 100)

vorticity_hog = vtkHedgeHog()
vorticity_hog.SetInputConnection(vorticity_geometry.GetOutputPort())
vorticity_hog.SetScaleFactor(1.0 / vorticity_output.GetPointData().GetVectors().GetMaxNorm())

# Mapper - Vorticity
vorticity_mapper = vtkPolyDataMapper()
vorticity_mapper.SetInputConnection(vorticity_hog.GetOutputPort())

# Actor - Vorticity
vorticity_actor = vtkActor()
vorticity_actor.SetMapper(vorticity_mapper)

vorticity_text_mapper = vtkTextMapper()
vorticity_text_mapper.SetInput("Vorticity")
vorticity_text_mapper.SetTextProperty(text_prop)

vorticity_text_actor = vtkActor2D()
vorticity_text_actor.SetMapper(vorticity_text_mapper)
vorticity_text_actor.SetPosition(2, 5)

# Source - Momentum (202)
momentum_reader = vtkMultiBlockPLOT3DReader()
momentum_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
momentum_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
momentum_reader.SetVectorFunctionNumber(202)
momentum_reader.Update()
momentum_output = momentum_reader.GetOutput().GetBlock(0)

momentum_geometry = vtkStructuredGridGeometryFilter()
momentum_geometry.SetInputData(momentum_output)
momentum_geometry.SetExtent(25, 25, 0, 100, 0, 100)

momentum_hog = vtkHedgeHog()
momentum_hog.SetInputConnection(momentum_geometry.GetOutputPort())
momentum_hog.SetScaleFactor(1.0 / momentum_output.GetPointData().GetVectors().GetMaxNorm())

# Mapper - Momentum
momentum_mapper = vtkPolyDataMapper()
momentum_mapper.SetInputConnection(momentum_hog.GetOutputPort())

# Actor - Momentum
momentum_actor = vtkActor()
momentum_actor.SetMapper(momentum_mapper)

momentum_text_mapper = vtkTextMapper()
momentum_text_mapper.SetInput("Momentum")
momentum_text_mapper.SetTextProperty(text_prop)

momentum_text_actor = vtkActor2D()
momentum_text_actor.SetMapper(momentum_text_mapper)
momentum_text_actor.SetPosition(2, 5)

# Source - Pressure Gradient (210)
pressure_gradient_reader = vtkMultiBlockPLOT3DReader()
pressure_gradient_reader.SetXYZFileName(os.path.join(data_dir, "bluntfinxyz.bin"))
pressure_gradient_reader.SetQFileName(os.path.join(data_dir, "bluntfinq.bin"))
pressure_gradient_reader.SetVectorFunctionNumber(210)
pressure_gradient_reader.Update()
pressure_gradient_output = pressure_gradient_reader.GetOutput().GetBlock(0)

pressure_gradient_geometry = vtkStructuredGridGeometryFilter()
pressure_gradient_geometry.SetInputData(pressure_gradient_output)
pressure_gradient_geometry.SetExtent(25, 25, 0, 100, 0, 100)

pressure_gradient_hog = vtkHedgeHog()
pressure_gradient_hog.SetInputConnection(pressure_gradient_geometry.GetOutputPort())
pressure_gradient_hog.SetScaleFactor(1.0 / pressure_gradient_output.GetPointData().GetVectors().GetMaxNorm())

# Mapper - Pressure Gradient
pressure_gradient_mapper = vtkPolyDataMapper()
pressure_gradient_mapper.SetInputConnection(pressure_gradient_hog.GetOutputPort())

# Actor - Pressure Gradient
pressure_gradient_actor = vtkActor()
pressure_gradient_actor.SetMapper(pressure_gradient_mapper)

pressure_gradient_text_mapper = vtkTextMapper()
pressure_gradient_text_mapper.SetInput("Pressure_Gradient")
pressure_gradient_text_mapper.SetTextProperty(text_prop)

pressure_gradient_text_actor = vtkActor2D()
pressure_gradient_text_actor.SetMapper(pressure_gradient_text_mapper)
pressure_gradient_text_actor.SetPosition(2, 5)

# Renderers
velocity_renderer = vtkRenderer()
velocity_renderer.SetBackground(0.5, 0.5, 0.5)
velocity_renderer.SetActiveCamera(camera)
velocity_renderer.AddLight(light)
velocity_renderer.AddActor(velocity_actor)
velocity_renderer.AddViewProp(velocity_text_actor)
velocity_renderer.SetViewport(0.025, 0.025, 0.475, 0.475)

vorticity_renderer = vtkRenderer()
vorticity_renderer.SetBackground(0.5, 0.5, 0.5)
vorticity_renderer.SetActiveCamera(camera)
vorticity_renderer.AddLight(light)
vorticity_renderer.AddActor(vorticity_actor)
vorticity_renderer.AddViewProp(vorticity_text_actor)
vorticity_renderer.SetViewport(0.525, 0.025, 0.975, 0.475)

momentum_renderer = vtkRenderer()
momentum_renderer.SetBackground(0.5, 0.5, 0.5)
momentum_renderer.SetActiveCamera(camera)
momentum_renderer.AddLight(light)
momentum_renderer.AddActor(momentum_actor)
momentum_renderer.AddViewProp(momentum_text_actor)
momentum_renderer.SetViewport(0.025, 0.525, 0.475, 0.975)

pressure_gradient_renderer = vtkRenderer()
pressure_gradient_renderer.SetBackground(0.5, 0.5, 0.5)
pressure_gradient_renderer.SetActiveCamera(camera)
pressure_gradient_renderer.AddLight(light)
pressure_gradient_renderer.AddActor(pressure_gradient_actor)
pressure_gradient_renderer.AddViewProp(pressure_gradient_text_actor)
pressure_gradient_renderer.SetViewport(0.525, 0.525, 0.975, 0.975)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(velocity_renderer)
render_window.AddRenderer(vorticity_renderer)
render_window.AddRenderer(momentum_renderer)
render_window.AddRenderer(pressure_gradient_renderer)
render_window.SetWindowName("plot3d vectors")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 350)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera.SetViewUp(1, 0, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0.4, -0.5, -0.75)
velocity_renderer.ResetCamera()
camera.Dolly(1.25)

velocity_renderer.ResetCameraClippingRange()
vorticity_renderer.ResetCameraClippingRange()
momentum_renderer.ResetCameraClippingRange()
pressure_gradient_renderer.ResetCameraClippingRange()

light.SetPosition(camera.GetPosition())
light.SetFocalPoint(camera.GetFocalPoint())

interactor.Initialize()
interactor.Start()
