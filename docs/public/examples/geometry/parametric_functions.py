#!/usr/bin/env python
# Demonstrate parametric surfaces: torus, Klein, Mobius, super toroid, ellipsoid, splines, and more.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonComputationalGeometry import (
    vtkParametricBoy,
    vtkParametricConicSpiral,
    vtkParametricCrossCap,
    vtkParametricDini,
    vtkParametricEllipsoid,
    vtkParametricEnneper,
    vtkParametricFigure8Klein,
    vtkParametricKlein,
    vtkParametricMobius,
    vtkParametricRandomHills,
    vtkParametricRoman,
    vtkParametricSpline,
    vtkParametricSuperEllipsoid,
    vtkParametricSuperToroid,
    vtkParametricTorus,
)
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
)

# Torus.
torus = vtkParametricTorus()
torus_source = vtkParametricFunctionSource()
torus_source.SetParametricFunction(torus)
torus_source.SetScalarModeToPhase()

torus_mapper = vtkPolyDataMapper()
torus_mapper.SetInputConnection(torus_source.GetOutputPort())
torus_mapper.SetScalarRange(0, 360)

torus_actor = vtkActor()
torus_actor.SetMapper(torus_mapper)
torus_actor.SetPosition(0, 12, 0)

torus_text_mapper = vtkTextMapper()
torus_text_mapper.SetInput("Torus")
torus_text_mapper.GetTextProperty().SetJustificationToCentered()
torus_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
torus_text_mapper.GetTextProperty().SetColor(1, 0, 0)
torus_text_mapper.GetTextProperty().SetFontSize(14)
torus_text_actor = vtkActor2D()
torus_text_actor.SetMapper(torus_text_mapper)
torus_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
torus_text_actor.GetPositionCoordinate().SetValue(0, 9.5, 0)

# Klein bottle.
klein = vtkParametricKlein()
klein_source = vtkParametricFunctionSource()
klein_source.SetParametricFunction(klein)
klein_source.SetScalarModeToU0V0()

klein_mapper = vtkPolyDataMapper()
klein_mapper.SetInputConnection(klein_source.GetOutputPort())
klein_mapper.SetScalarRange(0, 3)

klein_actor = vtkActor()
klein_actor.SetMapper(klein_mapper)
klein_actor.SetPosition(8, 10.5, 0)

klein_text_mapper = vtkTextMapper()
klein_text_mapper.SetInput("Klein")
klein_text_mapper.GetTextProperty().SetJustificationToCentered()
klein_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
klein_text_mapper.GetTextProperty().SetColor(1, 0, 0)
klein_text_mapper.GetTextProperty().SetFontSize(14)
klein_text_actor = vtkActor2D()
klein_text_actor.SetMapper(klein_text_mapper)
klein_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
klein_text_actor.GetPositionCoordinate().SetValue(8, 9.5, 0)

# Figure-8 Klein.
fig8_klein = vtkParametricFigure8Klein()
fig8_klein_source = vtkParametricFunctionSource()
fig8_klein_source.SetParametricFunction(fig8_klein)
fig8_klein_source.GenerateTextureCoordinatesOn()

fig8_klein_mapper = vtkPolyDataMapper()
fig8_klein_mapper.SetInputConnection(fig8_klein_source.GetOutputPort())
fig8_klein_mapper.SetScalarRange(0, 3)

fig8_klein_actor = vtkActor()
fig8_klein_actor.SetMapper(fig8_klein_mapper)
fig8_klein_actor.SetPosition(16, 12, 0)

fig8_klein_text_mapper = vtkTextMapper()
fig8_klein_text_mapper.SetInput("Fig-8.Klein")
fig8_klein_text_mapper.GetTextProperty().SetJustificationToCentered()
fig8_klein_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
fig8_klein_text_mapper.GetTextProperty().SetColor(1, 0, 0)
fig8_klein_text_mapper.GetTextProperty().SetFontSize(14)
fig8_klein_text_actor = vtkActor2D()
fig8_klein_text_actor.SetMapper(fig8_klein_text_mapper)
fig8_klein_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
fig8_klein_text_actor.GetPositionCoordinate().SetValue(16, 9.5, 0)

# Mobius strip.
mobius = vtkParametricMobius()
mobius_source = vtkParametricFunctionSource()
mobius_source.SetParametricFunction(mobius)
mobius_source.GenerateTextureCoordinatesOn()

mobius_mapper = vtkPolyDataMapper()
mobius_mapper.SetInputConnection(mobius_source.GetOutputPort())

