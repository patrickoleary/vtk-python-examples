#!/usr/bin/env python

# Demonstrate vtkPropPicker with two renderers and depth peeling.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Corner renderer with small non-pickable sphere
corner_sphere = vtkSphereSource()
corner_mapper = vtkPolyDataMapper()
corner_mapper.SetInputConnection(corner_sphere.GetOutputPort())
corner_actor = vtkActor()
corner_actor.PickableOff()
corner_actor.SetMapper(corner_mapper)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0, 0, 0.1, 0.1)
renderer_1.AddActor(corner_actor)

# Flat cube as background
cube = vtkCubeSource()
cube.SetXLength(80)
cube.SetYLength(50)
cube.SetZLength(1)

norm = vtkPolyDataNormals()
norm.SetInputConnection(cube.GetOutputPort())
norm.ComputePointNormalsOn()
norm.SplittingOff()

cube_mapper = vtkPolyDataMapper()
cube_mapper.ScalarVisibilityOff()
cube_mapper.SetResolveCoincidentTopologyToPolygonOffset()
cube_mapper.SetInputConnection(norm.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().BackfaceCullingOff()
cube_actor.GetProperty().SetColor(0.93, 0.5, 0.5)
cube_actor.PickableOff()

# Pickable sphere
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(24)
sphere_source.SetThetaResolution(24)
sphere_source.SetRadius(1.75)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().BackfaceCullingOff()
sphere_actor.GetProperty().SetColor(0.73, 0.33, 0.83)
sphere_actor.SetPosition(0, 0, 2)

# Main renderer with depth peeling
renderer_0 = vtkRenderer()
renderer_0.SetUseDepthPeeling(1)
renderer_0.SetMaximumNumberOfPeels(8)
renderer_0.LightFollowCameraOn()
renderer_0.TwoSidedLightingOn()
renderer_0.SetOcclusionRatio(0.0)
renderer_0.AddActor(cube_actor)
renderer_0.AddActor(sphere_actor)

render_window = vtkRenderWindow()
render_window.SetAlphaBitPlanes(1)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("prop picker 2 renderers")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.LightFollowCameraOff()

# Scene
renderer_0.GetActiveCamera().SetParallelProjection(1)
renderer_0.ResetCameraClippingRange()
renderer_0.ResetCamera()

# Pipeline exception: render needed for hardware picking
render_window.Render()

picker = vtkPropPicker()
if picker.Pick(160, 150, 0, renderer_0) != 0:
    path = picker.GetPath()
    prop = path.GetFirstNode().GetViewProp()
    actor = vtkActor.SafeDownCast(prop)
    if actor:
        actor.GetProperty().SetColor(1.0, 1.0, 0.0)

render_window.Render()
interactor.Initialize()
interactor.Start()
