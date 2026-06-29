#!/usr/bin/env python

# Demonstrate vtkSelectEnclosedPoints by generating random points,
# testing which ones fall inside a sphere, thresholding the enclosed
# points, glyphing them as small spheres, and rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkRandomPool
from vtkmodules.vtkCommonDataModel import vtkDataObject, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkThresholdPoints
from vtkmodules.vtkFiltersModeling import vtkSelectEnclosedPoints
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a containing sphere surface
sphere = vtkSphereSource()
sphere.SetPhiResolution(25)
sphere.SetThetaResolution(38)
sphere.SetCenter(4.5, 5.5, 5.0)
sphere.SetRadius(2.5)

# Generate random points using vtkRandomPool
points = vtkPoints()
points.SetNumberOfPoints(500)

pool = vtkRandomPool()
da = points.GetData()
pool.PopulateDataArray(da, 0, 2.25, 7)
pool.PopulateDataArray(da, 1, 1, 10)
pool.PopulateDataArray(da, 2, 0.5, 10.5)

profile = vtkPolyData()
profile.SetPoints(points)

# Select points enclosed by the sphere
select = vtkSelectEnclosedPoints()
select.SetInputData(profile)
select.SetSurfaceConnection(sphere.GetOutputPort())

# Threshold to extract enclosed points
thresh = vtkThresholdPoints()
thresh.SetInputConnection(select.GetOutputPort())
thresh.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "SelectedPoints"
)
thresh.SetUpperThreshold(0.9)
thresh.SetThresholdFunction(vtkThresholdPoints.THRESHOLD_UPPER)

# Glyph enclosed points as small spheres
glyph_source = vtkSphereSource()

glypher = vtkGlyph3D()
glypher.SetInputConnection(thresh.GetOutputPort())
glypher.SetSourceConnection(glyph_source.GetOutputPort())
glypher.SetScaleModeToDataScalingOff()
glypher.SetScaleFactor(0.25)

# Mapper and actor for glyphed points
points_mapper = vtkPolyDataMapper()
points_mapper.SetInputConnection(glypher.GetOutputPort())
points_mapper.ScalarVisibilityOff()

points_actor = vtkActor()
points_actor.SetMapper(points_mapper)
points_actor.GetProperty().SetColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(points_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("select enclosed points")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
