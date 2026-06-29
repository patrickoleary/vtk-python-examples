#!/usr/bin/env python

# Demonstrate vtkImprintFilter by imprinting a rotated plane onto a target
# plane and rendering the wireframe result.

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
plane_1 = vtkPlaneSource()
plane_1.SetXResolution(resolution)
plane_1.SetYResolution(resolution)
plane_1.SetOrigin(0, 0, 0)
plane_1.SetPoint1(10, 0, 0)
plane_1.SetPoint2(0, 10, 0)

# Imprint plane (rotated)
plane_2 = vtkPlaneSource()
plane_2.SetXResolution(2 * resolution)
plane_2.SetYResolution(2 * resolution)
plane_2.SetOrigin(2.25, 2.25, 0)
plane_2.SetPoint1(7.25, 2.25, 0)
plane_2.SetPoint2(2.25, 7.25, 0)

x_form = vtkTransform()
x_form.RotateZ(-25)

x_form_f = vtkTransformPolyDataFilter()
x_form_f.SetInputConnection(plane_2.GetOutputPort())
x_form_f.SetTransform(x_form)

# Imprint filter
imprint = vtkImprintFilter()
imprint.SetTargetConnection(plane_1.GetOutputPort())
imprint.SetImprintConnection(x_form_f.GetOutputPort())
imprint.SetTolerance(0.001)
imprint.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(imprint.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("imprint rotated plane")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
