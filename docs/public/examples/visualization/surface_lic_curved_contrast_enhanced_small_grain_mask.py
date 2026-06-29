#!/usr/bin/env python

# Test vtkCompositeSurfaceLICMapper: SurfaceLICCurvedContrastEnhancedSmallGrainMask.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math
import os

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
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

# Compute vector magnitude for coloring
mag_range = [float("inf"), float("-inf")]
mag_name = None
if hasattr(data_obj, "NewIterator"):
    it = data_obj.NewIterator()
    it.InitTraversal()
    while not it.IsDoneWithTraversal():
        ds = it.GetCurrentDataObject()
        if ds and ds.GetNumberOfCells() > 0:
            v = ds.GetPointData().GetArray("V")
            if v is not None:
                mag = vtkFloatArray()
                mag.SetName("magV")
                mag.SetNumberOfTuples(v.GetNumberOfTuples())
                for j in range(v.GetNumberOfTuples()):
                    s = sum(v.GetComponent(j, c) ** 2 for c in range(v.GetNumberOfComponents()))
                    mag.SetValue(j, math.sqrt(s))
                ds.GetPointData().SetScalars(mag)
                mag_name = mag.GetName()
                r = mag.GetRange()
                mag_range[0] = min(mag_range[0], r[0])
                mag_range[1] = max(mag_range[1], r[1])
        it.GoToNextItem()
else:
    if data_obj.GetNumberOfCells() > 0:
        v = data_obj.GetPointData().GetArray("V")
        if v is not None:
            mag = vtkFloatArray()
            mag.SetName("magV")
            mag.SetNumberOfTuples(v.GetNumberOfTuples())
            for j in range(v.GetNumberOfTuples()):
                s = sum(v.GetComponent(j, c) ** 2 for c in range(v.GetNumberOfComponents()))
                mag.SetValue(j, math.sqrt(s))
            data_obj.GetPointData().SetScalars(mag)
            mag_name = mag.GetName()
            r = mag.GetRange()
            mag_range = [r[0], r[1]]

lut = vtkDiscretizableColorTransferFunction()
lut.SetColorSpaceToRGB()
lut.AddRGBPoint(mag_range[0], 0.0, 0.0, 1.0)
lut.AddRGBPoint(mag_range[1], 1.0, 0.0, 0.0)
lut.SetColorSpaceToDiverging()
lut.Build()
lut.SetDiscretize(True)
lut.SetNumberOfValues(256)
lic_mapper.SetLookupTable(lut)
lic_mapper.SetScalarModeToUsePointData()
lic_mapper.SetScalarVisibility(1)
lic_mapper.SelectColorArray(mag_name)
lic_mapper.SetUseLookupTableScalarRange(1)
lic_mapper.SetScalarModeToUsePointFieldData()
lic_mapper.SetInterpolateScalarsBeforeMapping(0)

# LIC interface parameters
lic_interface = lic_mapper.GetLICInterface()
lic_interface.SetNumberOfSteps(40)
lic_interface.SetStepSize(0.4)
lic_interface.SetEnhancedLIC(1)
lic_interface.SetNormalizeVectors(1)
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
lic_interface.SetLowLICContrastEnhancementFactor(0.0)
lic_interface.SetHighLICContrastEnhancementFactor(0.0)
lic_interface.SetLowColorContrastEnhancementFactor(0.0)
lic_interface.SetHighColorContrastEnhancementFactor(0.0)
lic_interface.SetAntiAlias(0)
lic_interface.SetColorMode(0)
lic_interface.SetLICIntensity(0.6)
lic_interface.SetMapModeBias(0.0)
lic_interface.SetMaskOnSurface(0)
lic_interface.SetMaskThreshold(0.0)
lic_interface.SetMaskIntensity(0.2)
lic_interface.SetMaskColor([1.0, 1.0, 1.0])

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
render_window.SetWindowName("surface lic curved contrast enhanced small grain mask")

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
