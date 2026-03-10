#!/usr/bin/env python

# Cut a sphere source with an implicit plane using vtkCutter to show
# the cross-section contour line alongside the full sphere wireframe.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
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

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(40)
sphere.SetPhiResolution(40)

# Implicit function: a plane through the origin with normal along Z
cut_plane = vtkPlane()
cut_plane.SetOrigin(0.0, 0.0, 0.0)
cut_plane.SetNormal(0.0, 0.0, 1.0)

# Cutter: extract the cross-section contour where the plane intersects the sphere
cutter = vtkCutter()
cutter.SetInputConnection(sphere.GetOutputPort())
cutter.SetCutFunction(cut_plane)

# Mapper for the cut contour line
cut_mapper = vtkPolyDataMapper()
cut_mapper.SetInputConnection(cutter.GetOutputPort())
cut_mapper.ScalarVisibilityOff()

# Actor for the cut contour line (thick red)
cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(tomato_rgb)
cut_actor.GetProperty().SetLineWidth(4)

# Mapper for the sphere wireframe context
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_mapper.ScalarVisibilityOff()

# Actor for the sphere (translucent wireframe)
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(light_gray_rgb)
sphere_actor.GetProperty().SetOpacity(0.25)
sphere_actor.GetProperty().EdgeVisibilityOn()
sphere_actor.GetProperty().SetEdgeColor(0.6, 0.6, 0.6)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cut_actor)
renderer.AddActor(sphere_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CutWithImplicitFunction")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
