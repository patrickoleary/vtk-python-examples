#!/usr/bin/env python

# Compute a distance field from a polydata source using
# vtkImplicitModeller and extract an isosurface showing the
# distance envelope around the original geometry.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
light_gray_rgb = (0.800, 0.800, 0.800)
tomato_rgb = (1.000, 0.388, 0.278)

# Source: generate a tessellated sphere as the input geometry
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.SetRadius(0.5)

# ImplicitModeller: compute a distance field from the sphere surface
modeller = vtkImplicitModeller()
modeller.SetInputConnection(sphere.GetOutputPort())
modeller.SetSampleDimensions(50, 50, 50)
modeller.SetModelBounds(-1.5, 1.5, -1.5, 1.5, -1.5, 1.5)
modeller.SetMaximumDistance(0.5)
modeller.SetProcessModeToPerVoxel()

# Contour: extract an isosurface at distance 0.25 from the sphere
contour = vtkContourFilter()
contour.SetInputConnection(modeller.GetOutputPort())
contour.SetValue(0, 0.25)

# Mapper for the distance envelope
envelope_mapper = vtkPolyDataMapper()
envelope_mapper.SetInputConnection(contour.GetOutputPort())
envelope_mapper.ScalarVisibilityOff()

# Actor for the distance envelope (translucent tomato)
envelope_actor = vtkActor()
envelope_actor.SetMapper(envelope_mapper)
envelope_actor.GetProperty().SetColor(tomato_rgb)
envelope_actor.GetProperty().SetOpacity(0.4)

# Mapper for the original sphere
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

# Actor for the original sphere (opaque grey)
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(light_gray_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(envelope_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitModeller")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
