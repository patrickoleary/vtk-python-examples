#!/usr/bin/env python

# Demonstrate vtkEuclideanClusterExtraction with scalar connectivity by
# sampling implicit functions (cylinder, box, sphere) on a bounded point
# source and extracting the largest cluster within a scalar range.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkBox,
    vtkCylinder,
    vtkImplicitBoolean,
    vtkSphere,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersGeneral import vtkSampleImplicitFunctionFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkEuclideanClusterExtraction,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 100000
math = vtkMath()
math.RandomSeed(31415)

# Create bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.SetBounds(-3, 3, -1, 1, -1, 1)
points.ProduceRandomScalarsOff()
points.ProduceCellOutputOff()

# Implicit functions
cylinder = vtkCylinder()
cylinder.SetCenter(-2, 0, 0)
cylinder.SetRadius(0.02)

box = vtkBox()
box.SetBounds(-1, 0.5, -0.5, 0.5, -0.0005, 0.0005)

sphere = vtkSphere()
sphere.SetCenter(2, 0, 0)
sphere.SetRadius(0.8)

# Boolean union
boolean_func = vtkImplicitBoolean()
boolean_func.SetOperationTypeToUnion()
boolean_func.AddFunction(cylinder)
boolean_func.AddFunction(box)
boolean_func.AddFunction(sphere)

# Sample implicit function to generate scalars
sample = vtkSampleImplicitFunctionFilter()
sample.SetInputConnection(points.GetOutputPort())
sample.SetImplicitFunction(boolean_func)
sample.Update()

# Extract largest cluster with scalar connectivity
cluster_extract = vtkEuclideanClusterExtraction()
cluster_extract.SetInputConnection(sample.GetOutputPort())
cluster_extract.SetRadius(0.15)
cluster_extract.SetExtractionModeToLargestCluster()
cluster_extract.ScalarConnectivityOn()
cluster_extract.SetScalarRange(-0.64, -0.3)

timer = vtkTimerLog()
timer.StartTimer()
cluster_extract.Update()
timer.StopTimer()
print("Points processed: {0}".format(points.GetOutput().GetNumberOfPoints()))
print("   Time to segment objects: {0}".format(timer.GetElapsedTime()))
print("   Number of clusters: {0}".format(cluster_extract.GetNumberOfExtractedClusters()))

cluster_mapper = vtkPointGaussianMapper()
cluster_mapper.SetInputConnection(cluster_extract.GetOutputPort(0))
cluster_mapper.EmissiveOff()
cluster_mapper.SetScaleFactor(0.0)
cluster_mapper.SetScalarRange(-0.64, 2.25)

cluster_actor = vtkActor()
cluster_actor.SetMapper(cluster_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cluster_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("euclidean cluster scalar")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, -1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
