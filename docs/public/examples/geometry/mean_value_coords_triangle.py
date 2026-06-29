#!/usr/bin/env python
# Demonstrate mean value coordinates interpolation on triangle meshes with vtkProbePolyhedron.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkProbePolyhedron
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Case 0: triangle meshes.
# Create a sphere with elevation scalars.
sphere = vtkSphereSource()
sphere.SetThetaResolution(51)
sphere.SetPhiResolution(17)

ele = vtkElevationFilter()
ele.SetInputConnection(sphere.GetOutputPort())
ele.SetLowPoint(-0.5, 0, 0)
ele.SetHighPoint(0.5, 0, 0)
ele.Update()

# Clip the sphere in half.
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 0, 1)

clip = vtkClipPolyData()
clip.SetInputConnection(ele.GetOutputPort())
clip.SetClipFunction(plane)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(clip.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Sample the sphere mesh with a plane using faster MVC for triangle meshes.
p_source = vtkPlaneSource()
p_source.SetOrigin(-1.0, -1.0, 0)
p_source.SetPoint1(1.0, -1.0, 0)
p_source.SetPoint2(-1.0, 1.0, 0)
p_source.SetXResolution(50)
p_source.SetYResolution(50)

interp = vtkProbePolyhedron()
interp.SetInputConnection(p_source.GetOutputPort())
interp.SetSourceConnection(ele.GetOutputPort())

interp_mapper = vtkPolyDataMapper()
interp_mapper.SetInputConnection(interp.GetOutputPort())
interp_actor = vtkActor()
interp_actor.SetMapper(interp_mapper)

# Case 1: general meshes (second sphere).
sphere_1 = vtkSphereSource()
sphere_1.SetThetaResolution(51)
sphere_1.SetPhiResolution(17)

ele_1 = vtkElevationFilter()
ele_1.SetInputConnection(sphere_1.GetOutputPort())
ele_1.SetLowPoint(-0.5, 0, 0)
ele_1.SetHighPoint(0.5, 0, 0)
ele_1.Update()

# Sample with second plane using general MVC.
p_source_1 = vtkPlaneSource()
p_source_1.SetOrigin(-1.0, -1.0, 0)
p_source_1.SetPoint1(1.0, -1.0, 0)
p_source_1.SetPoint2(-1.0, 1.0, 0)
p_source_1.SetXResolution(50)
p_source_1.SetYResolution(50)

interp_1 = vtkProbePolyhedron()
interp_1.SetInputConnection(p_source_1.GetOutputPort())
interp_1.SetSourceConnection(ele_1.GetOutputPort())

interp_mapper_1 = vtkPolyDataMapper()
interp_mapper_1.SetInputConnection(interp_1.GetOutputPort())
interp_actor_1 = vtkActor()
interp_actor_1.SetMapper(interp_mapper_1)

# Turn off lighting for all actors.
light_property = vtkProperty()
light_property.LightingOff()
sphere_actor.SetProperty(light_property)
interp_actor.SetProperty(light_property)
interp_actor_1.SetProperty(light_property)

# Renderers.
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(sphere_actor)
renderer_0.AddActor(interp_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(sphere_actor)
renderer_1.AddActor(interp_actor_1)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("mean value coords triangle")

# Scene.
renderer_0.ResetCamera()
renderer_0.SetBackground(1, 1, 1)
renderer_1.ResetCamera()
renderer_1.SetBackground(1, 1, 1)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
