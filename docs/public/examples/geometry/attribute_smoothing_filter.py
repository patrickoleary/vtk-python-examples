#!/usr/bin/env python

# Demonstrate vtkAttributeSmoothingFilter with five smoothing
# strategies on synthetic scalar data: original, all points,
# all but boundary, adjacent to boundary, and smoothing mask.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersGeometry import vtkAttributeSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test size
res = 25

# Generate synthetic plane data
ps = vtkPlaneSource()
ps.SetXResolution(res - 1)
ps.SetYResolution(res - 1)
ps.Update()

pd = vtkPolyData()
pd.SetPoints(ps.GetOutput().GetPoints())
pd.SetPolys(ps.GetOutput().GetPolys())

# Create synthetic scalar data
s = vtkFloatArray()
s.SetNumberOfTuples(res * res)
s.Fill(4)
pd.GetPointData().SetScalars(s)

# Set row values
for x in range(0, res):
    s.SetTuple1(x + 1 * res, 1)  # Row 1
    s.SetTuple1(x + (res - 2) * res, 1)  # Row res-2
    s.SetTuple1(x + 0 * res, 0)  # Row 0
    s.SetTuple1(x + (res - 1) * res, 0)  # Row res-1

# Set column values
for y in range(0, res):
    s.SetTuple1(1 + y * res, 1)  # Column 1
    s.SetTuple1((res - 2) + y * res, 1)  # Column res-2
    s.SetTuple1(0 + y * res, 0)  # Column 0
    s.SetTuple1((res - 1) + y * res, 0)  # Column res-1

# Set center point
s.SetTuple1(int(res / 2) + int(res / 2) * res, 0)

# Viewport 0: original data
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(pd)
mapper_0.SetScalarRange(0, 4)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Viewport 1: smooth all points
att_1 = vtkAttributeSmoothingFilter()
att_1.SetInputData(pd)
att_1.SetSmoothingStrategyToAllPoints()
att_1.SetNumberOfIterations(50)
att_1.SetRelaxationFactor(0.1)
att_1.Update()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(att_1.GetOutputPort())
mapper_1.SetScalarRange(0, 4)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Viewport 2: smooth all but boundary
att_2 = vtkAttributeSmoothingFilter()
att_2.SetInputData(pd)
att_2.SetSmoothingStrategyToAllButBoundary()
att_2.SetNumberOfIterations(2)
att_2.SetRelaxationFactor(0.5)
att_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(att_2.GetOutputPort())
mapper_2.SetScalarRange(0, 4)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Viewport 3: smooth adjacent to boundary
att_3 = vtkAttributeSmoothingFilter()
att_3.SetInputData(pd)
att_3.SetSmoothingStrategyToAdjacentToBoundary()
att_3.SetNumberOfIterations(3)
att_3.SetRelaxationFactor(0.333)
att_3.Update()

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(att_3.GetOutputPort())
mapper_3.SetScalarRange(0, 4)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Viewport 4: smoothing mask (smooth all except center point)
smooth_array = vtkUnsignedCharArray()
smooth_array.SetNumberOfTuples(res * res)
smooth_array.Fill(1)
idx = int(res / 2) + int(res / 2) * res
smooth_array.SetTuple1(idx, 0)

att_4 = vtkAttributeSmoothingFilter()
att_4.SetInputData(pd)
att_4.SetSmoothingStrategyToSmoothingMask()
att_4.SetNumberOfIterations(50)
att_4.SetRelaxationFactor(0.10)
att_4.SetSmoothingMask(smooth_array)
att_4.Update()

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(att_4.GetOutputPort())
mapper_4.SetScalarRange(0, 4)

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

# Create renderers for five viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.20, 1)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.20, 0, 0.40, 1)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.40, 0, 0.60, 1)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.60, 0, 0.80, 1)
renderer_3.AddActor(actor_3)
renderer_3.SetBackground(0, 0, 0)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.80, 0, 1, 1)
renderer_4.AddActor(actor_4)
renderer_4.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(1000, 200)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.SetWindowName("attribute smoothing filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
