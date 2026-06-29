#!/usr/bin/env python

# Build an ice cream cone from implicit function primitives using vtkSampleFunction.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCone,
    vtkImplicitBoolean,
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersGeneral import vtkMarchingContourFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create implicit function primitives
cone = vtkCone()
cone.SetAngle(20)

vert_plane = vtkPlane()
vert_plane.SetOrigin(0.1, 0, 0)
vert_plane.SetNormal(-1, 0, 0)

base_plane = vtkPlane()
base_plane.SetOrigin(1.2, 0, 0)
base_plane.SetNormal(1, 0, 0)

ice_cream = vtkSphere()
ice_cream.SetCenter(1.333, 0, 0)
ice_cream.SetRadius(0.5)

bite = vtkSphere()
bite.SetCenter(1.5, 0, 0.5)
bite.SetRadius(0.25)

# Combine primitives to build ice-cream cone
the_cone = vtkImplicitBoolean()
the_cone.SetOperationTypeToIntersection()
the_cone.AddFunction(cone)
the_cone.AddFunction(vert_plane)
the_cone.AddFunction(base_plane)

the_cream = vtkImplicitBoolean()
the_cream.SetOperationTypeToDifference()
the_cream.AddFunction(ice_cream)
the_cream.AddFunction(bite)

# Iso-surface to create cone geometry
the_cone_sample = vtkSampleFunction()
the_cone_sample.SetImplicitFunction(the_cone)
the_cone_sample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
the_cone_sample.SetSampleDimensions(60, 60, 60)
the_cone_sample.ComputeNormalsOff()

the_cone_surface = vtkMarchingContourFilter()
the_cone_surface.SetInputConnection(the_cone_sample.GetOutputPort())
the_cone_surface.SetValue(0, 0.0)

# chocolate color
chocolate_rgb = (0.824, 0.412, 0.118)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(the_cone_surface.GetOutputPort())
cone_mapper.ScalarVisibilityOff()

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(chocolate_rgb)

# Iso-surface to create cream geometry
the_cream_sample = vtkSampleFunction()
the_cream_sample.SetImplicitFunction(the_cream)
the_cream_sample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
the_cream_sample.SetSampleDimensions(60, 60, 60)
the_cream_sample.ComputeNormalsOff()

the_cream_surface = vtkMarchingContourFilter()
the_cream_surface.SetInputConnection(the_cream_sample.GetOutputPort())
the_cream_surface.SetValue(0, 0.0)

# mint color
mint_rgb = (0.741, 0.988, 0.788)

cream_mapper = vtkPolyDataMapper()
cream_mapper.SetInputConnection(the_cream_surface.GetOutputPort())
cream_mapper.ScalarVisibilityOff()

cream_actor = vtkActor()
cream_actor.SetMapper(cream_mapper)
cream_actor.GetProperty().SetColor(mint_rgb)

# Rendering
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(cream_actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("ice cream marching contour")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Roll(90)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
