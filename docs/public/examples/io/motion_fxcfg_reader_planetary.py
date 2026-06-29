#!/usr/bin/env python

# Read a MotionFX CFG file for a planetary gear animation and render at the middle time step.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkStreamingDemandDrivenPipeline
from vtkmodules.vtkIOMotionFX import vtkMotionFXCFGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "MotionFX")

# Read the CFG file
motionfx_reader = vtkMotionFXCFGReader()
motionfx_reader.SetFileName(os.path.join(data_dir, "planetary", "Planetary_prescribedCOMmotion.cfg"))
motionfx_reader.SetTimeResolution(100)
motionfx_reader.UpdateInformation()

# Get time steps
out_info = motionfx_reader.GetOutputInformation(0)
num_time_steps = out_info.Length(vtkStreamingDemandDrivenPipeline.TIME_STEPS())
time_steps = [out_info.Get(vtkStreamingDemandDrivenPipeline.TIME_STEPS(), i)
              for i in range(num_time_steps)]

# Update to middle time step
motionfx_reader.UpdateTimeStep(time_steps[num_time_steps // 2])

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputDataObject(motionfx_reader.GetOutputDataObject(0))

# Actor
actor = vtkActor()
actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("motion fxcfg reader planetary")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(-412.84, 121.00, -304.88)
camera.SetPosition(-412.17, 121.27, -305.32)
camera.SetViewUp(0.54, 0.032, 0.83)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
