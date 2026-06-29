#!/usr/bin/env python

# Compute and display mass properties (volume, surface area) for
# a sphere, cone, and cube side by side.

from io import StringIO
import sys

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkMassProperties,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Sources
cone = vtkConeSource()
cone.SetResolution(50)

sphere = vtkSphereSource()
sphere.SetPhiResolution(50)
sphere.SetThetaResolution(50)

cube = vtkCubeSource()
cube.SetXLength(1)
cube.SetYLength(1)
cube.SetZLength(1)

# Sphere pipeline
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetDiffuseColor(1, 0.2, 0.4)
sphere_actor.SetPosition(-5, 0, 0)

# Cone pipeline
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetDiffuseColor(0.2, 0.4, 1)
cone_actor.SetPosition(0, 0, 0)

# Cube pipeline
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetDiffuseColor(0.2, 1, 0.4)
cube_actor.SetPosition(5, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(cube_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Compute mass properties and create text labels for each source.

# Sphere text label.
tri_filter_sphere = vtkTriangleFilter()
tri_filter_sphere.SetInputConnection(sphere.GetOutputPort())
mass_props_sphere = vtkMassProperties()
mass_props_sphere.SetInputConnection(tri_filter_sphere.GetOutputPort())
summary_io_sphere = StringIO()
old_stdout = sys.stdout
sys.stdout = summary_io_sphere
print(mass_props_sphere)
sys.stdout = old_stdout
summary_sphere = summary_io_sphere.getvalue()
start_idx_sphere = summary_sphere.find("  VolumeX")
label_text_sphere = summary_sphere[start_idx_sphere:] if start_idx_sphere >= 0 else summary_sphere
text_source_sphere = vtkVectorText()
text_source_sphere.SetText(label_text_sphere)
text_mapper_sphere = vtkPolyDataMapper()
text_mapper_sphere.SetInputConnection(text_source_sphere.GetOutputPort())
text_actor_sphere = vtkActor()
text_actor_sphere.SetMapper(text_mapper_sphere)
text_actor_sphere.SetScale(0.2, 0.2, 0.2)
text_actor_sphere.SetPosition(sphere_actor.GetPosition())
text_actor_sphere.AddPosition(-2, -1, 0)
renderer.AddActor(text_actor_sphere)

# Cube text label.
tri_filter_cube = vtkTriangleFilter()
tri_filter_cube.SetInputConnection(cube.GetOutputPort())
mass_props_cube = vtkMassProperties()
mass_props_cube.SetInputConnection(tri_filter_cube.GetOutputPort())
summary_io_cube = StringIO()
old_stdout = sys.stdout
sys.stdout = summary_io_cube
print(mass_props_cube)
sys.stdout = old_stdout
summary_cube = summary_io_cube.getvalue()
start_idx_cube = summary_cube.find("  VolumeX")
label_text_cube = summary_cube[start_idx_cube:] if start_idx_cube >= 0 else summary_cube
text_source_cube = vtkVectorText()
text_source_cube.SetText(label_text_cube)
text_mapper_cube = vtkPolyDataMapper()
text_mapper_cube.SetInputConnection(text_source_cube.GetOutputPort())
text_actor_cube = vtkActor()
text_actor_cube.SetMapper(text_mapper_cube)
text_actor_cube.SetScale(0.2, 0.2, 0.2)
text_actor_cube.SetPosition(cube_actor.GetPosition())
text_actor_cube.AddPosition(-2, -1, 0)
renderer.AddActor(text_actor_cube)

# Cone text label.
tri_filter_cone = vtkTriangleFilter()
tri_filter_cone.SetInputConnection(cone.GetOutputPort())
mass_props_cone = vtkMassProperties()
mass_props_cone.SetInputConnection(tri_filter_cone.GetOutputPort())
summary_io_cone = StringIO()
old_stdout = sys.stdout
sys.stdout = summary_io_cone
print(mass_props_cone)
sys.stdout = old_stdout
summary_cone = summary_io_cone.getvalue()
start_idx_cone = summary_cone.find("  VolumeX")
label_text_cone = summary_cone[start_idx_cone:] if start_idx_cone >= 0 else summary_cone
text_source_cone = vtkVectorText()
text_source_cone.SetText(label_text_cone)
text_mapper_cone = vtkPolyDataMapper()
text_mapper_cone.SetInputConnection(text_source_cone.GetOutputPort())
text_actor_cone = vtkActor()
text_actor_cone.SetMapper(text_mapper_cone)
text_actor_cone.SetScale(0.2, 0.2, 0.2)
text_actor_cone.SetPosition(cone_actor.GetPosition())
text_actor_cone.AddPosition(-2, -1, 0)
renderer.AddActor(text_actor_cone)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(786, 256)
render_window.SetWindowName("mass properties")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Dolly(3)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
