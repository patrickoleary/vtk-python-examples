#!/usr/bin/env python

# Towers of Hanoi: display the initial configuration with all disks on peg 0.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkPlaneSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
papaya_whip_rgb = (1.0, 0.937, 0.835)
saddle_brown_rgb = (0.545, 0.271, 0.075)
lavender_rgb = (0.902, 0.902, 0.980)

# Puzzle parameters
num_pucks = 5
puck_resolution = 48
L = 1.0
R = 0.5
r_min = 4.0 * R
r_max = 12.0 * R
D = 1.1 * 1.25 * r_max
H = 1.1 * num_pucks * L

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(papaya_whip_rgb)

camera = vtkCamera()
camera.SetPosition(41.0433, 27.9637, 30.442)
camera.SetFocalPoint(11.5603, -1.51931, 0.95899)
camera.SetClippingRange(18.9599, 91.6042)
camera.SetViewUp(0, 1, 0)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1200, 750)
render_window.SetWindowName("HanoiInitial")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Source/Mapper: peg geometry (thin cylinder)
peg_geometry = vtkCylinderSource()
peg_geometry.SetResolution(8)
peg_mapper = vtkPolyDataMapper()
peg_mapper.SetInputConnection(peg_geometry.GetOutputPort())

# Source/Mapper: puck geometry (wider cylinder)
puck_geometry = vtkCylinderSource()
puck_geometry.SetResolution(puck_resolution)
puck_mapper = vtkPolyDataMapper()
puck_mapper.SetInputConnection(puck_geometry.GetOutputPort())

# Source/Mapper: table geometry (plane)
table_geometry = vtkPlaneSource()
table_geometry.SetResolution(10, 10)
table_mapper = vtkPolyDataMapper()
table_mapper.SetInputConnection(table_geometry.GetOutputPort())

# Actor: table surface
table = vtkActor()
table.SetMapper(table_mapper)
table.GetProperty().SetColor(saddle_brown_rgb)
table.AddPosition(D, 0, 0)
table.SetScale(4 * D, 2 * D, 3 * D)
table.RotateX(90)
renderer.AddActor(table)

# Actors: three pegs
for i in range(3):
    peg = vtkActor()
    peg.SetMapper(peg_mapper)
    peg.GetProperty().SetColor(lavender_rgb)
    peg.AddPosition(i * D, H / 2, 0)
    peg.SetScale(1, H, 1)
    renderer.AddActor(peg)

# Actors: pucks stacked on peg 0 with random colors
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(1)
for i in range(num_pucks):
    puck = vtkActor()
    puck.SetMapper(puck_mapper)
    color = [0.0, 0.0, 0.0]
    for j in range(3):
        color[j] = rng.GetValue()
        rng.Next()
    puck.GetProperty().SetColor(*color)
    puck.AddPosition(0, i * L + L / 2, 0)
    scale = r_max - i * (r_max - r_min) / (num_pucks - 1)
    puck.SetScale(scale, 1, scale)
    renderer.AddActor(puck)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
