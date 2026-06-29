#!/usr/bin/env python

# Test vtkAssembly with sphere, cube, cone, and cylinder primitives.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAssembly,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere
sphere = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.SetOrigin(2, 1, 3)
sphere_actor.RotateY(6)
sphere_actor.SetPosition(2.25, 0, 0)
sphere_actor.GetProperty().SetColor(1, 0, 1)

# Cube
cube = vtkCubeSource()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.SetPosition(0.0, 0.25, 0)
cube_actor.GetProperty().SetColor(0, 0, 1)

# Cone
cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 0.25)
cone_actor.GetProperty().SetColor(0, 1, 0)

# Cylinder
cylinder = vtkCylinderSource()
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())
cylinder_mapper.SetResolveCoincidentTopologyToPolygonOffset()
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(1, 0, 0)

# Assembly
assembly = vtkAssembly()
assembly.AddPart(cylinder_actor)
assembly.AddPart(sphere_actor)
assembly.AddPart(cube_actor)
assembly.AddPart(cone_actor)
assembly.SetOrigin(5, 10, 15)
assembly.AddPosition(5, 0, 0)
assembly.RotateX(15)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(assembly)
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("assembly")
render_window.SetMultiSamples(0)
render_window.SetSize(200, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetClippingRange(21.9464, 30.0179)
camera.SetFocalPoint(3.49221, 2.28844, -0.970866)
camera.SetPosition(3.49221, 2.28844, 24.5216)
camera.SetViewAngle(30)
camera.SetViewUp(0, 1, 0)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
