#!/usr/bin/env python

# Decimate a sphere using vtkDecimatePro with 90% target reduction.
# Side-by-side viewports show the original mesh (left) and the
# decimated mesh (right), both with flat shading and gold back-faces.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkDecimatePro
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peru_background_rgb = (0.804, 0.522, 0.247)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
navajo_white_rgb = (1.000, 0.871, 0.678)
gold_rgb = (1.000, 0.843, 0.000)

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(15)
sphere.Update()
input_poly_data = sphere.GetOutput()

# Decimate: reduce the polygon count by 90%
decimate = vtkDecimatePro()
decimate.SetInputData(input_poly_data)
decimate.SetTargetReduction(0.9)
decimate.PreserveTopologyOn()
decimate.Update()

# Back-face property: gold for both viewports
back_face = vtkProperty()
back_face.SetColor(gold_rgb)

# Mapper: original sphere
input_mapper = vtkPolyDataMapper()
input_mapper.SetInputData(input_poly_data)

input_actor = vtkActor()
input_actor.SetMapper(input_mapper)
input_actor.GetProperty().SetInterpolationToFlat()
input_actor.GetProperty().SetColor(navajo_white_rgb)
input_actor.SetBackfaceProperty(back_face)

# Mapper: decimated sphere
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimate.GetOutputPort())

decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetInterpolationToFlat()
decimated_actor.GetProperty().SetColor(navajo_white_rgb)
decimated_actor.SetBackfaceProperty(back_face)

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Elevation(30)
camera.Azimuth(30)

# Left renderer: original mesh
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(peru_background_rgb)
left_renderer.AddActor(input_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: decimated mesh
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(decimated_actor)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Decimation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
