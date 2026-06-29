#!/usr/bin/env python

# Test vtkLookupTable GetRange methods with a colored sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Lookup table
lut = vtkLookupTable()
lut.SetRange(0.0, 1.0)
lut.SetHueRange(0.667, 0.0)
lut.SetSaturationRange(1.0, 1.0)
lut.SetAlphaRange(1.0, 1.0)
lut.Build()

# Sphere with elevation scalars
sphere = vtkSphereSource()
sphere.SetPhiResolution(32)
sphere.SetThetaResolution(32)

elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())
elevation.SetLowPoint(0, -0.5, 0)
elevation.SetHighPoint(0, 0.5, 0)
elevation.SetScalarRange(0.0, 1.0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(elevation.GetOutputPort())
sphere_mapper.SetLookupTable(lut)
sphere_mapper.SetScalarRange(0.0, 1.0)

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

renderer = vtkRenderer()
renderer.AddActor(sphere_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("get range lookup table")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
