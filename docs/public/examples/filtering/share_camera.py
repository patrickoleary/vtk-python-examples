#!/usr/bin/env python

# Share a single camera across four viewports showing different geometry.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)

# Background colors from a Brewer color series
color_series = vtkColorSeries()
color_series.SetColorSchemeByName("Brewer Qualitative Pastel2")

# --- Viewport 0: sphere (bottom-left) ---
sphere = vtkSphereSource()
sphere.Update()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(tomato_rgb)

bg_color_0 = color_series.GetColor(0)
bg_0 = (bg_color_0.GetRed() / 255.0, bg_color_0.GetGreen() / 255.0, bg_color_0.GetBlue() / 255.0)

renderer_0 = vtkRenderer()
renderer_0.AddActor(sphere_actor)
renderer_0.SetBackground(bg_0)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# --- Viewport 1: cone (bottom-right) ---
cone = vtkConeSource()
cone.Update()

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(tomato_rgb)

bg_color_1 = color_series.GetColor(1)
bg_1 = (bg_color_1.GetRed() / 255.0, bg_color_1.GetGreen() / 255.0, bg_color_1.GetBlue() / 255.0)

renderer_1 = vtkRenderer()
renderer_1.AddActor(cone_actor)
renderer_1.SetBackground(bg_1)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# --- Viewport 2: cube (top-left) ---
cube = vtkCubeSource()
cube.Update()

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(tomato_rgb)

bg_color_2 = color_series.GetColor(2)
bg_2 = (bg_color_2.GetRed() / 255.0, bg_color_2.GetGreen() / 255.0, bg_color_2.GetBlue() / 255.0)

renderer_2 = vtkRenderer()
renderer_2.AddActor(cube_actor)
renderer_2.SetBackground(bg_2)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# --- Viewport 3: cylinder (top-right) ---
cylinder = vtkCylinderSource()
cylinder.Update()

cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(tomato_rgb)

bg_color_3 = color_series.GetColor(3)
bg_3 = (bg_color_3.GetRed() / 255.0, bg_color_3.GetGreen() / 255.0, bg_color_3.GetBlue() / 255.0)

renderer_3 = vtkRenderer()
renderer_3.AddActor(cylinder_actor)
renderer_3.SetBackground(bg_3)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)

# Shared camera: all viewports share renderer_0's camera
shared_camera = renderer_0.GetActiveCamera()
renderer_1.SetActiveCamera(shared_camera)
renderer_2.SetActiveCamera(shared_camera)
renderer_3.SetActiveCamera(shared_camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("share camera")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: configure shared camera
shared_camera.Azimuth(30)
shared_camera.Elevation(30)
renderer_0.ResetCamera()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
