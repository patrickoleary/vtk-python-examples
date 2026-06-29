#!/usr/bin/env python

# Test vtkDiscretizableColorTransferFunction GetRange methods with a colored sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Discretizable color transfer function
cmap = vtkDiscretizableColorTransferFunction()
cmap.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
cmap.AddRGBPoint(0.5, 0.0, 1.0, 0.0)
cmap.AddRGBPoint(1.0, 1.0, 0.0, 0.0)
cmap.SetDiscretize(1)
cmap.SetNumberOfValues(8)

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
sphere_mapper.SetLookupTable(cmap)
sphere_mapper.SetScalarRange(0.0, 1.0)

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

renderer = vtkRenderer()
renderer.AddActor(sphere_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("get range discretizable color transfer function")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
