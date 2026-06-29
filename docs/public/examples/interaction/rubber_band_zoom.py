#!/usr/bin/env python

# Demonstrate vtkInteractorStyleRubberBandZoom, which allows the user to
# draw a rectangle to zoom into a region of the scene.  A grid of spheres
# provides visual context for the zoom operation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandZoom
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Sources: 5x5 grid of spheres
sphere_0 = vtkSphereSource()
sphere_0.SetCenter(0.0, 0.0, 0)
sphere_0.SetRadius(0.8)
sphere_0.SetPhiResolution(16)
sphere_0.SetThetaResolution(16)

sphere_1 = vtkSphereSource()
sphere_1.SetCenter(2.5, 0.0, 0)
sphere_1.SetRadius(0.8)
sphere_1.SetPhiResolution(16)
sphere_1.SetThetaResolution(16)

sphere_2 = vtkSphereSource()
sphere_2.SetCenter(5.0, 0.0, 0)
sphere_2.SetRadius(0.8)
sphere_2.SetPhiResolution(16)
sphere_2.SetThetaResolution(16)

sphere_3 = vtkSphereSource()
sphere_3.SetCenter(7.5, 0.0, 0)
sphere_3.SetRadius(0.8)
sphere_3.SetPhiResolution(16)
sphere_3.SetThetaResolution(16)

sphere_4 = vtkSphereSource()
sphere_4.SetCenter(10.0, 0.0, 0)
sphere_4.SetRadius(0.8)
sphere_4.SetPhiResolution(16)
sphere_4.SetThetaResolution(16)

sphere_5 = vtkSphereSource()
sphere_5.SetCenter(0.0, 2.5, 0)
sphere_5.SetRadius(0.8)
sphere_5.SetPhiResolution(16)
sphere_5.SetThetaResolution(16)

sphere_6 = vtkSphereSource()
sphere_6.SetCenter(2.5, 2.5, 0)
sphere_6.SetRadius(0.8)
sphere_6.SetPhiResolution(16)
sphere_6.SetThetaResolution(16)

sphere_7 = vtkSphereSource()
sphere_7.SetCenter(5.0, 2.5, 0)
sphere_7.SetRadius(0.8)
sphere_7.SetPhiResolution(16)
sphere_7.SetThetaResolution(16)

sphere_8 = vtkSphereSource()
sphere_8.SetCenter(7.5, 2.5, 0)
sphere_8.SetRadius(0.8)
sphere_8.SetPhiResolution(16)
sphere_8.SetThetaResolution(16)

sphere_9 = vtkSphereSource()
sphere_9.SetCenter(10.0, 2.5, 0)
sphere_9.SetRadius(0.8)
sphere_9.SetPhiResolution(16)
sphere_9.SetThetaResolution(16)

sphere_10 = vtkSphereSource()
sphere_10.SetCenter(0.0, 5.0, 0)
sphere_10.SetRadius(0.8)
sphere_10.SetPhiResolution(16)
sphere_10.SetThetaResolution(16)

sphere_11 = vtkSphereSource()
sphere_11.SetCenter(2.5, 5.0, 0)
sphere_11.SetRadius(0.8)
sphere_11.SetPhiResolution(16)
sphere_11.SetThetaResolution(16)

sphere_12 = vtkSphereSource()
sphere_12.SetCenter(5.0, 5.0, 0)
sphere_12.SetRadius(0.8)
sphere_12.SetPhiResolution(16)
sphere_12.SetThetaResolution(16)

sphere_13 = vtkSphereSource()
sphere_13.SetCenter(7.5, 5.0, 0)
sphere_13.SetRadius(0.8)
sphere_13.SetPhiResolution(16)
sphere_13.SetThetaResolution(16)

sphere_14 = vtkSphereSource()
sphere_14.SetCenter(10.0, 5.0, 0)
sphere_14.SetRadius(0.8)
sphere_14.SetPhiResolution(16)
sphere_14.SetThetaResolution(16)

sphere_15 = vtkSphereSource()
sphere_15.SetCenter(0.0, 7.5, 0)
sphere_15.SetRadius(0.8)
sphere_15.SetPhiResolution(16)
sphere_15.SetThetaResolution(16)

sphere_16 = vtkSphereSource()
sphere_16.SetCenter(2.5, 7.5, 0)
sphere_16.SetRadius(0.8)
sphere_16.SetPhiResolution(16)
sphere_16.SetThetaResolution(16)

