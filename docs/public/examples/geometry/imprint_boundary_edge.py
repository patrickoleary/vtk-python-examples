#!/usr/bin/env python

# Demonstrate vtkImprintFilter with BoundaryEdgeInsertion enabled,
# showing four output type permutations (target cells, imprinted cells,
# projected imprint, imprinted region) in a 2x2 renderer grid with a
# rotated and translated imprint plane.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkImprintFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 12

# Target plane
target = vtkPlaneSource()
target.SetXResolution(resolution)
target.SetYResolution(resolution)
target.SetOrigin(0, 0, 0)
target.SetPoint1(10, 0, 0)
target.SetPoint2(0, 10, 0)

# Imprint plane (rotated and translated)
plane_2 = vtkPlaneSource()
plane_2.SetXResolution(2 * resolution)
plane_2.SetYResolution(2 * resolution)
plane_2.SetOrigin(2.25, 2.25, 0)
plane_2.SetPoint1(7.25, 2.25, 0)
plane_2.SetPoint2(2.25, 7.25, 0)

x_form = vtkTransform()
x_form.RotateZ(-25)
x_form.Translate(-1.5, 1.5, 0)

x_form_f = vtkTransformPolyDataFilter()
x_form_f.SetInputConnection(plane_2.GetOutputPort())
x_form_f.SetTransform(x_form)

# Output: target cells with boundary edge insertion
imprint_filter = vtkImprintFilter()
imprint_filter.SetTargetConnection(target.GetOutputPort())
imprint_filter.SetImprintConnection(x_form_f.GetOutputPort())
imprint_filter.SetTolerance(0.001)
imprint_filter.SetOutputTypeToTargetCells()
imprint_filter.BoundaryEdgeInsertionOn()
imprint_filter.Update()

target_mapper = vtkPolyDataMapper()
target_mapper.SetInputConnection(imprint_filter.GetOutputPort())

target_actor = vtkActor()
target_actor.SetMapper(target_mapper)
target_actor.GetProperty().SetRepresentationToWireframe()
target_actor.GetProperty().SetColor(0, 1, 0)

imprint_mapper = vtkPolyDataMapper()
imprint_mapper.SetInputConnection(x_form_f.GetOutputPort())

imprint_actor = vtkActor()
imprint_actor.SetMapper(imprint_mapper)
imprint_actor.GetProperty().SetRepresentationToWireframe()
imprint_actor.GetProperty().SetColor(1, 0, 0)

# Output: imprinted cells
imprint_filter_2 = vtkImprintFilter()
imprint_filter_2.SetTargetConnection(target.GetOutputPort())
imprint_filter_2.SetImprintConnection(x_form_f.GetOutputPort())
imprint_filter_2.SetTolerance(0.001)
imprint_filter_2.SetOutputTypeToImprintedCells()
imprint_filter_2.BoundaryEdgeInsertionOn()
imprint_filter_2.Update()

target_mapper_2 = vtkPolyDataMapper()
target_mapper_2.SetInputConnection(imprint_filter_2.GetOutputPort())

target_actor_2 = vtkActor()
target_actor_2.SetMapper(target_mapper_2)
target_actor_2.GetProperty().SetRepresentationToWireframe()
target_actor_2.GetProperty().SetColor(0, 1, 0)

imprint_mapper_2 = vtkPolyDataMapper()
imprint_mapper_2.SetInputConnection(x_form_f.GetOutputPort())

imprint_actor_2 = vtkActor()
imprint_actor_2.SetMapper(imprint_mapper_2)
imprint_actor_2.GetProperty().SetRepresentationToWireframe()
imprint_actor_2.GetProperty().SetColor(1, 0, 0)

# Output: projected imprint
imprint_filter_3 = vtkImprintFilter()
imprint_filter_3.SetTargetConnection(target.GetOutputPort())
imprint_filter_3.SetImprintConnection(x_form_f.GetOutputPort())
imprint_filter_3.SetTolerance(0.001)
imprint_filter_3.SetOutputTypeToProjectedImprint()
imprint_filter_3.BoundaryEdgeInsertionOn()
imprint_filter_3.Update()

imprint_mapper_3 = vtkPolyDataMapper()
imprint_mapper_3.SetInputConnection(imprint_filter_3.GetOutputPort())

imprint_actor_3 = vtkActor()
imprint_actor_3.SetMapper(imprint_mapper_3)
imprint_actor_3.GetProperty().SetRepresentationToWireframe()
imprint_actor_3.GetProperty().SetColor(1, 0, 0)

# Output: imprinted region
imprint_filter_4 = vtkImprintFilter()
imprint_filter_4.SetTargetConnection(target.GetOutputPort())
imprint_filter_4.SetImprintConnection(x_form_f.GetOutputPort())
imprint_filter_4.SetTolerance(0.001)
imprint_filter_4.SetOutputTypeToImprintedRegion()
imprint_filter_4.BoundaryEdgeInsertionOn()
imprint_filter_4.Update()

imprint_mapper_4 = vtkPolyDataMapper()
imprint_mapper_4.SetInputConnection(imprint_filter_4.GetOutputPort())

imprint_actor_4 = vtkActor()
imprint_actor_4.SetMapper(imprint_mapper_4)
imprint_actor_4.GetProperty().SetRepresentationToWireframe()
imprint_actor_4.GetProperty().SetColor(1, 0, 0)

# Four renderers in a 2x2 grid
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.AddActor(imprint_actor)
renderer_0.AddActor(target_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.5)
renderer_1.AddActor(imprint_actor_2)
renderer_1.AddActor(target_actor_2)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1.0)
renderer_2.AddActor(imprint_actor_3)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1, 1)
renderer_3.AddActor(imprint_actor_4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(400, 400)
render_window.SetWindowName("imprint boundary edge")

# Scene
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
