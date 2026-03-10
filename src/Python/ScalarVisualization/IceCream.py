#!/usr/bin/env python

# Model an ice cream cone using boolean combinations of implicit functions.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkCone,
    vtkImplicitBoolean,
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
chocolate = (0.824, 0.412, 0.118)
mint = (0.741, 0.988, 0.788)
slate_gray = (0.439, 0.502, 0.565)

# Implicit function: cone primitive
cone = vtkCone()
cone.SetAngle(20)

# Implicit function: planes to clip the cone to finite extent
vert_plane = vtkPlane()
vert_plane.SetOrigin(0.1, 0, 0)
vert_plane.SetNormal(-1, 0, 0)

base_plane = vtkPlane()
base_plane.SetOrigin(1.2, 0, 0)
base_plane.SetNormal(1, 0, 0)

# Implicit function: ice cream scoop sphere
ice_cream = vtkSphere()
ice_cream.SetCenter(1.333, 0, 0)
ice_cream.SetRadius(0.5)

# Implicit function: bite sphere
bite = vtkSphere()
bite.SetCenter(1.5, 0, 0.5)
bite.SetRadius(0.25)

# Implicit function: boolean intersection to create the cone shape
the_cone = vtkImplicitBoolean()
the_cone.SetOperationTypeToIntersection()
the_cone.AddFunction(cone)
the_cone.AddFunction(vert_plane)
the_cone.AddFunction(base_plane)

# Implicit function: boolean difference to take a bite out of the ice cream
the_cream = vtkImplicitBoolean()
the_cream.SetOperationTypeToDifference()
the_cream.AddFunction(ice_cream)
the_cream.AddFunction(bite)

# Source: sample the cone implicit function on a grid
cone_sample = vtkSampleFunction()
cone_sample.SetImplicitFunction(the_cone)
cone_sample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
cone_sample.SetSampleDimensions(128, 128, 128)
cone_sample.ComputeNormalsOff()

# Filter: extract the cone isosurface
cone_surface = vtkContourFilter()
cone_surface.SetInputConnection(cone_sample.GetOutputPort())
cone_surface.SetValue(0, 0.0)

# Mapper: map cone surface to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_surface.GetOutputPort())
cone_mapper.ScalarVisibilityOff()

# Actor: display the cone
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(chocolate)

# Source: sample the cream implicit function on a grid
cream_sample = vtkSampleFunction()
cream_sample.SetImplicitFunction(the_cream)
cream_sample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
cream_sample.SetSampleDimensions(128, 128, 128)
cream_sample.ComputeNormalsOff()

# Filter: extract the cream isosurface
cream_surface = vtkContourFilter()
cream_surface.SetInputConnection(cream_sample.GetOutputPort())
cream_surface.SetValue(0, 0.0)

# Mapper: map cream surface to graphics primitives
cream_mapper = vtkPolyDataMapper()
cream_mapper.SetInputConnection(cream_surface.GetOutputPort())
cream_mapper.ScalarVisibilityOff()

# Actor: display the ice cream scoop
cream_actor = vtkActor()
cream_actor.SetMapper(cream_mapper)
cream_actor.GetProperty().SetDiffuseColor(mint)
cream_actor.GetProperty().SetSpecular(0.6)
cream_actor.GetProperty().SetSpecularPower(50)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(cream_actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Roll(90)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("IceCream")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