mobius_actor = vtkActor()
mobius_actor.SetMapper(mobius_mapper)
mobius_actor.RotateX(45)
mobius_actor.SetPosition(24, 12, 0)

mobius_text_mapper = vtkTextMapper()
mobius_text_mapper.SetInput("Mobius")
mobius_text_mapper.GetTextProperty().SetJustificationToCentered()
mobius_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
mobius_text_mapper.GetTextProperty().SetColor(1, 0, 0)
mobius_text_mapper.GetTextProperty().SetFontSize(14)
mobius_text_actor = vtkActor2D()
mobius_text_actor.SetMapper(mobius_text_mapper)
mobius_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
mobius_text_actor.GetPositionCoordinate().SetValue(24, 9.5, 0)

# Super toroid.
toroid = vtkParametricSuperToroid()
toroid.SetN1(2)
toroid.SetN2(3)
toroid_source = vtkParametricFunctionSource()
toroid_source.SetParametricFunction(toroid)
toroid_source.SetScalarModeToU()

toroid_mapper = vtkPolyDataMapper()
toroid_mapper.SetInputConnection(toroid_source.GetOutputPort())
toroid_mapper.SetScalarRange(0, 6.28)

toroid_actor = vtkActor()
toroid_actor.SetMapper(toroid_mapper)
toroid_actor.SetPosition(0, 4, 0)

toroid_text_mapper = vtkTextMapper()
toroid_text_mapper.SetInput("Super.Toroid")
toroid_text_mapper.GetTextProperty().SetJustificationToCentered()
toroid_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
toroid_text_mapper.GetTextProperty().SetColor(1, 0, 0)
toroid_text_mapper.GetTextProperty().SetFontSize(14)
toroid_text_actor = vtkActor2D()
toroid_text_actor.SetMapper(toroid_text_mapper)
toroid_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
toroid_text_actor.GetPositionCoordinate().SetValue(0, 1.5, 0)

# Super ellipsoid.
super_ellipsoid = vtkParametricSuperEllipsoid()
super_ellipsoid.SetXRadius(1.25)
super_ellipsoid.SetYRadius(1.5)
super_ellipsoid.SetZRadius(1.0)
super_ellipsoid.SetN1(1.1)
super_ellipsoid.SetN2(1.75)
super_ellipsoid_source = vtkParametricFunctionSource()
super_ellipsoid_source.SetParametricFunction(super_ellipsoid)
super_ellipsoid_source.SetScalarModeToV()

super_ellipsoid_mapper = vtkPolyDataMapper()
super_ellipsoid_mapper.SetInputConnection(super_ellipsoid_source.GetOutputPort())
super_ellipsoid_mapper.SetScalarRange(0, 3.14)

super_ellipsoid_actor = vtkActor()
super_ellipsoid_actor.SetMapper(super_ellipsoid_mapper)
super_ellipsoid_actor.SetPosition(8, 4, 0)

super_ellipsoid_text_mapper = vtkTextMapper()
super_ellipsoid_text_mapper.SetInput("Super.Ellipsoid")
super_ellipsoid_text_mapper.GetTextProperty().SetJustificationToCentered()
super_ellipsoid_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
super_ellipsoid_text_mapper.GetTextProperty().SetColor(1, 0, 0)
super_ellipsoid_text_mapper.GetTextProperty().SetFontSize(14)
super_ellipsoid_text_actor = vtkActor2D()
super_ellipsoid_text_actor.SetMapper(super_ellipsoid_text_mapper)
super_ellipsoid_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
super_ellipsoid_text_actor.GetPositionCoordinate().SetValue(8, 1.5, 0)

# Open 1D spline.
spline_points = [
    [0.50380158308139134, -0.60679315105396936, -0.37248976406291578],
    [-0.4354646054261665, -0.85362339758017258, -0.84844312996065385],
    [0.2163147512899315, -0.39797507012168643, -0.76700353518454523],
    [0.97158415334838644, -0.58513467367046257, -0.35846037946569753],
    [-0.64359767997804918, -0.94620739107309249, -0.90762176546623086],
    [-0.39901219094126117, -0.1978931497772658, 0.0098316934936828471],
    [-0.75872745167404765, 0.067719714281950116, 0.165237936733867],
    [-0.84599731389712418, -0.67685466896596114, 0.10357868909071133],
    [0.84702754758625654, -0.0080077177882230677, -0.58571286666473044],
    [-0.076150034124101484, 0.14637647622561856, 0.1494359239700418],
]
input_points = vtkPoints()
for i in range(10):
    input_points.InsertPoint(i, spline_points[i])

