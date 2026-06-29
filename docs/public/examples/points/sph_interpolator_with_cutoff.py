#!/usr/bin/env python

# Demonstrate vtkSPHInterpolator with a cutoff array by reading SPH
# particle data, adding mass and cutoff arrays via numpy, and
# interpolating onto a probe plane.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import numpy as np

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
from vtkmodules.numpy_interface import dataset_adapter as dsa

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Parameters
res = 250

# Read SPH particle data
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "SPH_Points.vtu"))
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetPointData().GetArray("Rho").GetRange()

# Add mass array
output_2 = dsa.WrapDataObject(output)
mass = np.ones(output.GetNumberOfPoints()) * 1.0
output_2.PointData.append(mass, "Mass")

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
plane.Push(1.15)
plane.Update()
plane_output = plane.GetOutput()
plane_output_2 = dsa.WrapDataObject(plane_output)

# The constant value in the Cutoff array is equal to
# the spatialStep (0.1) and the CutoffFactor (3) of the QuinticKernel.
cutoff = np.ones(plane_output.GetNumberOfPoints()) * 3.0 / 10.0
plane_output_2.PointData.append(cutoff, "Cutoff")

# SPH quintic kernel
sph_kernel = vtkSPHQuinticKernel()
sph_kernel.SetSpatialStep(0.1)

interpolator = vtkSPHInterpolator()
interpolator.SetInputConnection(plane.GetOutputPort())
interpolator.SetSourceConnection(reader.GetOutputPort())
interpolator.SetDensityArrayName("Rho")
interpolator.SetMassArrayName("Mass")
interpolator.SetCutoffArrayName("Cutoff")
interpolator.SetKernel(sph_kernel)

timer = vtkTimerLog()
timer.StartTimer()
interpolator.Update()
timer.StopTimer()
print("Interpolate Points (SPH): {0}".format(timer.GetElapsedTime()))

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(interpolator.GetOutputPort())
interpolator_mapper.SetScalarModeToUsePointFieldData()
interpolator_mapper.SelectColorArray("Rho")
interpolator_mapper.SetScalarRange(interpolator.GetOutput().GetPointData().GetArray("Rho").GetRange())

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
render_window.SetWindowName("sph interpolator with cutoff")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
