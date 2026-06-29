#!/usr/bin/env python

# Test opacity mapping with vector data using vtkDiscretizableColorTransferFunction.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkCommand,
    vtkMath,
)
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Callback to reset random seed for reproducibility
def set_random_seed(caller, event_id):
    ra_math = vtkMath()
    ra_math.RandomSeed(6)

# Force a starting random value
set_random_seed(0, 0)

# Create color transfer function with opacity
opacity_transfer = vtkPiecewiseFunction()
opacity_transfer.AddPoint(0, 0)
opacity_transfer.AddPoint(0.6, 0)
opacity_transfer.AddPoint(1, 1)

lut = vtkDiscretizableColorTransferFunction()
lut.SetColorSpaceToDiverging()
lut.AddRGBPoint(0.0, 0.23, 0.299, 0.754)
lut.AddRGBPoint(1.0, 0.706, 0.016, 0.150)
lut.SetVectorModeToMagnitude()
lut.SetRange(0, 1)
lut.SetScalarOpacityFunction(opacity_transfer)
lut.EnableOpacityMappingOn()

# Sphere actor without interpolation
sphere_0 = vtkSphereSource()
brownian_0 = vtkBrownianPoints()
brownian_0.SetInputConnection(sphere_0.GetOutputPort())
brownian_0.AddObserver(vtkCommand.EndEvent, set_random_seed)
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(brownian_0.GetOutputPort())
mapper_0.SetScalarModeToUsePointFieldData()
mapper_0.SelectColorArray("BrownianVectors")
mapper_0.SetLookupTable(lut)
mapper_0.SetInterpolateScalarsBeforeMapping(0)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Sphere actor with interpolation
sphere_1 = vtkSphereSource()
sphere_1.SetCenter(-1, 0, 0)
brownian_1 = vtkBrownianPoints()
brownian_1.SetInputConnection(sphere_1.GetOutputPort())
brownian_1.AddObserver(vtkCommand.EndEvent, set_random_seed)
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(brownian_1.GetOutputPort())
mapper_1.SetScalarModeToUsePointFieldData()
mapper_1.SelectColorArray("BrownianVectors")
mapper_1.SetLookupTable(lut)
mapper_1.SetInterpolateScalarsBeforeMapping(1)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Renderer with depth peeling
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.UseDepthPeelingOn()
renderer.SetMaximumNumberOfPeels(4)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("opacity vectors")
render_window.SetMultiSamples(0)
render_window.AlphaBitPlanesOn()
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
