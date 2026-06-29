#!/usr/bin/env python

# Demonstrate vtkPointSetStreamer streaming a sphere point set into
# buckets, rendering the first non-empty bucket.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometryPreview import vtkPointSetStreamer
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# High-resolution sphere
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.5)
sphere.SetPhiResolution(2000)
sphere.SetThetaResolution(2000)

# Stream into buckets of 75000 points
streamer = vtkPointSetStreamer()
streamer.SetInputConnection(sphere.GetOutputPort())
streamer.SetNumberOfPointsPerBucket(75000)
streamer.Update()

# Find the first non-empty bucket
for i in range(streamer.GetNumberOfBuckets()):
    streamer.SetBucketId(i)
    streamer.Update()
    if streamer.GetOutput().GetNumberOfPoints() > 0:
        break

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(streamer.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("pointset streamer")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
