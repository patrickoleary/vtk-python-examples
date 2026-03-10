#!/usr/bin/env python

# Clip a superquadric with a plane using vtkClipPolyData, showing the
# retained surface with a tomato back-face color and the clipped-away
# portion as a faint translucent ghost.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
tomato_rgb = (1.000, 0.388, 0.278)
silver_rgb = (0.753, 0.753, 0.753)

# Source: generate a superquadric
superquadric_source = vtkSuperquadricSource()
superquadric_source.SetPhiRoundness(3.1)
superquadric_source.SetThetaRoundness(2.2)

# Clip plane: diagonal plane through the origin
clip_plane = vtkPlane()
clip_plane.SetNormal(1.0, -1.0, -1.0)
clip_plane.SetOrigin(0.0, 0.0, 0.0)

# Clip: remove everything on the positive side of the plane
clipper = vtkClipPolyData()
clipper.SetInputConnection(superquadric_source.GetOutputPort())
clipper.SetClipFunction(clip_plane)
clipper.GenerateClippedOutputOn()

# Mapper: map the retained surface to graphics primitives
retained_mapper = vtkPolyDataMapper()
retained_mapper.SetInputConnection(clipper.GetOutputPort())

# Back-face property: flat tomato color for interior faces
back_faces = vtkProperty()
back_faces.SetSpecular(0.0)
back_faces.SetDiffuse(0.0)
back_faces.SetAmbient(1.0)
back_faces.SetAmbientColor(tomato_rgb)

# Actor: retained half with back-face coloring
retained_actor = vtkActor()
retained_actor.SetMapper(retained_mapper)
retained_actor.SetBackfaceProperty(back_faces)

# Mapper: map the clipped-away portion
clipped_mapper = vtkPolyDataMapper()
clipped_mapper.SetInputData(clipper.GetClippedOutput())
clipped_mapper.ScalarVisibilityOff()

# Actor: clipped-away portion as a faint translucent ghost
clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetDiffuseColor(silver_rgb)
clipped_actor.GetProperty().SetOpacity(0.1)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(retained_actor)
renderer.AddActor(clipped_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SolidClip")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
