#!/usr/bin/env python

# Demonstrate labeled axes around the bounding box of a 3D object
# using vtkCubeAxesActor.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSuperquadricSource
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a superquadric shape
source = vtkSuperquadricSource()
source.SetPhiRoundness(3.1)
source.SetThetaRoundness(1.0)
source.Update()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)

# Cube axes: labeled axes around the bounding box
cube_axes = vtkCubeAxesActor()
cube_axes.SetBounds(source.GetOutput().GetBounds())
cube_axes.SetCamera(renderer.GetActiveCamera())
cube_axes.GetTitleTextProperty(0).SetColor(tomato_rgb)
cube_axes.GetTitleTextProperty(1).SetColor(tomato_rgb)
cube_axes.GetTitleTextProperty(2).SetColor(tomato_rgb)
cube_axes.GetLabelTextProperty(0).SetColor(tomato_rgb)
cube_axes.GetLabelTextProperty(1).SetColor(tomato_rgb)
cube_axes.GetLabelTextProperty(2).SetColor(tomato_rgb)
cube_axes.SetXTitle("X Axis")
cube_axes.SetYTitle("Y Axis")
cube_axes.SetZTitle("Z Axis")
cube_axes.SetFlyModeToStaticTriad()
cube_axes.SetGridLineLocation(cube_axes.VTK_GRID_LINES_FURTHEST)
cube_axes.XAxisMinorTickVisibilityOff()
cube_axes.YAxisMinorTickVisibilityOff()
cube_axes.ZAxisMinorTickVisibilityOff()
renderer.AddActor(cube_axes)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CubeAxesActor")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
