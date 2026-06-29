#!/usr/bin/env python

# Demonstrate vtkAttributeSmoothingFilter on general datasets:
# 2D unstructured grid (original and smoothed) and 3D image data
# (Mandelbrot source, original and smoothed).

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkSphere,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkAttributeSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
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
    s.SetTuple1(x + 1 * res, 1)
    s.SetTuple1(x + (res - 2) * res, 1)
    s.SetTuple1(x + 0 * res, 0)
    s.SetTuple1(x + (res - 1) * res, 0)

# Set column values
for y in range(0, res):
    s.SetTuple1(1 + y * res, 1)
    s.SetTuple1((res - 2) + y * res, 1)
    s.SetTuple1(0 + y * res, 0)
    s.SetTuple1((res - 1) + y * res, 0)

# Set center point
s.SetTuple1(int(res / 2) + int(res / 2) * res, 0)

# Convert poly data to unstructured grid
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1000000)

extract = vtkExtractGeometry()
extract.SetInputData(pd)
extract.SetImplicitFunction(sphere)
extract.Update()

# Viewport 0: original 2D unstructured grid
mapper_0 = vtkDataSetMapper()
mapper_0.SetInputConnection(extract.GetOutputPort())
mapper_0.SetScalarRange(0, 4)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Viewport 1: smoothed 2D unstructured grid
att_1 = vtkAttributeSmoothingFilter()
att_1.SetInputConnection(extract.GetOutputPort())
att_1.SetSmoothingStrategyToAllButBoundary()
att_1.SetNumberOfIterations(20)
att_1.SetRelaxationFactor(0.1)
att_1.Update()

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(att_1.GetOutputPort())
mapper_1.SetScalarRange(0, 4)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Viewport 2: 3D Mandelbrot original
mandel = vtkImageMandelbrotSource()
mandel.SetWholeExtent(-res, res, -res, res, -res, res)
mandel.Update()

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(mandel.GetOutputPort())
mapper_2.SetScalarRange(1, 8)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Viewport 3: 3D Mandelbrot smoothed
att_3 = vtkAttributeSmoothingFilter()
att_3.SetInputConnection(mandel.GetOutputPort())
att_3.SetSmoothingStrategyToAllPoints()
att_3.SetNumberOfIterations(50)
att_3.SetRelaxationFactor(0.1)
att_3.Update()

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(att_3.GetOutputPort())
mapper_3.SetScalarRange(1, 8)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.5)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1, 1)
renderer_3.AddActor(actor_3)
renderer_3.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("attribute smoothing general")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_2.GetActiveCamera().SetPosition(-1, 1, 1)
renderer_2.ResetCamera()
renderer_3.SetActiveCamera(renderer_2.GetActiveCamera())

interactor.Initialize()
interactor.Start()
