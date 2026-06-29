#!/usr/bin/env python

# Test vtkCompositeSurfaceLICMapper: SurfaceLICCurvedContrastEnhancedMappedSmallVectorNormalizeOff.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLICOpenGL2 import (
    vtkCompositeSurfaceLICMapper,
    vtkSurfaceLICInterface,
)

# Read data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "disk_out_ref_surface.vtp"))
reader.Update()
data_obj = reader.GetOutputDataObject(0)

# Mapper
lic_mapper = vtkCompositeSurfaceLICMapper()
lic_mapper.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS_THEN_CELLS, "V")
lic_mapper.SetInputDataObject(data_obj)

# LIC interface parameters
lic_interface = lic_mapper.GetLICInterface()
lic_interface.SetNumberOfSteps(800)
lic_interface.SetStepSize(0.5)
lic_interface.SetEnhancedLIC(1)
lic_interface.SetNormalizeVectors(0)
lic_interface.SetGenerateNoiseTexture(1)
lic_interface.SetNoiseType(1)
lic_interface.SetNoiseTextureSize(200)
lic_interface.SetNoiseGrainSize(1)
lic_interface.SetMinNoiseValue(0.0)
lic_interface.SetMaxNoiseValue(1.0)
lic_interface.SetNumberOfNoiseLevels(1024)
lic_interface.SetImpulseNoiseProbability(1.0)
lic_interface.SetImpulseNoiseBackgroundValue(0.0)
lic_interface.SetNoiseGeneratorSeed(1)
lic_interface.SetEnhanceContrast(1)
lic_interface.SetLowLICContrastEnhancementFactor(0.05)
lic_interface.SetHighLICContrastEnhancementFactor(0.0)
lic_interface.SetLowColorContrastEnhancementFactor(0.0)
lic_interface.SetHighColorContrastEnhancementFactor(0.0)
lic_interface.SetAntiAlias(0)
lic_interface.SetColorMode(1)
lic_interface.SetLICIntensity(0.8)
lic_interface.SetMapModeBias(0.0)
lic_interface.SetMaskOnSurface(0)
lic_interface.SetMaskThreshold(0.0)
lic_interface.SetMaskIntensity(0.0)
lic_interface.SetMaskColor([1.0, 0.0, 0.84705])

# Actor
lic_actor = vtkActor()
lic_actor.SetMapper(lic_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(lic_actor)
renderer.SetBackground(0.3216, 0.3412, 0.4314)
renderer.SetBackground2(0.0, 0.0, 0.1647)
renderer.GradientBackgroundOn()

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("surface lic curved contrast enhanced mapped small vector normalize off")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Functional render for OpenGL context check
render_window.Render()

if not vtkSurfaceLICInterface.IsSupported(render_window):
    print("WARNING: Surface LIC not supported, skipping.")
else:
    # Scene
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(-1.88, -0.98, -1.04)
    camera.SetPosition(13.64, 4.27, -31.59)
    camera.SetViewAngle(30)
    camera.SetViewUp(0.41, 0.83, 0.35)
    renderer.ResetCamera()

    interactor.Initialize()
    interactor.Start()
