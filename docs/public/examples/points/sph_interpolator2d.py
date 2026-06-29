#!/usr/bin/env python

# Demonstrate vtkSPHInterpolator with a 2D quintic kernel by reading 2D
# SPH particle data and interpolating onto a probe plane.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkSPHInterpolator,
    vtkSPHQuinticKernel,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Parameters
res = 250

# Read 2D SPH particle data
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "SPH_Points2D.vtu"))
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetPointData().GetArray("Rho").GetRange()
print("Scalar range: {}".format(scalar_range))

# Probe plane
center = output.GetCenter()
bounds = output.GetBounds()

plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.SetOrigin(bounds[0], bounds[2], bounds[4])
plane.SetPoint1(bounds[1], bounds[2], bounds[4])
plane.SetPoint2(bounds[0], bounds[3], bounds[4])
plane.SetCenter(center)
plane.SetNormal(0, 0, 1)
plane.Update()

# 2D SPH quintic kernel
sph_kernel = vtkSPHQuinticKernel()
sph_kernel.SetSpatialStep(0.00002)
sph_kernel.SetDimension(2)

interpolator = vtkSPHInterpolator()
interpolator.SetInputConnection(plane.GetOutputPort())
interpolator.SetSourceConnection(reader.GetOutputPort())
interpolator.SetKernel(sph_kernel)
interpolator.Update()

timer = vtkTimerLog()
timer.StartTimer()
interpolator.Update()
timer.StopTimer()
print("Interpolate Points (SPH): {0}".format(timer.GetElapsedTime()))

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(interpolator.GetOutputPort())
interpolator_mapper.SetScalarModeToUsePointFieldData()
interpolator_mapper.SelectColorArray("Rho")
interpolator_mapper.SetScalarRange(750, 1050)

interpolator_actor = vtkActor()
interpolator_actor.SetMapper(interpolator_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(interpolator_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("sph interpolator2d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