spline = vtkParametricSpline()
spline.SetPoints(input_points)
spline.ClosedOff()
spline_source = vtkParametricFunctionSource()
spline_source.SetParametricFunction(spline)

spline_mapper = vtkPolyDataMapper()
spline_mapper.SetInputConnection(spline_source.GetOutputPort())

spline_actor = vtkActor()
spline_actor.SetMapper(spline_mapper)
spline_actor.SetPosition(16, 4, 0)
spline_actor.GetProperty().SetColor(0, 0, 0)

spline_text_mapper = vtkTextMapper()
spline_text_mapper.SetInput("Open.Spline")
spline_text_mapper.GetTextProperty().SetJustificationToCentered()
spline_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
spline_text_mapper.GetTextProperty().SetColor(1, 0, 0)
spline_text_mapper.GetTextProperty().SetFontSize(14)
spline_text_actor = vtkActor2D()
spline_text_actor.SetMapper(spline_text_mapper)
spline_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
spline_text_actor.GetPositionCoordinate().SetValue(16, 1.5, 0)

# Closed 1D spline.
spline_2 = vtkParametricSpline()
spline_2.SetPoints(input_points)
spline_2.ClosedOn()
spline_2_source = vtkParametricFunctionSource()
spline_2_source.SetParametricFunction(spline_2)

spline_2_mapper = vtkPolyDataMapper()
spline_2_mapper.SetInputConnection(spline_2_source.GetOutputPort())

spline_2_actor = vtkActor()
spline_2_actor.SetMapper(spline_2_mapper)
spline_2_actor.SetPosition(24, 4, 0)
spline_2_actor.GetProperty().SetColor(0, 0, 0)

spline_2_text_mapper = vtkTextMapper()
spline_2_text_mapper.SetInput("Closed.Spline")
spline_2_text_mapper.GetTextProperty().SetJustificationToCentered()
spline_2_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
spline_2_text_mapper.GetTextProperty().SetColor(1, 0, 0)
spline_2_text_mapper.GetTextProperty().SetFontSize(14)
spline_2_text_actor = vtkActor2D()
spline_2_text_actor.SetMapper(spline_2_text_mapper)
spline_2_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
spline_2_text_actor.GetPositionCoordinate().SetValue(24, 1.5, 0)

# Conic spiral.
sconic = vtkParametricConicSpiral()
sconic.SetA(0.8)
sconic.SetB(2.5)
sconic.SetC(0.4)
sconic_source = vtkParametricFunctionSource()
sconic_source.SetParametricFunction(sconic)
sconic_source.SetScalarModeToDistance()

sconic_mapper = vtkPolyDataMapper()
sconic_mapper.SetInputConnection(sconic_source.GetOutputPort())
sconic_mapper.SetScalarRange(0, 9)

sconic_actor = vtkActor()
sconic_actor.SetMapper(sconic_mapper)
sconic_actor.SetPosition(0, -4, 0)
sconic_actor.SetScale(1.2, 1.2, 1.2)

sconic_text_mapper = vtkTextMapper()
sconic_text_mapper.SetInput("Spiral.Conic")
sconic_text_mapper.GetTextProperty().SetJustificationToCentered()
sconic_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
sconic_text_mapper.GetTextProperty().SetColor(1, 0, 0)
sconic_text_mapper.GetTextProperty().SetFontSize(14)
sconic_text_actor = vtkActor2D()
sconic_text_actor.SetMapper(sconic_text_mapper)
sconic_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
sconic_text_actor.GetPositionCoordinate().SetValue(0, -6.5, 0)

# Boy's surface.
boy = vtkParametricBoy()
boy_source = vtkParametricFunctionSource()
boy_source.SetParametricFunction(boy)
boy_source.SetScalarModeToModulus()

boy_mapper = vtkPolyDataMapper()
boy_mapper.SetInputConnection(boy_source.GetOutputPort())
boy_mapper.SetScalarRange(0, 2)

boy_actor = vtkActor()
boy_actor.SetMapper(boy_mapper)
boy_actor.SetPosition(8, -4, 0)
boy_actor.SetScale(1.5, 1.5, 1.5)

boy_text_mapper = vtkTextMapper()
boy_text_mapper.SetInput("Boy")
boy_text_mapper.GetTextProperty().SetJustificationToCentered()
boy_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
boy_text_mapper.GetTextProperty().SetColor(1, 0, 0)
boy_text_mapper.GetTextProperty().SetFontSize(14)
boy_text_actor = vtkActor2D()
boy_text_actor.SetMapper(boy_text_mapper)
boy_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
boy_text_actor.GetPositionCoordinate().SetValue(8, -6.5, 0)

