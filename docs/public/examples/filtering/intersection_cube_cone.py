#!/usr/bin/env python

# Demonstrate vtkIntersectionPolyDataFilter on a subdivided cube and cone,
# rendering both surfaces (transparent) with the intersection curve.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersModeling import vtkLinearSubdivisionFilter
from vtkmodules.vtkFiltersGeneral import vtkIntersectionPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a subdivided cube
cube = vtkCubeSource()
cube.SetCenter(0.0, 0.0, 0.0)
cube.SetXLength(1.0)
cube.SetYLength(1.0)
cube.SetZLength(1.0)

cube_tri = vtkTriangleFilter()
cube_tri.SetInputConnection(cube.GetOutputPort())

cube_sub = vtkLinearSubdivisionFilter()
cube_sub.SetInputConnection(cube_tri.GetOutputPort())
cube_sub.SetNumberOfSubdivisions(3)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_sub.GetOutputPort())
cube_mapper.ScalarVisibilityOff()

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetOpacity(0.3)
cube_actor.GetProperty().SetColor(1, 0, 0)
cube_actor.GetProperty().SetInterpolationToFlat()

# Create a subdivided cone
cone = vtkConeSource()
cone.SetCenter(0.0, 0.0, 0.0)
cone.SetRadius(0.5)
cone.SetHeight(2.0)
cone.SetResolution(10)
cone.SetDirection(1, 0, 0)

cone_tri = vtkTriangleFilter()
cone_tri.SetInputConnection(cone.GetOutputPort())

cone_sub = vtkLinearSubdivisionFilter()
cone_sub.SetInputConnection(cone_tri.GetOutputPort())
cone_sub.SetNumberOfSubdivisions(3)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_sub.GetOutputPort())
cone_mapper.ScalarVisibilityOff()

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetOpacity(0.3)
cone_actor.GetProperty().SetColor(0, 1, 0)
cone_actor.GetProperty().SetInterpolationToFlat()

# Compute intersection
intersection = vtkIntersectionPolyDataFilter()
intersection.SetInputConnection(0, cube_sub.GetOutputPort())
intersection.SetInputConnection(1, cone_sub.GetOutputPort())
intersection.SetSplitFirstOutput(0)
intersection.SetSplitSecondOutput(0)
intersection.Update()

intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(cube_actor)
renderer.AddViewProp(cone_actor)
renderer.AddViewProp(intersection_actor)
renderer.SetBackground(0.1, 0.2, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("intersection cube cone")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
