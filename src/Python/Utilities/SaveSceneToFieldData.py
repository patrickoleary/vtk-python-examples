#!/usr/bin/env python

# Save and restore camera state using polydata field data.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkStringArray
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
cone.Update()

poly_data = cone.GetOutput()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

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

# Camera: set up an interesting viewpoint and save it to field data
camera = renderer.GetActiveCamera()
camera.Azimuth(30)
camera.Elevation(20)
renderer.ResetCameraClippingRange()

# SaveScene: serialize camera parameters into a vtkStringArray stored
# in the polydata's field data. This allows the camera state to travel
# with the dataset.
fp_format = "{:.6f}"
buffer = ""
buffer += "Camera:FocalPoint " + ", ".join(fp_format.format(n) for n in camera.GetFocalPoint()) + "\n"
buffer += "Camera:Position " + ", ".join(fp_format.format(n) for n in camera.GetPosition()) + "\n"
buffer += "Camera:ViewUp " + ", ".join(fp_format.format(n) for n in camera.GetViewUp()) + "\n"
buffer += "Camera:ViewAngle " + fp_format.format(camera.GetViewAngle()) + "\n"
buffer += "Camera:ClippingRange " + ", ".join(fp_format.format(n) for n in camera.GetClippingRange()) + "\n"

camera_array = vtkStringArray()
camera_array.SetNumberOfValues(1)
camera_array.SetValue(0, buffer)
camera_array.SetName("Camera")
poly_data.GetFieldData().AddArray(camera_array)

# Scramble the camera to prove the restore works
camera.SetPosition(0, 0, 10)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 1, 0)

# RestoreScene: parse the camera parameters back from field data
stored = poly_data.GetFieldData().GetAbstractArray("Camera").GetValue(0)
for line in stored.strip().split("\n"):
    parts = line.strip().replace(",", "").split()
    key = parts[0]
    values = list(map(float, parts[1:]))
    if key == "Camera:Position":
        camera.SetPosition(values)
    elif key == "Camera:FocalPoint":
        camera.SetFocalPoint(values)
    elif key == "Camera:ViewUp":
        camera.SetViewUp(values)
    elif key == "Camera:ViewAngle":
        camera.SetViewAngle(values[0])
    elif key == "Camera:ClippingRange":
        camera.SetClippingRange(values)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SaveSceneToFieldData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
