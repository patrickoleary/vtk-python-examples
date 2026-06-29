#!/usr/bin/env python

# Demonstrate vtkArrowSource with three variants: normal, centered,
# and inverted-centered arrows rendered side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Normal arrow
arrow = vtkArrowSource()
shaft_radius = arrow.GetShaftRadius()
arrow.SetShaftRadius(shaft_radius * 2.0)
shaft_res = arrow.GetShaftResolution()
arrow.SetShaftResolution(int(shaft_res * 15.0))
tip_res = arrow.GetTipResolution()
arrow.SetTipResolution(int(tip_res * 10.0))
arrow.Update()

arrow_mapper = vtkPolyDataMapper()
arrow_mapper.SetInputConnection(arrow.GetOutputPort())
arrow_mapper.ScalarVisibilityOff()

arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)
arrow_actor.SetPosition(0.0, 0.325, 0.0)
arrow_actor.GetProperty().SetDiffuseColor(0.501, 1.0, 0.0)
arrow_actor.GetProperty().SetSpecular(0.15)
arrow_actor.GetProperty().SetSpecularPower(5.0)

# Centered arrow
arrow_central = vtkArrowSource()
arrow_central.SetShaftRadius(shaft_radius * 2.0)
arrow_central.SetShaftResolution(int(shaft_res * 15.0))
arrow_central.SetTipResolution(int(tip_res * 10.0))
arrow_central.SetArrowOriginToCenter()
arrow_central.Update()

arrow_central_mapper = vtkPolyDataMapper()
arrow_central_mapper.SetInputConnection(arrow_central.GetOutputPort())
arrow_central_mapper.ScalarVisibilityOff()

arrow_central_actor = vtkActor()
arrow_central_actor.SetMapper(arrow_central_mapper)
arrow_central_actor.SetPosition(0.0, 0.0, 0.0)
arrow_central_actor.GetProperty().SetDiffuseColor(1.0, 0.647, 0.0)
arrow_central_actor.GetProperty().SetSpecular(0.15)
arrow_central_actor.GetProperty().SetSpecularPower(5.0)

# Inverted centered arrow
arrow_invert_central = vtkArrowSource()
arrow_invert_central.SetShaftRadius(shaft_radius * 2.0)
arrow_invert_central.SetShaftResolution(int(shaft_res * 15.0))
arrow_invert_central.SetTipResolution(int(tip_res * 10.0))
arrow_invert_central.SetArrowOriginToCenter()
arrow_invert_central.InvertOn()
arrow_invert_central.Update()

arrow_invert_central_mapper = vtkPolyDataMapper()
arrow_invert_central_mapper.SetInputConnection(arrow_invert_central.GetOutputPort())
arrow_invert_central_mapper.ScalarVisibilityOff()

arrow_invert_central_actor = vtkActor()
arrow_invert_central_actor.SetMapper(arrow_invert_central_mapper)
arrow_invert_central_actor.SetPosition(0.0, -0.325, 0.0)
arrow_invert_central_actor.GetProperty().SetDiffuseColor(0.2, 0.8, 1.0)
arrow_invert_central_actor.GetProperty().SetSpecular(0.25)
arrow_invert_central_actor.GetProperty().SetSpecularPower(5.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(arrow_actor)
renderer.AddActor(arrow_central_actor)
renderer.AddActor(arrow_invert_central_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(450, 450)
render_window.SetWindowName("arrow source")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-2.3332, 1.0, 2.25)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