sphere_17 = vtkSphereSource()
sphere_17.SetCenter(5.0, 7.5, 0)
sphere_17.SetRadius(0.8)
sphere_17.SetPhiResolution(16)
sphere_17.SetThetaResolution(16)

sphere_18 = vtkSphereSource()
sphere_18.SetCenter(7.5, 7.5, 0)
sphere_18.SetRadius(0.8)
sphere_18.SetPhiResolution(16)
sphere_18.SetThetaResolution(16)

sphere_19 = vtkSphereSource()
sphere_19.SetCenter(10.0, 7.5, 0)
sphere_19.SetRadius(0.8)
sphere_19.SetPhiResolution(16)
sphere_19.SetThetaResolution(16)

sphere_20 = vtkSphereSource()
sphere_20.SetCenter(0.0, 10.0, 0)
sphere_20.SetRadius(0.8)
sphere_20.SetPhiResolution(16)
sphere_20.SetThetaResolution(16)

sphere_21 = vtkSphereSource()
sphere_21.SetCenter(2.5, 10.0, 0)
sphere_21.SetRadius(0.8)
sphere_21.SetPhiResolution(16)
sphere_21.SetThetaResolution(16)

sphere_22 = vtkSphereSource()
sphere_22.SetCenter(5.0, 10.0, 0)
sphere_22.SetRadius(0.8)
sphere_22.SetPhiResolution(16)
sphere_22.SetThetaResolution(16)

sphere_23 = vtkSphereSource()
sphere_23.SetCenter(7.5, 10.0, 0)
sphere_23.SetRadius(0.8)
sphere_23.SetPhiResolution(16)
sphere_23.SetThetaResolution(16)

sphere_24 = vtkSphereSource()
sphere_24.SetCenter(10.0, 10.0, 0)
sphere_24.SetRadius(0.8)
sphere_24.SetPhiResolution(16)
sphere_24.SetThetaResolution(16)

# Mapper + Actor 0
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sphere_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetColor(0.500, 0.700, 0.000)

