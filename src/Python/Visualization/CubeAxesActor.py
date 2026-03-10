#!/usr/bin/env python

# Display labeled cube axes with gridlines around a superquadric surface.

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
dark_slate_gray = (0.184, 0.310, 0.310)
tomato = (1.000, 0.388, 0.278)
salmon = (0.980, 0.502, 0.447)
pale_green = (0.596, 0.984, 0.596)
light_sky_blue = (0.529, 0.808, 0.980)

# Source: generate superquadric polygon data
source = vtkSuperquadricSource()
source.SetPhiRoundness(3.1)
source.SetThetaRoundness(1.0)
source.Update()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry with diffuse and specular shading
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(tomato)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetSpecular(0.7)
actor.GetProperty().SetSpecularPower(50.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(dark_slate_gray)

# CubeAxes: draw labeled bounding-box axes with gridlines
cube_axes = vtkCubeAxesActor()
cube_axes.SetUseTextActor3D(1)
cube_axes.SetBounds(source.GetOutput().GetBounds())
cube_axes.SetCamera(renderer.GetActiveCamera())

cube_axes.GetTitleTextProperty(0).SetColor(salmon)
cube_axes.GetTitleTextProperty(0).SetFontSize(18)
cube_axes.GetLabelTextProperty(0).SetColor(salmon)
cube_axes.DrawXGridlinesOn()
cube_axes.XAxisMinorTickVisibilityOff()

cube_axes.GetTitleTextProperty(1).SetColor(pale_green)
cube_axes.GetTitleTextProperty(1).SetFontSize(18)
cube_axes.GetLabelTextProperty(1).SetColor(pale_green)
cube_axes.DrawYGridlinesOn()
cube_axes.YAxisMinorTickVisibilityOff()

cube_axes.GetTitleTextProperty(2).SetColor(light_sky_blue)
cube_axes.GetTitleTextProperty(2).SetFontSize(18)
cube_axes.GetLabelTextProperty(2).SetColor(light_sky_blue)
cube_axes.DrawZGridlinesOn()
cube_axes.ZAxisMinorTickVisibilityOff()

cube_axes.SetGridLineLocation(cube_axes.VTK_GRID_LINES_FURTHEST)
cube_axes.SetFlyModeToStaticEdges()

renderer.AddActor(cube_axes)
renderer.AddActor(actor)
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(0.8)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CubeAxesActor")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
