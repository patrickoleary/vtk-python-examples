#!/usr/bin/env python

# Test vtkLookupTable with SetTable and below/above range colors.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create grayscale table
colors = vtkUnsignedCharArray()
colors.SetNumberOfComponents(4)
colors.SetNumberOfTuples(256)
for i in range(256):
    colors.SetTuple(i, (i, i, i, 255))

table = vtkLookupTable()
table.SetNumberOfColors(256)
table.SetRange(-0.5, 0.5)
table.SetTable(colors)
table.SetBelowRangeColor(1, 0, 0, 1)
table.SetAboveRangeColor(0, 1, 0, 1)
table.SetUseBelowRangeColor(0)
table.SetUseAboveRangeColor(0)

# Sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(32)
sphere.SetThetaResolution(32)
sphere.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Normals")
mapper.ColorByArrayComponent("Normals", 0)
mapper.SetLookupTable(table)
mapper.UseLookupTableScalarRangeOn()
mapper.InterpolateScalarsBeforeMappingOn()

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("set table out of range lookup table")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
