#!/usr/bin/env python

# Render a cube on layer 0 and a semi-transparent cone on layer 1 so
# the layer-1 background is transparent and layer-0 shows through.
# Press '0' or '1' to switch which layer receives interaction.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_green = (0.0, 0.392, 0.0)
dark_turquoise = (0.0, 0.808, 0.820)
silver = (0.753, 0.753, 0.753)
midnight_blue = (0.098, 0.098, 0.439)

# Source: generate a cube slab
cube = vtkCubeSource()
cube.SetXLength(4.0)
cube.SetYLength(9.0)
cube.SetZLength(1.0)

# Mapper: map cube polygon data
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

# Actor: the cube on layer 0
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetDiffuseColor(dark_green)

# Source: generate a cone
cone = vtkConeSource()
cone.SetHeight(1.0)
cone.SetRadius(0.25)
cone.SetDirection(0.0, 1.0, 0.0)
cone.SetResolution(60)
cone.CappingOn()

# Mapper: map cone polygon data
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: the semi-transparent cone on layer 1
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetDiffuseColor(dark_turquoise)
cone_actor.GetProperty().SetOpacity(0.75)

# Renderer: layer 0 — opaque background with cube
renderer_0 = vtkRenderer()
renderer_0.AddActor(cube_actor)
renderer_0.SetBackground(silver)
renderer_0.SetLayer(0)

# Renderer: layer 1 — transparent background with cone
renderer_1 = vtkRenderer()
renderer_1.AddActor(cone_actor)
renderer_1.SetBackground(midnight_blue)
renderer_1.SetLayer(1)

# Window: display both layers
render_window = vtkRenderWindow()
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(640, 480)
render_window.SetWindowName("TransparentBackground")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

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

interactor.AddObserver("KeyPressEvent", on_keypress)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
