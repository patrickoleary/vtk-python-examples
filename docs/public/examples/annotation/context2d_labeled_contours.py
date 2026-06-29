#!/usr/bin/env python

# Display labeled contours in a 2D context using vtkLabeledContourPolyDataItem.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkLookupTable,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkRectd,
    vtkRecti,
)
from vtkmodules.vtkChartsCore import (
    vtkAxis,
    vtkInteractiveArea,
)
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkStripper,
)
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    VTK_SCALAR_MODE_USE_POINT_DATA,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
    vtkTextPropertyCollection,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkLabeledContourPolyDataItem

contour_values = [84.0, 105.0, 126.0, 148.0, 169.0, 191.0, 212.0, 233.0, 255.0, 276.0]

# Wavelet source and contour pipeline
wavelet = vtkRTAnalyticSource()

plane = vtkPlane()
plane.SetOrigin(0.0, 0.0, 0.0)
plane.SetNormal(0.0, 0.0, 1.0)

plane_cut = vtkCutter()
plane_cut.SetInputConnection(wavelet.GetOutputPort())
plane_cut.SetCutFunction(plane)

contours = vtkContourFilter()
contours.SetInputConnection(plane_cut.GetOutputPort())
contours.SetNumberOfContours(len(contour_values))
contours.SetComputeScalars(True)
contours.SetValue(0, 84.0)
contours.SetValue(1, 105.0)
contours.SetValue(2, 126.0)
contours.SetValue(3, 148.0)
contours.SetValue(4, 169.0)
contours.SetValue(5, 191.0)
contours.SetValue(6, 212.0)
contours.SetValue(7, 233.0)
contours.SetValue(8, 255.0)
contours.SetValue(9, 276.0)

stripper = vtkStripper()
stripper.SetInputConnection(contours.GetOutputPort())
stripper.Update()
pd = stripper.GetOutput()
pd_bounds = pd.GetBounds()

# Lookup table
lut = vtkLookupTable()
lut.SetNumberOfColors(10)
lut.SetRange(84.0, 277.0)
lut.Build()

# Text properties for each contour value
tprops = vtkTextPropertyCollection()

col_0 = [0.0, 0.0, 0.0]
lut.GetColor(84.0, col_0)
text_prop_0 = vtkTextProperty()
text_prop_0.SetColor(*col_0)
text_prop_0.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_0.SetFrame(0)
text_prop_0.SetFontSize(16)
text_prop_0.SetBold(0)
text_prop_0.SetItalic(0)
text_prop_0.SetShadow(0)
text_prop_0.SetJustification(0)
text_prop_0.SetBackgroundOpacity(1.0)
text_prop_0.SetVerticalJustification(1)
text_prop_0.SetUseTightBoundingBox(0)
text_prop_0.SetOrientation(0.0)
text_prop_0.SetLineSpacing(1.1)
text_prop_0.SetLineOffset(0.0)
tprops.AddItem(text_prop_0)

col_1 = [0.0, 0.0, 0.0]
lut.GetColor(105.0, col_1)
text_prop_1 = vtkTextProperty()
text_prop_1.SetColor(*col_1)
text_prop_1.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_1.SetFrame(0)
text_prop_1.SetFontSize(16)
text_prop_1.SetBold(0)
text_prop_1.SetItalic(0)
text_prop_1.SetShadow(0)
text_prop_1.SetJustification(0)
text_prop_1.SetBackgroundOpacity(1.0)
text_prop_1.SetVerticalJustification(1)
text_prop_1.SetUseTightBoundingBox(0)
text_prop_1.SetOrientation(0.0)
text_prop_1.SetLineSpacing(1.1)
text_prop_1.SetLineOffset(0.0)
tprops.AddItem(text_prop_1)

col_2 = [0.0, 0.0, 0.0]
lut.GetColor(126.0, col_2)
text_prop_2 = vtkTextProperty()
text_prop_2.SetColor(*col_2)
text_prop_2.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_2.SetFrame(0)
text_prop_2.SetFontSize(16)
text_prop_2.SetBold(0)
text_prop_2.SetItalic(0)
text_prop_2.SetShadow(0)
text_prop_2.SetJustification(0)
text_prop_2.SetBackgroundOpacity(1.0)
text_prop_2.SetVerticalJustification(1)
text_prop_2.SetUseTightBoundingBox(0)
text_prop_2.SetOrientation(0.0)
text_prop_2.SetLineSpacing(1.1)
text_prop_2.SetLineOffset(0.0)
tprops.AddItem(text_prop_2)

