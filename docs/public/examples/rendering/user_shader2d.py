#!/usr/bin/env python

# Demonstrate user shader replacements on a 2D mapper with a custom uniform for a grid pattern.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkCoordinate,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

plane = vtkPlaneSource()

mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(plane.GetOutputPort())

# Transform coordinates from world to normalized viewport
p_coord = vtkCoordinate()
p_coord.SetCoordinateSystemToWorld()

coord = vtkCoordinate()
coord.SetCoordinateSystemToNormalizedViewport()
coord.SetReferenceCoordinate(p_coord)
mapper.SetTransformCoordinate(coord)

actor = vtkActor2D()
actor.SetMapper(mapper)

# Fragment shader replacements: sinusoidal grid pattern
sp = actor.GetShaderProperty()
sp.AddFragmentShaderReplacement(
    "//VTK::CustomUniforms::Dec", True,
    "\nuniform float time;\n",
    False,
)
sp.AddFragmentShaderReplacement(
    "//VTK::Color::Impl", True,
    "\ngl_FragData[0] = vec4(sin(tcoordVCVSOutput.xy * time * 0.01), 0.0, 1.0);\n",
    False,
)

# Set the time uniform to produce a static grid
sp.GetFragmentCustomUniforms().SetUniformf("time", 150)

renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddViewProp(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("user shader2d")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
