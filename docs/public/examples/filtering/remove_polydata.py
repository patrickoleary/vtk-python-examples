#!/usr/bin/env python

# Demonstrate vtkRemovePolyData by appending a plane, sphere, and edges,
# then progressively removing inputs. Four viewports show: original,
# minus plane, minus plane+edges, minus all.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkFeatureEdges,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkRemovePolyData,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 32

# Create a plane
plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.SetOrigin(-1, -1, 1)
plane.SetPoint1(1, -1, 1)
plane.SetPoint2(-1, 1, 1)
plane.Update()

# Create a sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(2 * res)
sphere.SetPhiResolution(res)
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.75)
sphere.Update()

# Transform the plane for edge extraction
xform = vtkTransform()
xform.Translate(0, 0, -2)

xform_f = vtkTransformPolyDataFilter()
xform_f.SetInputConnection(plane.GetOutputPort())
xform_f.SetTransform(xform)

edges = vtkFeatureEdges()
edges.SetInputConnection(xform_f.GetOutputPort())
edges.ExtractAllEdgeTypesOff()
edges.ManifoldEdgesOn()
edges.BoundaryEdgesOn()

# Append all three
append = vtkAppendPolyData()
append.AddInputConnection(plane.GetOutputPort())
append.AddInputConnection(edges.GetOutputPort())
append.AddInputConnection(sphere.GetOutputPort())
append.Update()

before_mapper = vtkPolyDataMapper()
before_mapper.SetInputConnection(append.GetOutputPort())

before_actor = vtkActor()
before_actor.SetMapper(before_mapper)

# Remove the plane
remove = vtkRemovePolyData()
remove.AddInputConnection(append.GetOutputPort())
remove.AddInputConnection(plane.GetOutputPort())
remove.Update()

after_mapper = vtkPolyDataMapper()
after_mapper.SetInputConnection(remove.GetOutputPort())

after_actor = vtkActor()
after_actor.SetMapper(after_mapper)

# Remove the plane and edges
append_2 = vtkAppendPolyData()
append_2.AddInputConnection(plane.GetOutputPort())
append_2.AddInputConnection(edges.GetOutputPort())
append_2.Update()

remove_2 = vtkRemovePolyData()
remove_2.AddInputConnection(append.GetOutputPort())
remove_2.AddInputConnection(append_2.GetOutputPort())
remove_2.Update()

after_mapper_2 = vtkPolyDataMapper()
after_mapper_2.SetInputConnection(remove_2.GetOutputPort())

after_actor_2 = vtkActor()
after_actor_2.SetMapper(after_mapper_2)

# Remove all (self-subtract)
remove_3 = vtkRemovePolyData()
remove_3.AddInputConnection(append.GetOutputPort())
remove_3.AddInputConnection(append.GetOutputPort())
remove_3.Update()

after_mapper_3 = vtkPolyDataMapper()
after_mapper_3.SetInputConnection(remove_3.GetOutputPort())

after_actor_3 = vtkActor()
after_actor_3.SetMapper(after_mapper_3)

# Four renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.25, 1.0)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.25, 0, 0.5, 1.0)
renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.5, 0, 0.75, 1.0)
renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.75, 0, 1.0, 1.0)

renderer_0.AddActor(before_actor)
renderer_1.AddActor(after_actor)
renderer_2.AddActor(after_actor_2)
renderer_3.AddActor(after_actor_3)

renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetBackground(0.1, 0.2, 0.4)

renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(600, 200)
render_window.SetWindowName("remove polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.GetActiveCamera().SetPosition(1, 0, 0.5)
renderer_0.ResetCamera()

interactor.Initialize()
interactor.Start()
