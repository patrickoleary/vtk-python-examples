#!/usr/bin/env python

# Demonstrate vtkStreamTracer with vtkClosestNPointsStrategy on
# incompatible meshes (hanging and duplicate nodes) created by
# appending three image data volumes of different resolutions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkClosestNPointsStrategy,
    vtkImageData,
)
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersCore import vtkAppendFilter
from vtkmodules.vtkFiltersFlowPaths import (
    vtkCompositeInterpolatedVelocityField,
    vtkStreamTracer,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

dim = 40
num_streamlines = 50

# Create three volumes of different resolution butted together
spacing = 1.0 / (2.0 * dim - 1.0)
volume_1 = vtkImageData()
volume_1.SetOrigin(0.0, 0, 0)
volume_1.SetDimensions(2 * dim, 2 * dim, 2 * dim)
volume_1.SetSpacing(spacing, spacing, spacing)

spacing = 1.0 / (dim - 1.0)
volume_2 = vtkImageData()
volume_2.SetOrigin(1.0, 0, 0)
volume_2.SetDimensions(dim, dim, dim)
volume_2.SetSpacing(spacing, spacing, spacing)

spacing = 1.0 / (2.0 * dim - 1.0)
volume_3 = vtkImageData()
volume_3.SetOrigin(2.0, 0, 0)
volume_3.SetDimensions(2 * dim, 2 * dim, 2 * dim)
volume_3.SetSpacing(spacing, spacing, spacing)

# Append volumes to create unstructured grid with hanging/duplicate points
append = vtkAppendFilter()
append.AddInputData(volume_1)
append.AddInputData(volume_2)
append.AddInputData(volume_3)
append.MergePointsOff()
append.Update()

# Create uniform vector field in the x-direction
num_pts = append.GetOutput().GetNumberOfPoints()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(num_pts)
for i in range(num_pts):
    vectors.SetTuple3(i, 1, 0, 0)

append.GetOutput().GetPointData().SetVectors(vectors)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(append.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Seed line
pt1 = [0.001, 0.1, 0.5]
pt2 = [0.001, 0.9, 0.5]
line = vtkLineSource()
line.SetResolution(num_streamlines - 1)
line.SetPoint1(pt1)
line.SetPoint2(pt2)
line.Update()

# Stream tracer with ClosestNPointsStrategy
rk4 = vtkRungeKutta4()
strategy = vtkClosestNPointsStrategy()
ivp = vtkCompositeInterpolatedVelocityField()
ivp.SetFindCellStrategy(strategy)

streamer = vtkStreamTracer()
streamer.SetInputConnection(append.GetOutputPort())
streamer.SetSourceConnection(line.GetOutputPort())
streamer.SetMaximumPropagation(10)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()
streamer.SetMinimumIntegrationStep(0.01)
streamer.SetMaximumIntegrationStep(0.5)
streamer.SetTerminalSpeed(1.0e-12)
streamer.SetMaximumError(1.0e-06)
streamer.SetComputeVorticity(0)
streamer.SetIntegrator(rk4)
streamer.SetInterpolatorPrototype(ivp)
streamer.Update()

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(streamer.GetOutputPort())

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(stream_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 300)
render_window.SetWindowName("find cell")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2)

interactor.Initialize()
interactor.Start()
