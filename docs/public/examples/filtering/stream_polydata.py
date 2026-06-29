#!/usr/bin/env python

# Stream a sphere through quadric clustering and polydata streamer,
# splitting into multiple pieces for processing.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePro,
    vtkPolyDataNormals,
    vtkQuadricClustering,
)
from vtkmodules.vtkFiltersGeneral import vtkPolyDataStreamer
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

number_of_pieces = 5

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetRadius(3)
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(150)

# Decimate the sphere
decimate = vtkDecimatePro()
decimate.SetInputConnection(sphere.GetOutputPort())
decimate.BoundaryVertexDeletionOff()

# Quadric clustering to reduce geometry
quadric = vtkQuadricClustering()
quadric.SetInputConnection(sphere.GetOutputPort())
quadric.SetNumberOfXDivisions(5)
quadric.SetNumberOfYDivisions(5)
quadric.SetNumberOfZDivisions(10)
quadric.UseInputPointsOn()

# Stream the data in pieces
streamer = vtkPolyDataStreamer()
streamer.SetInputConnection(quadric.GetOutputPort())
streamer.SetNumberOfStreamDivisions(number_of_pieces)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(streamer.GetOutputPort())
mapper.ScalarVisibilityOff()
mapper.SetPiece(0)
mapper.SetNumberOfPieces(2)

# Actor
colors = vtkNamedColors()
rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("english_red", rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("stream polydata")

# Scene
renderer.GetActiveCamera().SetPosition(5, 5, 10)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
