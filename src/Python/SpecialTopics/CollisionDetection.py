#!/usr/bin/env python

# Detect collisions between a moving wireframe sphere and a fixed solid sphere.

import time

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersModeling import vtkCollisionDetectionFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
black_rgb = (0.0, 0.0, 0.0)
gray_rgb = (0.502, 0.502, 0.502)

# Source: fixed sphere (solid)
sphere0 = vtkSphereSource()
sphere0.SetRadius(0.29)
sphere0.SetPhiResolution(31)
sphere0.SetThetaResolution(31)
sphere0.SetCenter(0.0, 0.0, 0.0)

# Source: moving sphere (wireframe)
sphere1 = vtkSphereSource()
sphere1.SetPhiResolution(30)
sphere1.SetThetaResolution(30)
sphere1.SetRadius(0.3)

# Transforms for the two spheres
matrix1 = vtkMatrix4x4()
transform0 = vtkTransform()

# CollisionDetection: find contacts between the two spheres
collide = vtkCollisionDetectionFilter()
collide.SetInputConnection(0, sphere0.GetOutputPort())
collide.SetTransform(0, transform0)
collide.SetInputConnection(1, sphere1.GetOutputPort())
collide.SetMatrix(1, matrix1)
collide.SetBoxTolerance(0.0)
collide.SetCellTolerance(0.0)
collide.SetNumberOfCellsPerNode(2)
collide.SetCollisionModeToAllContacts()
collide.GenerateScalarsOn()

# Mapper/Actor: moving sphere (wireframe, tomato)
mapper1 = vtkPolyDataMapper()
mapper1.SetInputConnection(collide.GetOutputPort(0))
mapper1.ScalarVisibilityOff()

actor1 = vtkActor()
actor1.SetMapper(mapper1)
actor1.GetProperty().BackfaceCullingOn()
actor1.SetUserTransform(transform0)
actor1.GetProperty().SetDiffuseColor(tomato_rgb)
actor1.GetProperty().SetRepresentationToWireframe()

# Mapper/Actor: fixed sphere (solid white)
mapper2 = vtkPolyDataMapper()
mapper2.SetInputConnection(collide.GetOutputPort(1))

actor2 = vtkActor()
actor2.SetMapper(mapper2)
actor2.GetProperty().BackfaceCullingOn()
actor2.SetUserMatrix(matrix1)

# Mapper/Actor: contact points (black lines)
mapper3 = vtkPolyDataMapper()
mapper3.SetInputConnection(collide.GetContactsOutputPort())
mapper3.SetResolveCoincidentTopologyToPolygonOffset()

actor3 = vtkActor()
actor3.SetMapper(mapper3)
actor3.GetProperty().SetColor(black_rgb)
actor3.GetProperty().SetLineWidth(3.0)

# Text: display collision mode and contact count
txt = vtkTextActor()
txt.GetTextProperty().SetFontSize(18)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.UseHiddenLineRemovalOn()
renderer.AddActor(actor1)
renderer.AddActor(actor2)
renderer.AddActor(actor3)
renderer.AddActor(txt)
renderer.SetBackground(gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("CollisionDetection")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Animation: translate the moving sphere toward the fixed sphere
num_steps = 100
dx = 1.0 / float(num_steps) * 2.0
transform0.Translate(-num_steps * dx - 0.3, 0.0, 0.0)
render_window.Render()
renderer.GetActiveCamera().Azimuth(-60)
renderer.GetActiveCamera().Elevation(45)
renderer.GetActiveCamera().Dolly(1.2)
render_window.Render()

for i in range(num_steps):
    transform0.Translate(dx, 0.0, 0.0)
    renderer.ResetCameraClippingRange()
    s = "{}: Number of contact cells is {}".format(
        collide.GetCollisionModeAsString(), collide.GetNumberOfContacts()
    )
    txt.SetInput(s)
    render_window.Render()
    if collide.GetNumberOfContacts() > 0:
        break
    time.sleep(3.0 / num_steps)

renderer.ResetCamera()
render_window.Render()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
