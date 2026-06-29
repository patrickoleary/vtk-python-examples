#!/usr/bin/env python

# Demonstrate vtkStatisticalOutlierRemoval by creating a random point
# cloud with six deliberate outliers, removing statistically isolated
# points, and rendering non-outliers and outliers in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPolyData,
    vtkStaticPointLocator,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import vtkStatisticalOutlierRemoval
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 20000
math = vtkMath()
math.RandomSeed(31415)

# Create random point cloud with six outliers
point_positions = vtkPoints()
point_positions.SetDataTypeToFloat()
point_positions.SetNumberOfPoints(n_pts + 6)
scalars = vtkFloatArray()
scalars.SetNumberOfTuples(n_pts + 6)
scalars.SetName("scalars")
for i in range(0, n_pts):
    point_positions.SetPoint(i, math.Random(-1, 1), math.Random(-1, 1), math.Random(-1, 1))
    scalars.SetValue(i, math.Random(0, 1))

point_positions.SetPoint(n_pts, -5, 0, 0)
scalars.SetValue(n_pts, 0.5)
point_positions.SetPoint(n_pts + 1, 5, 0, 0)
scalars.SetValue(n_pts + 1, 0.5)
point_positions.SetPoint(n_pts + 2, 0, -5, 0)
scalars.SetValue(n_pts + 2, 0.5)
point_positions.SetPoint(n_pts + 3, 0, 5, 0)
scalars.SetValue(n_pts + 3, 0.5)
point_positions.SetPoint(n_pts + 4, 0, 0, -5)
scalars.SetValue(n_pts + 4, 0.5)
point_positions.SetPoint(n_pts + 5, 0, 0, 5)
scalars.SetValue(n_pts + 5, 0.5)

polydata = vtkPolyData()
polydata.SetPoints(point_positions)
polydata.GetPointData().SetScalars(scalars)

# Reuse locator
locator = vtkStaticPointLocator()
locator.SetDataSet(polydata)
locator.BuildLocator()

# Remove statistically isolated points
removal = vtkStatisticalOutlierRemoval()
removal.SetInputData(polydata)
removal.SetLocator(locator)
removal.SetSampleSize(20)
removal.SetStandardDeviationFactor(1.5)
removal.GenerateOutliersOn()

timer = vtkTimerLog()
timer.StartTimer()
removal.Update()
timer.StopTimer()
print("Number of points processed: {0}".format(n_pts))
print("   Time to remove outliers: {0}".format(timer.GetElapsedTime()))
print("   Number removed: {0}".format(removal.GetNumberOfPointsRemoved()))
print("   Computed mean: {0}".format(removal.GetComputedMean()))
print("   Computed standard deviation: {0}".format(removal.GetComputedStandardDeviation()))

# Non-outliers
removal_mapper = vtkPointGaussianMapper()
removal_mapper.SetInputConnection(removal.GetOutputPort())
removal_mapper.EmissiveOff()
removal_mapper.SetScaleFactor(0.0)

removal_actor = vtkActor()
removal_actor.SetMapper(removal_mapper)

outline = vtkOutlineFilter()
outline.SetInputData(polydata)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Outliers
outlier_mapper = vtkPointGaussianMapper()
outlier_mapper.SetInputConnection(removal.GetOutputPort(1))
outlier_mapper.EmissiveOff()
outlier_mapper.SetScaleFactor(0.0)

outlier_actor = vtkActor()
outlier_actor.SetMapper(outlier_mapper)

outline_1 = vtkOutlineFilter()
outline_1.SetInputData(polydata)

outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())

outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(removal_actor)
renderer_0.AddActor(outline_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(outlier_actor)
renderer_1.AddActor(outline_actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("statistical outlier removal cloud")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetFocalPoint(1, 1, 1)
camera.SetPosition(0, 0, 0)
renderer_0.ResetCamera()

renderer_1.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
