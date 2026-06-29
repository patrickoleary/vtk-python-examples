#!/usr/bin/env python

# Demonstrate vtkSPHInterpolator with a quintic kernel by reading SPH
# particle data from a VTU file and interpolating onto a probe plane.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
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

# Read SPH particle data
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "SPH_Points.vtu"))
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetPointData().GetArray("Rho").GetRange()

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

# First test with empty input
empty_points = vtkPoints()
empty_data = vtkPolyData()
empty_data.SetPoints(empty_points)

sph_kernel = vtkSPHQuinticKernel()
sph_kernel.SetSpatialStep(0.1)

interpolator = vtkSPHInterpolator()
interpolator.SetInputConnection(plane.GetOutputPort())
interpolator.SetSourceData(empty_data)
interpolator.SetKernel(sph_kernel)
interpolator.Update()

# Now with actual data
interpolator.SetInputConnection(plane.GetOutputPort())
interpolator.SetSourceConnection(reader.GetOutputPort())

timer = vtkTimerLog()
timer.StartTimer()
interpolator.Update()
timer.StopTimer()
print("Interpolate Points (SPH): {0}".format(timer.GetElapsedTime()))

interpolator_mapper = vtkPolyDataMapper()
interpolator_mapper.SetInputConnection(interpolator.GetOutputPort())
interpolator_mapper.SetScalarModeToUsePointFieldData()
interpolator_mapper.SelectColorArray("Rho")
interpolator_mapper.SetScalarRange(0, 720)

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
render_window.SetWindowName("sph interpolator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
