#!/usr/bin/env python

# Save and restore camera state using a JSON file.

import json
import tempfile

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
crimson_rgb = (0.863, 0.078, 0.235)
silver_rgb = (0.753, 0.753, 0.753)

# Source: a cone (procedural, no external data needed)
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(crimson_rgb)
actor.GetProperty().SetSpecular(0.6)
actor.GetProperty().SetSpecularPower(30)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_rgb)
renderer.ResetCamera()

# Camera: set up an interesting viewpoint
camera = renderer.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(20)
renderer.ResetCameraClippingRange()

# SaveScene: write camera parameters to a temporary JSON file
scene = {
    "FocalPoint": list(camera.GetFocalPoint()),
    "Position": list(camera.GetPosition()),
    "ViewUp": list(camera.GetViewUp()),
    "ViewAngle": camera.GetViewAngle(),
    "ClippingRange": list(camera.GetClippingRange()),
}

scene_file = tempfile.NamedTemporaryFile(
    mode="w", suffix=".json", prefix="vtk_scene_", delete=False
)
json.dump(scene, scene_file, indent=2)
scene_file.close()

# Scramble the camera to prove the restore works
camera.SetPosition(0, 0, 10)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 1, 0)

# RestoreScene: read camera parameters back from the JSON file
with open(scene_file.name, "r") as f:
    restored = json.load(f)

camera.SetFocalPoint(restored["FocalPoint"])
camera.SetPosition(restored["Position"])
camera.SetViewUp(restored["ViewUp"])
camera.SetViewAngle(restored["ViewAngle"])
camera.SetClippingRange(restored["ClippingRange"])

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SaveSceneToFile")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