col_3 = [0.0, 0.0, 0.0]
lut.GetColor(148.0, col_3)
text_prop_3 = vtkTextProperty()
text_prop_3.SetColor(*col_3)
text_prop_3.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_3.SetFrame(0)
text_prop_3.SetFontSize(16)
text_prop_3.SetBold(0)
text_prop_3.SetItalic(0)
text_prop_3.SetShadow(0)
text_prop_3.SetJustification(0)
text_prop_3.SetBackgroundOpacity(1.0)
text_prop_3.SetVerticalJustification(1)
text_prop_3.SetUseTightBoundingBox(0)
text_prop_3.SetOrientation(0.0)
text_prop_3.SetLineSpacing(1.1)
text_prop_3.SetLineOffset(0.0)
tprops.AddItem(text_prop_3)

col_4 = [0.0, 0.0, 0.0]
lut.GetColor(169.0, col_4)
text_prop_4 = vtkTextProperty()
text_prop_4.SetColor(*col_4)
text_prop_4.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_4.SetFrame(0)
text_prop_4.SetFontSize(16)
text_prop_4.SetBold(0)
text_prop_4.SetItalic(0)
text_prop_4.SetShadow(0)
text_prop_4.SetJustification(0)
text_prop_4.SetBackgroundOpacity(1.0)
text_prop_4.SetVerticalJustification(1)
text_prop_4.SetUseTightBoundingBox(0)
text_prop_4.SetOrientation(0.0)
text_prop_4.SetLineSpacing(1.1)
text_prop_4.SetLineOffset(0.0)
tprops.AddItem(text_prop_4)

col_5 = [0.0, 0.0, 0.0]
lut.GetColor(191.0, col_5)
text_prop_5 = vtkTextProperty()
text_prop_5.SetColor(*col_5)
text_prop_5.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_5.SetFrame(0)
text_prop_5.SetFontSize(16)
text_prop_5.SetBold(0)
text_prop_5.SetItalic(0)
text_prop_5.SetShadow(0)
text_prop_5.SetJustification(0)
text_prop_5.SetBackgroundOpacity(1.0)
text_prop_5.SetVerticalJustification(1)
text_prop_5.SetUseTightBoundingBox(0)
text_prop_5.SetOrientation(0.0)
text_prop_5.SetLineSpacing(1.1)
text_prop_5.SetLineOffset(0.0)
tprops.AddItem(text_prop_5)

col_6 = [0.0, 0.0, 0.0]
lut.GetColor(212.0, col_6)
text_prop_6 = vtkTextProperty()
text_prop_6.SetColor(*col_6)
text_prop_6.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_6.SetFrame(0)
text_prop_6.SetFontSize(16)
text_prop_6.SetBold(0)
text_prop_6.SetItalic(0)
text_prop_6.SetShadow(0)
text_prop_6.SetJustification(0)
text_prop_6.SetBackgroundOpacity(1.0)
text_prop_6.SetVerticalJustification(1)
text_prop_6.SetUseTightBoundingBox(0)
text_prop_6.SetOrientation(0.0)
text_prop_6.SetLineSpacing(1.1)
text_prop_6.SetLineOffset(0.0)
tprops.AddItem(text_prop_6)

col_7 = [0.0, 0.0, 0.0]
lut.GetColor(233.0, col_7)
text_prop_7 = vtkTextProperty()
text_prop_7.SetColor(*col_7)
text_prop_7.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_7.SetFrame(0)
text_prop_7.SetFontSize(16)
text_prop_7.SetBold(0)
text_prop_7.SetItalic(0)
text_prop_7.SetShadow(0)
text_prop_7.SetJustification(0)
text_prop_7.SetBackgroundOpacity(1.0)
text_prop_7.SetVerticalJustification(1)
text_prop_7.SetUseTightBoundingBox(0)
text_prop_7.SetOrientation(0.0)
text_prop_7.SetLineSpacing(1.1)
text_prop_7.SetLineOffset(0.0)
tprops.AddItem(text_prop_7)

