#!/usr/bin/env python

# Demonstrate vtkExtractPolyDataGeometry extracting polygonal cells
# from a sphere using a cylinder implicit function, with and without
# point culling, and glyph visualization of extracted points.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCylinder
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersExtraction import vtkExtractPolyDataGeometry
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(16)
sphere.SetRadius(1.5)

# Cylinder implicit function rotated 90 degrees about X
cylinder_transform = vtkTransform()
cylinder_transform.RotateX(90)
cyl_func = vtkCylinder()
cyl_func.SetRadius(0.5)
cyl_func.SetTransform(cylinder_transform)

# Extract with pass points on (keeps all original points)
extract = vtkExtractPolyDataGeometry()
extract.SetInputConnection(sphere.GetOutputPort())
extract.SetImplicitFunction(cyl_func)
extract.ExtractBoundaryCellsOn()
extract.PassPointsOn()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(extract.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Extract with pass points off (culls unused points)
extract_2 = vtkExtractPolyDataGeometry()
extract_2.SetInputConnection(sphere.GetOutputPort())
extract_2.SetImplicitFunction(cyl_func)
extract_2.ExtractBoundaryCellsOn()
extract_2.PassPointsOff()

sphere_mapper_2 = vtkPolyDataMapper()
sphere_mapper_2.SetInputConnection(extract_2.GetOutputPort())

sphere_actor_2 = vtkActor()
sphere_actor_2.SetMapper(sphere_mapper_2)
sphere_actor_2.AddPosition(2.5, 0, 0)

# Glyph visualization of points (pass points on)
glyph_sphere = vtkSphereSource()
glyph_sphere.SetRadius(0.05)

glyph = vtkGlyph3D()
glyph.SetInputConnection(extract.GetOutputPort())
glyph.SetSourceConnection(glyph_sphere.GetOutputPort())
glyph.SetScaleModeToDataScalingOff()

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Glyph visualization of points (pass points off)
glyph_2 = vtkGlyph3D()
glyph_2.SetInputConnection(extract_2.GetOutputPort())
glyph_2.SetSourceConnection(glyph_sphere.GetOutputPort())
glyph_2.SetScaleModeToDataScalingOff()

glyph_mapper_2 = vtkPolyDataMapper()
glyph_mapper_2.SetInputConnection(glyph_2.GetOutputPort())

glyph_actor_2 = vtkActor()
glyph_actor_2.SetMapper(glyph_mapper_2)
glyph_actor_2.AddPosition(2.5, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(glyph_actor)
renderer.AddActor(sphere_actor_2)
renderer.AddActor(glyph_actor_2)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extract polydata")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
