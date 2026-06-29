#!/usr/bin/env python

# Demonstrate vtkImprintFilter by imprinting one plane onto another,
# showing the original planes side-by-side with the imprinted result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersModeling import vtkImprintFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 2

# Target plane
plane_1 = vtkPlaneSource()
plane_1.SetXResolution(3)
plane_1.SetYResolution(1)
plane_1.SetOrigin(0, 0, 0)
plane_1.SetPoint1(2, 0, 0)
plane_1.SetPoint2(0, 1, 0)

plane_1_mapper = vtkPolyDataMapper()
plane_1_mapper.SetInputConnection(plane_1.GetOutputPort())

plane_1_actor = vtkActor()
plane_1_actor.SetMapper(plane_1_mapper)
plane_1_actor.GetProperty().SetColor(0.8, 0.4, 0.2)
plane_1_actor.GetProperty().EdgeVisibilityOn()
plane_1_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Imprint plane
plane_2 = vtkPlaneSource()
plane_2.SetXResolution(resolution)
plane_2.SetYResolution(resolution)
plane_2.SetOrigin(-0.25, 0.25, 0)
plane_2.SetPoint1(1.5, 0.25, 0)
plane_2.SetPoint2(-0.25, 0.75, 0)

plane_2_mapper = vtkPolyDataMapper()
plane_2_mapper.SetInputConnection(plane_2.GetOutputPort())

plane_2_actor = vtkActor()
plane_2_actor.SetMapper(plane_2_mapper)
plane_2_actor.GetProperty().SetColor(0.3, 0.7, 0.9)
plane_2_actor.GetProperty().EdgeVisibilityOn()
plane_2_actor.GetProperty().SetEdgeColor(0, 0, 0)
plane_2_actor.GetProperty().SetOpacity(0.6)

# Imprint filter
imprint = vtkImprintFilter()
imprint.SetTargetConnection(plane_1.GetOutputPort())
imprint.SetImprintConnection(plane_2.GetOutputPort())
imprint.SetTolerance(0.00001)
imprint.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(imprint.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.5, 0.9, 0.4)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0, 0, 0)

# Two renderers: left shows input planes, right shows imprint result
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.AddActor(plane_1_actor)
renderer_0.AddActor(plane_2_actor)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.AddActor(actor)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("imprint filter")

# Scene
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