col_8 = [0.0, 0.0, 0.0]
lut.GetColor(255.0, col_8)
text_prop_8 = vtkTextProperty()
text_prop_8.SetColor(*col_8)
text_prop_8.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_8.SetFrame(0)
text_prop_8.SetFontSize(16)
text_prop_8.SetBold(0)
text_prop_8.SetItalic(0)
text_prop_8.SetShadow(0)
text_prop_8.SetJustification(0)
text_prop_8.SetBackgroundOpacity(1.0)
text_prop_8.SetVerticalJustification(1)
text_prop_8.SetUseTightBoundingBox(0)
text_prop_8.SetOrientation(0.0)
text_prop_8.SetLineSpacing(1.1)
text_prop_8.SetLineOffset(0.0)
tprops.AddItem(text_prop_8)

col_9 = [0.0, 0.0, 0.0]
lut.GetColor(276.0, col_9)
text_prop_9 = vtkTextProperty()
text_prop_9.SetColor(*col_9)
text_prop_9.SetBackgroundColor(1.0, 1.0, 1.0)
text_prop_9.SetFrame(0)
text_prop_9.SetFontSize(16)
text_prop_9.SetBold(0)
text_prop_9.SetItalic(0)
text_prop_9.SetShadow(0)
text_prop_9.SetJustification(0)
text_prop_9.SetBackgroundOpacity(1.0)
text_prop_9.SetVerticalJustification(1)
text_prop_9.SetUseTightBoundingBox(0)
text_prop_9.SetOrientation(0.0)
text_prop_9.SetLineSpacing(1.1)
text_prop_9.SetLineOffset(0.0)
tprops.AddItem(text_prop_9)

tprop_map = vtkDoubleArray()
tprop_map.SetNumberOfComponents(1)
tprop_map.InsertNextTypedTuple([84.0])
tprop_map.InsertNextTypedTuple([105.0])
tprop_map.InsertNextTypedTuple([126.0])
tprop_map.InsertNextTypedTuple([148.0])
tprop_map.InsertNextTypedTuple([169.0])
tprop_map.InsertNextTypedTuple([191.0])
tprop_map.InsertNextTypedTuple([212.0])
tprop_map.InsertNextTypedTuple([233.0])
tprop_map.InsertNextTypedTuple([255.0])
tprop_map.InsertNextTypedTuple([276.0])

mapped_colors = vtkUnsignedCharArray()
mapped_colors.SetNumberOfComponents(4)
for i in range(pd.GetNumberOfPoints()):
    mapped_colors.InsertNextTypedTuple([0, 0, 0, 255])

# Labeled contour item
item = vtkLabeledContourPolyDataItem()
item.SetPolyData(pd)
item.SetTextProperties(tprops)
item.SetTextPropertyMapping(tprop_map)
item.SetLabelVisibility(1)
item.SetSkipDistance(20.0)
item.SetScalarMode(VTK_SCALAR_MODE_USE_POINT_DATA)
item.SetMappedColors(mapped_colors)

width = 600
height = 600

# Interactive area
area = vtkInteractiveArea()

xmin = pd_bounds[0]
ymin = pd_bounds[2]
data_width = pd_bounds[1] - pd_bounds[0]
data_height = pd_bounds[3] - pd_bounds[2]
draw_area_bounds = vtkRectd(xmin, ymin, data_width, data_height)

vp = [0.0, 1.0, 0.0, 1.0]
screen_geometry = vtkRecti(
    int(vp[0] * width), int(vp[2] * height),
    int((vp[1] - vp[0]) * width), int((vp[3] - vp[2]) * height))

area.SetDrawAreaBounds(draw_area_bounds)
area.SetGeometry(screen_geometry)
area.SetFillViewport(False)
area.SetShowGrid(False)

for axis_pos in [vtkAxis.LEFT, vtkAxis.RIGHT, vtkAxis.BOTTOM, vtkAxis.TOP]:
    ax = area.GetAxis(axis_pos)
    ax.SetVisible(False)
    ax.SetMargins(0, 0)

# Context actor
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(area)

# Renderer
renderer = vtkRenderer()
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("context2d labeled contours")
render_window.SetMultiSamples(0)
render_window.SetSize(width, height)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# First render initializes area, then add labeled contour item
render_window.Render()
area.GetDrawAreaItem().AddItem(item)

interactor.Initialize()
interactor.Start()
