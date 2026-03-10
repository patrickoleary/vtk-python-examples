#!/usr/bin/env python

# Clip a sphere source with an implicit plane using vtkClipPolyData,
# showing the clipped surface with a back-face color on the cut interior.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
peach_puff_rgb = (1.000, 0.855, 0.725)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)

# Implicit function: a plane through the origin with normal along X
clip_plane = vtkPlane()
clip_plane.SetOrigin(0.0, 0.0, 0.0)
clip_plane.SetNormal(1.0, 0.0, 0.0)

# Clip: remove everything on the positive side of the plane
clipper = vtkClipPolyData()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetClipFunction(clip_plane)
clipper.GenerateClippedOutputOn()

# Mapper: map the clipped surface to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry with front/back colors
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.GetProperty().BackfaceCullingOff()

# Mapper for the clipped-away part (the other half)
clipped_mapper = vtkPolyDataMapper()
clipped_mapper.SetInputConnection(clipper.GetClippedOutputPort())
clipped_mapper.ScalarVisibilityOff()

clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetColor(tomato_rgb)
clipped_actor.GetProperty().SetOpacity(0.3)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(clipped_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipWithImplicitFunction")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