# Cross cap.
cross_cap = vtkParametricCrossCap()
cross_cap_source = vtkParametricFunctionSource()
cross_cap_source.SetParametricFunction(cross_cap)
cross_cap_source.SetScalarModeToY()

cross_cap_mapper = vtkPolyDataMapper()
cross_cap_mapper.SetInputConnection(cross_cap_source.GetOutputPort())

cross_cap_actor = vtkActor()
cross_cap_actor.SetMapper(cross_cap_mapper)
cross_cap_actor.RotateX(65)
cross_cap_actor.SetPosition(16, -4, 0)
cross_cap_actor.SetScale(1.5, 1.5, 1.5)

cross_cap_text_mapper = vtkTextMapper()
cross_cap_text_mapper.SetInput("Cross.Cap")
cross_cap_text_mapper.GetTextProperty().SetJustificationToCentered()
cross_cap_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
cross_cap_text_mapper.GetTextProperty().SetColor(1, 0, 0)
cross_cap_text_mapper.GetTextProperty().SetFontSize(14)
cross_cap_text_actor = vtkActor2D()
cross_cap_text_actor.SetMapper(cross_cap_text_mapper)
cross_cap_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
cross_cap_text_actor.GetPositionCoordinate().SetValue(16, -6.5, 0)

# Dini's surface.
dini = vtkParametricDini()
dini_source = vtkParametricFunctionSource()
dini_source.SetScalarModeToDistance()
dini_source.SetParametricFunction(dini)

dini_mapper = vtkPolyDataMapper()
dini_mapper.SetInputConnection(dini_source.GetOutputPort())

dini_actor = vtkActor()
dini_actor.SetMapper(dini_mapper)
dini_actor.RotateX(-90)
dini_actor.SetPosition(24, -3, 0)
dini_actor.SetScale(1.5, 1.5, 0.5)

dini_text_mapper = vtkTextMapper()
dini_text_mapper.SetInput("Dini")
dini_text_mapper.GetTextProperty().SetJustificationToCentered()
dini_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
dini_text_mapper.GetTextProperty().SetColor(1, 0, 0)
dini_text_mapper.GetTextProperty().SetFontSize(14)
dini_text_actor = vtkActor2D()
dini_text_actor.SetMapper(dini_text_mapper)
dini_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
dini_text_actor.GetPositionCoordinate().SetValue(24, -6.5, 0)

# Enneper's surface.
enneper = vtkParametricEnneper()
enneper_source = vtkParametricFunctionSource()
enneper_source.SetParametricFunction(enneper)
enneper_source.SetScalarModeToQuadrant()

enneper_mapper = vtkPolyDataMapper()
enneper_mapper.SetInputConnection(enneper_source.GetOutputPort())
enneper_mapper.SetScalarRange(1, 4)

enneper_actor = vtkActor()
enneper_actor.SetMapper(enneper_mapper)
enneper_actor.SetPosition(0, -12, 0)
enneper_actor.SetScale(0.25, 0.25, 0.25)

enneper_text_mapper = vtkTextMapper()
enneper_text_mapper.SetInput("Enneper")
enneper_text_mapper.GetTextProperty().SetJustificationToCentered()
enneper_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
enneper_text_mapper.GetTextProperty().SetColor(1, 0, 0)
enneper_text_mapper.GetTextProperty().SetFontSize(14)
enneper_text_actor = vtkActor2D()
enneper_text_actor.SetMapper(enneper_text_mapper)
enneper_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
enneper_text_actor.GetPositionCoordinate().SetValue(0, -14.5, 0)

# Ellipsoid.
ellipsoid = vtkParametricEllipsoid()
ellipsoid.SetXRadius(1)
ellipsoid.SetYRadius(0.75)
ellipsoid.SetZRadius(0.5)
ellipsoid_source = vtkParametricFunctionSource()
ellipsoid_source.SetParametricFunction(ellipsoid)
ellipsoid_source.SetScalarModeToZ()

ellipsoid_mapper = vtkPolyDataMapper()
ellipsoid_mapper.SetInputConnection(ellipsoid_source.GetOutputPort())
ellipsoid_mapper.SetScalarRange(-0.5, 0.5)

ellipsoid_actor = vtkActor()
ellipsoid_actor.SetMapper(ellipsoid_mapper)
ellipsoid_actor.SetPosition(8, -12, 0)
ellipsoid_actor.SetScale(1.5, 1.5, 1.5)

