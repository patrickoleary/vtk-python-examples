#!/usr/bin/env python

# Demonstrate vtkEuclideanClusterExtraction by sampling points from a
# cylinder, plane, and sphere, then extracting all clusters from the
# combined point cloud.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersModeling import vtkPolyDataPointSampler
from vtkmodules.vtkFiltersPoints import vtkEuclideanClusterExtraction
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cylinder
cylinder = vtkCylinderSource()
cylinder.SetCenter(-2, 0, 0)
cylinder.SetRadius(0.02)
cylinder.SetHeight(1.8)
cylinder.SetResolution(24)

# Create a plane
plane = vtkPlaneSource()
plane.SetOrigin(-1, -0.5, 0)
plane.SetPoint1(0.5, -0.5, 0)
plane.SetPoint2(-1, 0.5, 0)

# Create a sphere
sphere = vtkSphereSource()
sphere.SetCenter(2, 0, 0)
sphere.SetRadius(0.8)
sphere.SetThetaResolution(96)
sphere.SetPhiResolution(48)

# Combine
append = vtkAppendPolyData()
append.AddInputConnection(cylinder.GetOutputPort())
append.AddInputConnection(plane.GetOutputPort())
append.AddInputConnection(sphere.GetOutputPort())

# Sample points along surfaces
sampler = vtkPolyDataPointSampler()
sampler.SetInputConnection(append.GetOutputPort())
sampler.SetDistance(0.025)
sampler.Update()

# Extract clusters
cluster_extract = vtkEuclideanClusterExtraction()
cluster_extract.SetInputConnection(sampler.GetOutputPort())
cluster_extract.SetRadius(0.1)
cluster_extract.ColorClustersOn()
cluster_extract.SetExtractionModeToAllClusters()

timer = vtkTimerLog()
timer.StartTimer()
cluster_extract.Update()
timer.StopTimer()
print("Points processed: {0}".format(sampler.GetOutput().GetNumberOfPoints()))
print("   Time to segment objects: {0}".format(timer.GetElapsedTime()))
print("   Number of clusters: {0}".format(cluster_extract.GetNumberOfExtractedClusters()))

cluster_mapper = vtkPointGaussianMapper()
cluster_mapper.SetInputConnection(cluster_extract.GetOutputPort(0))
cluster_mapper.EmissiveOff()
cluster_mapper.SetScaleFactor(0.0)
cluster_mapper.SetScalarRange(0, 2)

cluster_actor = vtkActor()
cluster_actor.SetMapper(cluster_mapper)
cluster_actor.AddPosition(0, 2.25, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cluster_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("euclidean cluster extraction")

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
