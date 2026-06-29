#!/usr/bin/env python

# Demonstrate vtkExtractEnclosedPoints by generating random points and
# extracting those enclosed by a sphere surface, rendering extracted
# points as glyphed spheres.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
    vtkRandomPool,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersPoints import vtkExtractEnclosedPoints
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

num_pts = 500

# Enclosing sphere surface
enclosing_sphere = vtkSphereSource()
enclosing_sphere.SetPhiResolution(25)
enclosing_sphere.SetThetaResolution(38)
enclosing_sphere.SetCenter(4.5, 5.5, 5.0)
enclosing_sphere.SetRadius(2.5)

# Generate random points and scalars
points = vtkPoints()
points.SetNumberOfPoints(num_pts)

points_data = points.GetData()
pool = vtkRandomPool()
pool.PopulateDataArray(points_data, 0, 2.25, 7)
pool.PopulateDataArray(points_data, 1, 1, 10)
pool.PopulateDataArray(points_data, 2, 0.5, 10.5)

scalars = vtkFloatArray()
scalars.SetNumberOfTuples(num_pts)
scalars.SetName("Random Scalars")
pool.PopulateDataArray(scalars, 100, 200)

profile = vtkPolyData()
profile.SetPoints(points)
profile.GetPointData().SetScalars(scalars)

# Extract enclosed points
extract = vtkExtractEnclosedPoints()
extract.SetInputData(profile)
extract.SetSurfaceConnection(enclosing_sphere.GetOutputPort())

timer = vtkTimerLog()
timer.StartTimer()
extract.Update()
timer.StopTimer()
print("Time to extract points: {0}".format(timer.GetElapsedTime()))

# Glyph extracted points
glyph = vtkSphereSource()
glypher = vtkGlyph3D()
glypher.SetInputConnection(extract.GetOutputPort())
glypher.SetSourceConnection(glyph.GetOutputPort())
glypher.SetScaleModeToDataScalingOff()
glypher.SetScaleFactor(0.25)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(enclosing_sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetRepresentationToWireframe()

points_mapper = vtkPolyDataMapper()
points_mapper.SetInputConnection(glypher.GetOutputPort())
points_mapper.SetScalarRange(100, 200)

points_actor = vtkActor()
points_actor.SetMapper(points_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(points_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract enclosed")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