# Mapper + Actor 1
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(sphere_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(0.540, 0.672, 0.028)

# Mapper + Actor 2
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(sphere_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(0.580, 0.644, 0.056)

# Mapper + Actor 3
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(sphere_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColor(0.620, 0.616, 0.084)

# Mapper + Actor 4
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(sphere_4.GetOutputPort())

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.GetProperty().SetColor(0.660, 0.588, 0.112)

# Mapper + Actor 5
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(sphere_5.GetOutputPort())

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.GetProperty().SetColor(0.700, 0.560, 0.140)

# Mapper + Actor 6
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(sphere_6.GetOutputPort())

actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.GetProperty().SetColor(0.740, 0.532, 0.168)

# Mapper + Actor 7
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(sphere_7.GetOutputPort())

actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.GetProperty().SetColor(0.780, 0.504, 0.196)

# Mapper + Actor 8
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputConnection(sphere_8.GetOutputPort())

actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)
actor_8.GetProperty().SetColor(0.820, 0.476, 0.224)

# Mapper + Actor 9
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputConnection(sphere_9.GetOutputPort())

actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)
actor_9.GetProperty().SetColor(0.860, 0.448, 0.252)

# Mapper + Actor 10
mapper_10 = vtkPolyDataMapper()
mapper_10.SetInputConnection(sphere_10.GetOutputPort())

actor_10 = vtkActor()
actor_10.SetMapper(mapper_10)
actor_10.GetProperty().SetColor(0.900, 0.420, 0.280)

# Mapper + Actor 11
mapper_11 = vtkPolyDataMapper()
mapper_11.SetInputConnection(sphere_11.GetOutputPort())

actor_11 = vtkActor()
actor_11.SetMapper(mapper_11)
actor_11.GetProperty().SetColor(0.940, 0.392, 0.308)

# Mapper + Actor 12
mapper_12 = vtkPolyDataMapper()
mapper_12.SetInputConnection(sphere_12.GetOutputPort())

actor_12 = vtkActor()
actor_12.SetMapper(mapper_12)
actor_12.GetProperty().SetColor(0.980, 0.364, 0.336)

# Mapper + Actor 13
mapper_13 = vtkPolyDataMapper()
mapper_13.SetInputConnection(sphere_13.GetOutputPort())

actor_13 = vtkActor()
actor_13.SetMapper(mapper_13)
actor_13.GetProperty().SetColor(0.980, 0.336, 0.364)

# Mapper + Actor 14
mapper_14 = vtkPolyDataMapper()
mapper_14.SetInputConnection(sphere_14.GetOutputPort())

actor_14 = vtkActor()
actor_14.SetMapper(mapper_14)
actor_14.GetProperty().SetColor(0.940, 0.308, 0.392)

# Mapper + Actor 15
mapper_15 = vtkPolyDataMapper()
mapper_15.SetInputConnection(sphere_15.GetOutputPort())

actor_15 = vtkActor()
actor_15.SetMapper(mapper_15)
actor_15.GetProperty().SetColor(0.900, 0.280, 0.420)

# Mapper + Actor 16
mapper_16 = vtkPolyDataMapper()
mapper_16.SetInputConnection(sphere_16.GetOutputPort())

actor_16 = vtkActor()
actor_16.SetMapper(mapper_16)
actor_16.GetProperty().SetColor(0.860, 0.252, 0.448)

# Mapper + Actor 17
mapper_17 = vtkPolyDataMapper()
mapper_17.SetInputConnection(sphere_17.GetOutputPort())

actor_17 = vtkActor()
actor_17.SetMapper(mapper_17)
actor_17.GetProperty().SetColor(0.820, 0.224, 0.476)

# Mapper + Actor 18
mapper_18 = vtkPolyDataMapper()
mapper_18.SetInputConnection(sphere_18.GetOutputPort())

actor_18 = vtkActor()
actor_18.SetMapper(mapper_18)
actor_18.GetProperty().SetColor(0.780, 0.196, 0.504)

# Mapper + Actor 19
mapper_19 = vtkPolyDataMapper()
mapper_19.SetInputConnection(sphere_19.GetOutputPort())

actor_19 = vtkActor()
actor_19.SetMapper(mapper_19)
actor_19.GetProperty().SetColor(0.740, 0.168, 0.532)

# Mapper + Actor 20
mapper_20 = vtkPolyDataMapper()
mapper_20.SetInputConnection(sphere_20.GetOutputPort())

actor_20 = vtkActor()
actor_20.SetMapper(mapper_20)
actor_20.GetProperty().SetColor(0.700, 0.140, 0.560)

# Mapper + Actor 21
mapper_21 = vtkPolyDataMapper()
mapper_21.SetInputConnection(sphere_21.GetOutputPort())

actor_21 = vtkActor()
actor_21.SetMapper(mapper_21)
actor_21.GetProperty().SetColor(0.660, 0.112, 0.588)

# Mapper + Actor 22
mapper_22 = vtkPolyDataMapper()
mapper_22.SetInputConnection(sphere_22.GetOutputPort())

actor_22 = vtkActor()
actor_22.SetMapper(mapper_22)
actor_22.GetProperty().SetColor(0.620, 0.084, 0.616)

# Mapper + Actor 23
mapper_23 = vtkPolyDataMapper()
mapper_23.SetInputConnection(sphere_23.GetOutputPort())

actor_23 = vtkActor()
actor_23.SetMapper(mapper_23)
actor_23.GetProperty().SetColor(0.580, 0.056, 0.644)

# Mapper + Actor 24
mapper_24 = vtkPolyDataMapper()
mapper_24.SetInputConnection(sphere_24.GetOutputPort())

actor_24 = vtkActor()
actor_24.SetMapper(mapper_24)
actor_24.GetProperty().SetColor(0.540, 0.028, 0.672)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddActor(actor_8)
renderer.AddActor(actor_9)
renderer.AddActor(actor_10)
renderer.AddActor(actor_11)
renderer.AddActor(actor_12)
renderer.AddActor(actor_13)
renderer.AddActor(actor_14)
renderer.AddActor(actor_15)
renderer.AddActor(actor_16)
renderer.AddActor(actor_17)
renderer.AddActor(actor_18)
renderer.AddActor(actor_19)
renderer.AddActor(actor_20)
renderer.AddActor(actor_21)
renderer.AddActor(actor_22)
renderer.AddActor(actor_23)
renderer.AddActor(actor_24)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("rubber band zoom")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Style: rubber-band zoom (draw a rectangle to zoom)
style = vtkInteractorStyleRubberBandZoom()
interactor.SetInteractorStyle(style)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
