#!/usr/bin/env python
# Demonstrate vtkOrientationMarkerWidget with custom axes and annotated cube assembly.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAnnotatedCubeActor,
    vtkAxesActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkMapper,
    vtkPropAssembly,
    vtkPropCollection,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Part 1: create a helical spring for the shaft
dt = math.pi / 20.0
t = 0.0
x = 0.0
n_points = 120
dx = 0.8 / n_points

points = vtkPoints()
line = vtkCellArray()
line.InsertNextCell(n_points + 80)

i = 0
while i < 40:
    points.InsertPoint(i, 0.1 * math.cos(t), x, 0.1 * math.sin(t))
    line.InsertCellPoint(i)
    t += dt
    i += 1

while i < n_points + 40:
    points.InsertPoint(i, 0.1 * math.cos(t), x, 0.1 * math.sin(t))
    line.InsertCellPoint(i)
    t += dt
    x += dx
    i += 1

while i < n_points + 80:
    points.InsertPoint(i, 0.1 * math.cos(t), x, 0.1 * math.sin(t))
    line.InsertCellPoint(i)
    t += dt
    i += 1

wiggle = vtkPolyData()
wiggle.SetPoints(points)
wiggle.SetLines(line)

tube = vtkTubeFilter()
tube.SetInputData(wiggle)
tube.SetGenerateTCoordsToOff()
tube.CappingOff()
tube.SetVaryRadiusToVaryRadiusOff()
tube.SetRadius(0.02)
tube.SetNumberOfSides(5)
tube.Update()

# Part 2: annotated cube for the tip
cube = vtkAnnotatedCubeActor()
cube.SetXPlusFaceText("V")
cube.SetXMinusFaceText("K")
cube.SetYPlusFaceText("T")
cube.SetZPlusFaceText("")
cube.SetZMinusFaceText("")
cube.SetYMinusFaceText("")
cube.SetFaceTextScale(0.666667)

props = vtkPropCollection()
cube.GetActors(props)
append_filter = vtkAppendPolyData()

transform_filter = vtkTransformPolyDataFilter()
transform = vtkTransform()
transform_filter.SetTransform(transform)

n_props = props.GetNumberOfItems()
props.InitTraversal()
for idx in range(n_props):
    node = props.GetNextProp()
    if node and (idx == 0 or idx == (n_props - 1)):
        mapper = node.GetMapper()
        if mapper:
            transform_filter.SetInputConnection(mapper.GetInputConnection(0, 0))
            transform.Identity()
            transform.SetMatrix(node.GetMatrix())
            transform.Scale(2.0, 2.0, 2.0)
            transform_filter.Update()

            newpoly = vtkPolyData()
            newpoly.DeepCopy(transform_filter.GetOutput())
            append_filter.AddInputData(newpoly)

append_filter.Update()

# Create axes actor with custom tip and shaft
axes = vtkAxesActor()
axes.SetTotalLength(1.2, 1.2, 1.2)
axes.SetUserDefinedTip(append_filter.GetOutput())
axes.SetTipTypeToUserDefined()
axes.SetNormalizedShaftLength(0.85, 0.85, 0.85)
axes.SetNormalizedTipLength(0.15, 0.15, 0.15)
axes.AxisLabelsOff()
axes.SetUserDefinedShaft(tube.GetOutput())
axes.SetShaftTypeToUserDefined()

prop = axes.GetXAxisTipProperty()
prop.SetRepresentationToWireframe()
prop.SetDiffuse(0)
prop.SetAmbient(1)
prop.SetColor(1, 0, 1)

prop = axes.GetYAxisTipProperty()
prop.SetRepresentationToWireframe()
prop.SetDiffuse(0)
prop.SetAmbient(1)
prop.SetColor(1, 1, 0)

prop = axes.GetZAxisTipProperty()
prop.SetRepresentationToWireframe()
prop.SetDiffuse(0)
prop.SetAmbient(1)
prop.SetColor(0, 1, 1)

# Configure annotated cube for orientation marker
cube.SetFaceTextScale(0.65)
prop = cube.GetCubeProperty()
prop.SetColor(0.5, 1, 1)

prop = cube.GetTextEdgesProperty()
prop.SetLineWidth(1)
prop.SetDiffuse(0)
prop.SetAmbient(1)
prop.SetColor(0.1800, 0.2800, 0.2300)

vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()

# Anatomic labelling
cube.SetXPlusFaceText("A")
cube.SetXMinusFaceText("P")
cube.SetYPlusFaceText("L")
cube.SetYMinusFaceText("R")
cube.SetZPlusFaceText("S")
cube.SetZMinusFaceText("I")

# Face colors
prop = cube.GetXPlusFaceProperty()
prop.SetColor(0, 0, 1)
prop.SetInterpolationToFlat()
prop = cube.GetXMinusFaceProperty()
prop.SetColor(0, 0, 1)
prop.SetInterpolationToFlat()
prop = cube.GetYPlusFaceProperty()
prop.SetColor(0, 1, 0)
prop.SetInterpolationToFlat()
prop = cube.GetYMinusFaceProperty()
prop.SetColor(0, 1, 0)
prop.SetInterpolationToFlat()
prop = cube.GetZPlusFaceProperty()
prop.SetColor(1, 0, 0)
prop.SetInterpolationToFlat()
prop = cube.GetZMinusFaceProperty()
prop.SetColor(1, 0, 0)
prop.SetInterpolationToFlat()

# Second axes actor simulating left-handed coordinate system
axes2 = vtkAxesActor()
transform.Identity()
transform.RotateY(90)
axes2.SetShaftTypeToCylinder()
axes2.SetUserTransform(transform)
axes2.SetXAxisLabelText("w")
axes2.SetYAxisLabelText("v")
axes2.SetZAxisLabelText("u")
axes2.SetTotalLength(1.5, 1.5, 1.5)
axes2.SetCylinderRadius(0.500 * axes2.GetCylinderRadius())
axes2.SetConeRadius(1.025 * axes2.GetConeRadius())
axes2.SetSphereRadius(1.500 * axes2.GetSphereRadius())

tprop = axes2.GetXAxisCaptionActor2D().GetCaptionTextProperty()
tprop.ItalicOn()
tprop.ShadowOn()
tprop.SetFontFamilyToTimes()

axes2.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)
axes2.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)

# Combine markers into a prop assembly
assembly = vtkPropAssembly()
assembly.AddPart(axes2)
assembly.AddPart(cube)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(axes)
renderer.SetBackground(0.0980, 0.0980, 0.4392)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("orientation marker widget test")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
orientation_marker_widget = vtkOrientationMarkerWidget()
orientation_marker_widget.SetOutlineColor(0.9300, 0.5700, 0.1300)
orientation_marker_widget.SetOrientationMarker(assembly)
orientation_marker_widget.SetInteractor(interactor)
orientation_marker_widget.SetViewport(0.0, 0.0, 0.4, 0.4)
orientation_marker_widget.SetEnabled(1)
orientation_marker_widget.InteractiveOff()
orientation_marker_widget.InteractiveOn()

# Scene
camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(4.5, 4.5, 2.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
