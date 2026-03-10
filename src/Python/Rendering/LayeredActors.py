#!/usr/bin/env python

# Display a cube slab on layer 0 and axes on layer 1, demonstrating
# layered rendering.  Press '0' or '1' to switch the interactive layer;
# camera orientation is synchronised between layers after interaction.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burly_wood = (0.871, 0.722, 0.529)
sienna = (0.627, 0.322, 0.176)
papaya_whip = (1.0, 0.937, 0.835)
dark_slate_gray = (0.184, 0.310, 0.310)

# Source: generate a cube slab
cube = vtkCubeSource()
cube.SetXLength(4.0)
cube.SetYLength(9.0)
cube.SetZLength(1.0)

# Mapper: map cube polygon data
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

# Actor: cube with edge visibility and back-face colouring
back_prop = vtkProperty()
back_prop.SetColor(sienna)

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetDiffuseColor(burly_wood)
cube_actor.GetProperty().EdgeVisibilityOn()
cube_actor.GetProperty().SetLineWidth(2.0)
cube_actor.GetProperty().SetEdgeColor(papaya_whip)
cube_actor.SetBackfaceProperty(back_prop)

# Actor: axes widget positioned at the origin
transform = vtkTransform()
transform.Translate(0.0, 0.0, 0.0)
axes = vtkAxesActor()
axes.SetUserTransform(transform)

# Renderer: layer 0 — opaque background with cube
renderer_0 = vtkRenderer()
renderer_0.AddActor(cube_actor)
renderer_0.SetBackground(dark_slate_gray)
renderer_0.SetLayer(0)

# Renderer: layer 1 — transparent background with axes
renderer_1 = vtkRenderer()
renderer_1.AddActor(axes)
renderer_1.SetLayer(1)

# Camera: set a shared initial view for both layers
for ren in (renderer_0, renderer_1):
    ren.GetActiveCamera().Elevation(-30)
    ren.GetActiveCamera().Azimuth(-30)
    ren.ResetCamera()

# Window: display both layers
render_window = vtkRenderWindow()
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(640, 480)
render_window.SetWindowName("LayeredActors")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Callback: press '0' or '1' to switch the interactive layer
def on_keypress(caller, event):
    key = caller.GetKeySym()
    renderers = caller.GetRenderWindow().GetRenderers()
    renderers.InitTraversal()
    ren0 = renderers.GetNextItem()
    ren1 = renderers.GetNextItem()
    if key in ("0", "KP_0"):
        caller.GetInteractorStyle().SetDefaultRenderer(ren0)
        ren0.InteractiveOn()
        ren1.InteractiveOff()
    elif key in ("1", "KP_1"):
        caller.GetInteractorStyle().SetDefaultRenderer(ren1)
        ren0.InteractiveOff()
        ren1.InteractiveOn()

# Callback: synchronise camera orientation between layers after interaction
def on_end_interaction(caller, event):
    renderers = caller.GetRenderWindow().GetRenderers()
    renderers.InitTraversal()
    ren0 = renderers.GetNextItem()
    ren1 = renderers.GetNextItem()
    if ren1.GetInteractive():
        src, dst = ren1, ren0
    else:
        src, dst = ren0, ren1
    cam_src = src.GetActiveCamera()
    cam_dst = dst.GetActiveCamera()
    cam_dst.SetPosition(cam_src.GetPosition())
    cam_dst.SetFocalPoint(cam_src.GetFocalPoint())
    cam_dst.SetViewUp(cam_src.GetViewUp())
    cam_dst.SetDistance(cam_src.GetDistance())
    cam_dst.SetClippingRange(cam_src.GetClippingRange())
    dst.ResetCamera()

interactor.AddObserver("KeyPressEvent", on_keypress)
interactor.AddObserver("EndInteractionEvent", on_end_interaction)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
