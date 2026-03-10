#!/usr/bin/env python

# Shadow-mapped spotlights illuminating a box, cone, sphere on a ground plane.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkLightActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkOpaquePass,
    vtkOpenGLRenderer,
    vtkRenderPassCollection,
    vtkSequencePass,
    vtkShadowMapPass,
)

# Colors (normalized RGB)
beige_rgb = (0.961, 0.961, 0.863)
tomato_rgb = (1.0, 0.388, 0.278)
peacock_rgb = (0.200, 0.631, 0.788)
banana_rgb = (0.890, 0.812, 0.341)
white_rgb = (1.0, 1.0, 1.0)
magenta_rgb = (1.0, 0.0, 1.0)
black_rgb = (0.0, 0.0, 0.0)
silver_rgb = (0.753, 0.753, 0.753)

# Renderer: use vtkOpenGLRenderer for shadow map support
renderer = vtkOpenGLRenderer()

# Shadow map render pass pipeline
seq = vtkSequencePass()
passes = vtkRenderPassCollection()
shadows = vtkShadowMapPass()
passes.AddItem(shadows.GetShadowMapBakerPass())
passes.AddItem(shadows)
opaque = vtkOpaquePass()
passes.AddItem(opaque)
seq.SetPasses(passes)
camera_pass = vtkCameraPass()
camera_pass.SetDelegatePass(seq)
renderer.SetPass(camera_pass)

# Source/Mapper/Actor: ground plane (beige)
rectangle_source = vtkPlaneSource()
rectangle_source.SetOrigin(-5.0, 0.0, 5.0)
rectangle_source.SetPoint1(5.0, 0.0, 5.0)
rectangle_source.SetPoint2(-5.0, 0.0, -5.0)
rectangle_source.SetResolution(100, 100)

rectangle_mapper = vtkPolyDataMapper()
rectangle_mapper.SetInputConnection(rectangle_source.GetOutputPort())
rectangle_mapper.SetScalarVisibility(0)

rectangle_actor = vtkActor()
rectangle_actor.SetMapper(rectangle_mapper)
rectangle_actor.GetProperty().SetColor(beige_rgb)

# Source/Mapper/Actor: box (tomato)
box_source = vtkCubeSource()
box_source.SetXLength(2.0)

box_normals = vtkPolyDataNormals()
box_normals.SetInputConnection(box_source.GetOutputPort())
box_normals.ComputePointNormalsOff()
box_normals.ComputeCellNormalsOn()
box_normals.Update()
box_normals.GetOutput().GetPointData().SetNormals(None)

box_mapper = vtkPolyDataMapper()
box_mapper.SetInputConnection(box_normals.GetOutputPort())
box_mapper.ScalarVisibilityOff()

box_actor = vtkActor()
box_actor.SetMapper(box_mapper)
box_actor.SetPosition(-2.0, 2.0, 0.0)
box_actor.GetProperty().SetColor(tomato_rgb)

# Source/Mapper/Actor: cone (peacock blue)
cone_source = vtkConeSource()
cone_source.SetResolution(24)
cone_source.SetDirection(1.0, 1.0, 1.0)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())
cone_mapper.SetScalarVisibility(0)

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0.0, 1.0, 1.0)
cone_actor.GetProperty().SetColor(peacock_rgb)

# Source/Mapper/Actor: sphere (banana yellow)
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(32)
sphere_source.SetPhiResolution(32)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetPosition(2.0, 2.0, -1.0)
sphere_actor.GetProperty().SetColor(banana_rgb)

renderer.AddViewProp(rectangle_actor)
renderer.AddViewProp(box_actor)
renderer.AddViewProp(cone_actor)
renderer.AddViewProp(sphere_actor)

# Spotlight 1: white, aimed at the box
l1 = vtkLight()
l1.SetPosition(-4.0, 4.0, -1.0)
l1.SetFocalPoint(box_actor.GetPosition())
l1.SetColor(white_rgb)
l1.PositionalOn()
l1.SwitchOn()
renderer.AddLight(l1)

# Spotlight 2: magenta, aimed at the sphere
l2 = vtkLight()
l2.SetPosition(4.0, 5.0, 1.0)
l2.SetFocalPoint(sphere_actor.GetPosition())
l2.SetColor(magenta_rgb)
l2.PositionalOn()
l2.SwitchOn()
renderer.AddLight(l2)

# Light frustum wireframes for each spotlight
for light in (l1, l2):
    if light.LightTypeIsSceneLight() and light.GetPositional() and light.GetConeAngle() < 180.0:
        la = vtkLightActor()
        la.SetLight(light)
        renderer.AddViewProp(la)

renderer.SetBackground2(black_rgb)
renderer.SetBackground(silver_rgb)
renderer.SetGradientBackground(True)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("ShadowsLightsDemo")
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(40.0)
renderer.GetActiveCamera().Elevation(10.0)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
