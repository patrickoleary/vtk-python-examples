#!/usr/bin/env python

# Use a spline widget to draw an interactive spline over a cylinder.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkCameraOrientationWidget,
    vtkSplineWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornsilk_rgb = (1.0, 0.973, 0.863)
paraview_bkg_rgb = (0.322, 0.341, 0.431)

# Source: generate a cylinder
cylinder = vtkCylinderSource()
cylinder.SetCenter(0.0, 0.0, 0.0)
cylinder.SetRadius(3.0)
cylinder.SetHeight(5.0)
cylinder.SetResolution(100)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cylinder.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.GetProperty().SetColor(cornsilk_rgb)
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(paraview_bkg_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1024, 1024)
render_window.SetWindowName("SplineWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# SplineWidget: interactive spline placed over the actor
spline_widget = vtkSplineWidget()
spline_widget.SetInteractor(render_window_interactor)
spline_widget.SetProp3D(actor)
spline_widget.PlaceWidget(-2.5, 2.5, 3.5, 3.5, 0, 0)
spline_widget.On()

spline_widget.AddObserver(vtkCommand.EndInteractionEvent,
                          lambda obj, event: print(
                              f"Length: {obj.GetSummedLength():.4f}"))

# CameraOrientationWidget: orientation gizmo in the viewport corner
cow = vtkCameraOrientationWidget()
cow.SetParentRenderer(renderer)
cow.On()

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
