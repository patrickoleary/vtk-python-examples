#!/usr/bin/env python

# Demonstrate a legend box with colored symbols using vtkLegendBoxActor,
# showing labels for three geometric objects in the scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingAnnotation import vtkLegendBoxActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
gold_rgb = (1.0, 0.843, 0.0)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetCenter(-2.0, 0.0, 0.0)
sphere_source.SetThetaResolution(20)
sphere_source.SetPhiResolution(20)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(tomato_rgb)

# Source: generate a cube
cube_source = vtkCubeSource()
cube_source.SetCenter(0.0, 0.0, 0.0)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(steel_blue_rgb)

# Source: generate a cone
cone_source = vtkConeSource()
cone_source.SetCenter(2.0, 0.0, 0.0)
cone_source.SetResolution(20)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(gold_rgb)

# Legend box: display labeled color swatches for each object
legend = vtkLegendBoxActor()
legend.SetNumberOfEntries(3)
legend.SetEntry(0, sphere_source.GetOutput(), "Sphere", tomato_rgb)
legend.SetEntry(1, cube_source.GetOutput(), "Cube", steel_blue_rgb)
legend.SetEntry(2, cone_source.GetOutput(), "Cone", gold_rgb)
legend.UseBackgroundOn()
legend.SetBackgroundColor(0.1, 0.1, 0.1)
legend.SetBackgroundOpacity(0.5)
legend.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
legend.GetPositionCoordinate().SetValue(0.025, 0.025)
legend.GetPosition2Coordinate().SetCoordinateSystemToNormalizedViewport()
legend.GetPosition2Coordinate().SetValue(0.2, 0.2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cube_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(legend)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("LegendBoxActor")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
