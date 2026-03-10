#!/usr/bin/env python

# Clip a plane with a boolean combination of a sphere and a cylinder.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkCylinder,
    vtkImplicitBoolean,
    vtkSphere,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
midnight_blue = (0.098, 0.098, 0.439)
light_blue = (0.678, 0.847, 0.902)
wheat = (0.961, 0.871, 0.702)

# Source: generate a high-resolution plane
plane = vtkPlaneSource()
plane.SetXResolution(25)
plane.SetYResolution(25)
plane.SetOrigin(-1, -1, 0)
plane.SetPoint1(1, -1, 0)
plane.SetPoint2(-1, 1, 0)

# Implicit function: transformed sphere
transform_sphere = vtkTransform()
transform_sphere.Identity()
transform_sphere.Translate(0.4, -0.4, 0)
transform_sphere.Inverse()

sphere = vtkSphere()
sphere.SetTransform(transform_sphere)
sphere.SetRadius(0.5)

# Implicit function: transformed cylinder
transform_cylinder = vtkTransform()
transform_cylinder.Identity()
transform_cylinder.Translate(-0.4, 0.4, 0)
transform_cylinder.RotateZ(30)
transform_cylinder.RotateY(60)
transform_cylinder.RotateX(90)
transform_cylinder.Inverse()

cylinder = vtkCylinder()
cylinder.SetTransform(transform_cylinder)
cylinder.SetRadius(0.3)

# Implicit function: boolean union of sphere and cylinder
boolean = vtkImplicitBoolean()
boolean.AddFunction(cylinder)
boolean.AddFunction(sphere)

# Filter: clip the plane with the boolean implicit function
clipper = vtkClipPolyData()
clipper.SetInputConnection(plane.GetOutputPort())
clipper.SetClipFunction(boolean)
clipper.GenerateClippedOutputOn()
clipper.GenerateClipScalarsOn()
clipper.SetValue(0)

# Mapper: outside region (wireframe)
clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())
clip_mapper.ScalarVisibilityOff()

# Actor: outside region displayed as wireframe
clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetDiffuseColor(midnight_blue)
clip_actor.GetProperty().SetRepresentationToWireframe()

# Mapper: inside region (solid)
clip_inside_mapper = vtkPolyDataMapper()
clip_inside_mapper.SetInputData(clipper.GetClippedOutput())
clip_inside_mapper.ScalarVisibilityOff()

# Actor: inside region displayed as solid surface
clip_inside_actor = vtkActor()
clip_inside_actor.SetMapper(clip_inside_mapper)
clip_inside_actor.GetProperty().SetDiffuseColor(light_blue)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(clip_inside_actor)
renderer.SetBackground(wheat)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.4)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ClipSphereCylinder")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