ellipsoid_text_mapper = vtkTextMapper()
ellipsoid_text_mapper.SetInput("Ellipsoid")
ellipsoid_text_mapper.GetTextProperty().SetJustificationToCentered()
ellipsoid_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
ellipsoid_text_mapper.GetTextProperty().SetColor(1, 0, 0)
ellipsoid_text_mapper.GetTextProperty().SetFontSize(14)
ellipsoid_text_actor = vtkActor2D()
ellipsoid_text_actor.SetMapper(ellipsoid_text_mapper)
ellipsoid_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
ellipsoid_text_actor.GetPositionCoordinate().SetValue(8, -14.5, 0)

# Random hills.
random_hills = vtkParametricRandomHills()
random_hills.AllowRandomGenerationOn()
random_hills_source = vtkParametricFunctionSource()
random_hills_source.SetParametricFunction(random_hills)
random_hills_source.GenerateTextureCoordinatesOn()

random_hills_mapper = vtkPolyDataMapper()
random_hills_mapper.SetInputConnection(random_hills_source.GetOutputPort())

random_hills_actor = vtkActor()
random_hills_actor.SetMapper(random_hills_mapper)
random_hills_actor.SetPosition(16, -14, 0)
random_hills_actor.SetScale(0.2, 0.2, 0.2)

random_hills_text_mapper = vtkTextMapper()
random_hills_text_mapper.SetInput("Random.Hills")
random_hills_text_mapper.GetTextProperty().SetJustificationToCentered()
random_hills_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
random_hills_text_mapper.GetTextProperty().SetColor(1, 0, 0)
random_hills_text_mapper.GetTextProperty().SetFontSize(14)
random_hills_text_actor = vtkActor2D()
random_hills_text_actor.SetMapper(random_hills_text_mapper)
random_hills_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
random_hills_text_actor.GetPositionCoordinate().SetValue(16, -14.5, 0)

# Steiner's Roman surface.
roman = vtkParametricRoman()
roman.SetRadius(1.5)
roman_source = vtkParametricFunctionSource()
roman_source.SetParametricFunction(roman)
roman_source.SetScalarModeToX()

roman_mapper = vtkPolyDataMapper()
roman_mapper.SetInputConnection(roman_source.GetOutputPort())

roman_actor = vtkActor()
roman_actor.SetMapper(roman_mapper)
roman_actor.SetPosition(24, -12, 0)

roman_text_mapper = vtkTextMapper()
roman_text_mapper.SetInput("Roman")
roman_text_mapper.GetTextProperty().SetJustificationToCentered()
roman_text_mapper.GetTextProperty().SetVerticalJustificationToCentered()
roman_text_mapper.GetTextProperty().SetColor(1, 0, 0)
roman_text_mapper.GetTextProperty().SetFontSize(14)
roman_text_actor = vtkActor2D()
roman_text_actor.SetMapper(roman_text_mapper)
roman_text_actor.GetPositionCoordinate().SetCoordinateSystemToWorld()
roman_text_actor.GetPositionCoordinate().SetValue(24, -14.5, 0)

# Rendering pipeline.
renderer = vtkRenderer()

renderer.AddActor(torus_actor)
renderer.AddActor(klein_actor)
renderer.AddActor(fig8_klein_actor)
renderer.AddActor(toroid_actor)
renderer.AddActor(super_ellipsoid_actor)
renderer.AddActor(mobius_actor)
renderer.AddActor(spline_actor)
renderer.AddActor(spline_2_actor)
renderer.AddActor(sconic_actor)
renderer.AddActor(boy_actor)
renderer.AddActor(cross_cap_actor)
renderer.AddActor(dini_actor)
renderer.AddActor(enneper_actor)
renderer.AddActor(ellipsoid_actor)
renderer.AddActor(random_hills_actor)
renderer.AddActor(roman_actor)

renderer.AddActor(torus_text_actor)
renderer.AddActor(klein_text_actor)
renderer.AddActor(fig8_klein_text_actor)
renderer.AddActor(mobius_text_actor)
renderer.AddActor(toroid_text_actor)
renderer.AddActor(super_ellipsoid_text_actor)
renderer.AddActor(spline_text_actor)
renderer.AddActor(spline_2_text_actor)
renderer.AddActor(sconic_text_actor)
renderer.AddActor(boy_text_actor)
renderer.AddActor(cross_cap_text_actor)
renderer.AddActor(dini_text_actor)
renderer.AddActor(enneper_text_actor)
renderer.AddActor(ellipsoid_text_actor)
renderer.AddActor(random_hills_text_actor)
renderer.AddActor(roman_text_actor)

renderer.SetBackground(0.7, 0.8, 1)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("parametric functions")

renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
