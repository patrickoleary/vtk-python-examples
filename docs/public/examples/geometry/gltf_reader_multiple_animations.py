#!/usr/bin/env python

# Read a glTF file with multiple animations (interpolation test) and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkIOGeometry import vtkGLTFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read glTF file with multiple animations
step = 75
gltf_reader = vtkGLTFReader()
gltf_reader.SetFileName(os.path.join(data_dir, "glTF", "InterpolationTest", "InterpolationTest.gltf"))
gltf_reader.SetFrameRate(60)
gltf_reader.ApplyDeformationsToGeometryOn()

# Enable all animations
gltf_reader.UpdateInformation()
for i in range(gltf_reader.GetNumberOfAnimations()):
    gltf_reader.EnableAnimation(i)

# Update to get time steps
gltf_reader.UpdateInformation()
output_info = gltf_reader.GetOutputInformation(0)
nb_steps = output_info.Length(vtkStreamingDemandDrivenPipeline.TIME_STEPS())
assert nb_steps >= step, f"Not enough time steps: {nb_steps} < {step}"

time = output_info.Get(vtkStreamingDemandDrivenPipeline.TIME_STEPS(), step)
output_info.Set(vtkStreamingDemandDrivenPipeline.UPDATE_TIME_STEP(), time)
gltf_reader.Update()

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(gltf_reader.GetOutputPort())

# Actor
gltf_actor = vtkActor()
gltf_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(gltf_actor)
renderer.SetBackground(0.0, 0.0, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf reader multiple animations")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(30)
camera.SetClippingRange(0.1, 1000)

interactor.Initialize()
interactor.Start()
