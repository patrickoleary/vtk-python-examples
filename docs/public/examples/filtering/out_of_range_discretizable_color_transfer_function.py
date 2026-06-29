#!/usr/bin/env python

# Test vtkDiscretizableColorTransferFunction with below/above range colors.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Color map with below/above range colors
cmap = vtkDiscretizableColorTransferFunction()
cmap.AddRGBPoint(-0.4, 0.8, 0.8, 0.8)
cmap.AddRGBPoint(0.4, 1, 0, 0)
cmap.SetUseBelowRangeColor(0)
cmap.SetBelowRangeColor(0.0, 1.0, 0.0)
cmap.SetUseAboveRangeColor(0)
cmap.SetAboveRangeColor(1.0, 1.0, 0.0)

# Sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(32)
sphere.SetThetaResolution(32)
sphere.Update()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_mapper.SetScalarModeToUsePointFieldData()
sphere_mapper.SelectColorArray("Normals")
sphere_mapper.ColorByArrayComponent("Normals", 0)
sphere_mapper.SetLookupTable(cmap)
sphere_mapper.UseLookupTableScalarRangeOn()
sphere_mapper.InterpolateScalarsBeforeMappingOn()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

renderer = vtkRenderer()
renderer.AddActor(sphere_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("out of range discretizable color transfer function")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
