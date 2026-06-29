#!/usr/bin/env python

# Demonstrate vtkSmoothPolyDataFilter on a semi-cylinder created via
# vtkRotationalExtrusionFilter, warped with Brownian points, then
# smoothed and rendered with normals.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkSmoothPolyDataFilter
from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints, vtkWarpVector
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()

# Create a semi-cylinder via line + rotational extrusion
line = vtkLineSource()
line.SetPoint1(0, 1, 0)
line.SetPoint2(0, 1, 2)
line.SetResolution(10)

line_sweeper = vtkRotationalExtrusionFilter()
line_sweeper.SetResolution(20)
line_sweeper.SetInputConnection(line.GetOutputPort())
line_sweeper.SetAngle(270)

# Add Brownian noise
bump = vtkBrownianPoints()
bump.SetInputConnection(line_sweeper.GetOutputPort())

warp = vtkWarpVector()
warp.SetInputConnection(bump.GetOutputPort())
warp.SetScaleFactor(0.2)

# Smooth the warped surface
smooth = vtkSmoothPolyDataFilter()
smooth.SetInputConnection(warp.GetOutputPort())
smooth.SetNumberOfIterations(50)
smooth.BoundarySmoothingOn()
smooth.SetFeatureAngle(120)
smooth.SetEdgeAngle(90)
smooth.SetRelaxationFactor(0.025)

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(smooth.GetOutputPort())

# Smoothed cylinder actor
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(normals.GetOutputPort())

tomato_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("tomato", tomato_rgb)

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetInterpolationToGouraud()
cylinder_actor.GetProperty().SetInterpolationToFlat()
cylinder_actor.GetProperty().SetColor(tomato_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cylinder_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 300)
render_window.SetWindowName("smooth cyl")

# Scene
camera = vtkCamera()
camera.SetClippingRange(0.576398, 28.8199)
camera.SetFocalPoint(0.0463079, -0.0356571, 1.01993)
camera.SetPosition(-2.47044, 2.39516, -3.56066)
camera.SetViewUp(0.607296, -0.513537, -0.606195)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
