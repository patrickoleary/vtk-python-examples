#!/usr/bin/env python

# Demonstrate vtkCollisionDetectionFilter in AllContacts mode by creating
# two spheres, translating one toward the other, detecting collisions,
# and rendering the wireframe spheres with contact lines.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
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

named_colors = vtkNamedColors()

# Two spheres
sphere_0 = vtkSphereSource()
sphere_0.SetRadius(0.29)
sphere_0.SetPhiResolution(31)
sphere_0.SetThetaResolution(31)
sphere_0.SetCenter(0.0, 0.0, 0.0)

sphere_1 = vtkSphereSource()
sphere_1.SetPhiResolution(30)
sphere_1.SetThetaResolution(30)
sphere_1.SetRadius(0.3)

# Transform and matrix for collision detection
matrix_1 = vtkMatrix4x4()
transform_0 = vtkTransform()

# Collision detection filter — AllContacts mode
collide = vtkCollisionDetectionFilter()
collide.SetInputConnection(0, sphere_0.GetOutputPort())
collide.SetTransform(0, transform_0)
collide.SetInputConnection(1, sphere_1.GetOutputPort())
collide.SetMatrix(1, matrix_1)
collide.SetBoxTolerance(0.0)
collide.SetCellTolerance(0.0)
collide.SetNumberOfCellsPerNode(2)
collide.SetCollisionModeToAllContacts()
collide.GenerateScalarsOn()

# Sphere 0 actor (wireframe)
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(collide.GetOutputPort(0))
mapper_0.ScalarVisibilityOff()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().BackfaceCullingOn()
actor_0.SetUserTransform(transform_0)
actor_0.GetProperty().SetDiffuseColor(named_colors.GetColor3d("Tomato"))
actor_0.GetProperty().SetRepresentationToWireframe()

# Sphere 1 actor
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(collide.GetOutputPort(1))

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().BackfaceCullingOn()
actor_1.SetUserMatrix(matrix_1)

# Contact lines actor
mapper_contacts = vtkPolyDataMapper()
mapper_contacts.SetInputConnection(collide.GetContactsOutputPort())
mapper_contacts.SetResolveCoincidentTopologyToPolygonOffset()

actor_contacts = vtkActor()
actor_contacts.SetMapper(mapper_contacts)
actor_contacts.GetProperty().SetColor(0, 0, 0)
actor_contacts.GetProperty().SetLineWidth(3.0)

# Text actor for collision info
text_actor = vtkTextActor()

# Renderer
renderer = vtkRenderer()
renderer.UseHiddenLineRemovalOn()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_contacts)
renderer.AddActor(text_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.AddRenderer(renderer)
render_window.SetWindowName("collision detection all contacts")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Translate sphere 0 toward sphere 1
delta_x = 0.1
num_steps = 20
transform_0.Translate(-num_steps * delta_x - 0.3, 0.0, 0.0)
render_window.Render()
renderer.GetActiveCamera().Azimuth(-45)
renderer.GetActiveCamera().Elevation(45)
renderer.GetActiveCamera().Dolly(1.2)

for i in range(num_steps):
    transform_0.Translate(delta_x, 0.0, 0.0)
    renderer.ResetCameraClippingRange()
    text_actor.SetInput(
        f"{collide.GetCollisionModeAsString()}: "
        f"Number of contact cells is {collide.GetNumberOfContacts()}"
    )
    render_window.Render()
    if collide.GetNumberOfContacts() > 0:
        break

renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
