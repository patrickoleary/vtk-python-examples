#!/usr/bin/env python

# Test vtkPropAssembly combining vtkAssembly with primitives.

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
    vtkPolyDataMapper,
    vtkPropAssembly,
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
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(1, 0, 0)

# Composite assembly
composite_assembly = vtkAssembly()
composite_assembly.AddPart(cylinder_actor)
composite_assembly.AddPart(sphere_actor)
composite_assembly.AddPart(cube_actor)
composite_assembly.AddPart(cone_actor)
composite_assembly.SetOrigin(5, 10, 15)
composite_assembly.AddPosition(5, 0, 0)
composite_assembly.RotateX(15)

# Build prop assembly from vtkActor and vtkAssembly
assembly = vtkPropAssembly()
assembly.AddPart(composite_assembly)
assembly.AddPart(cone_actor)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(assembly)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("prop assembly")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
