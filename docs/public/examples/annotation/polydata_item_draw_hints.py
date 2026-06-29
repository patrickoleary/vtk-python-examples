#!/usr/bin/env python

# Demonstrate vtkPolyDataItem with draw hints (line width, stipple patterns).

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_POLY_LINE,
    vtkPolyData,
    vtkRectd,
    vtkRecti,
)
from vtkmodules.vtkChartsCore import (
    vtkAxis,
    vtkInteractiveArea,
)
from vtkmodules.vtkRenderingCore import (
    VTK_SCALAR_MODE_USE_CELL_DATA,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkPen, vtkPolyDataItem


# Spiral 1 — bottom-left, red, dash-dot-dot, width 3.5
# vp [0.0, 0.5, 0.0, 0.5]: affine maps [0..1] to [0..0.5] x [0..0.5]
spiral_1_pd = vtkPolyData()
spiral_1_pd.Allocate(50)
spiral_1_pts = vtkPoints()
spiral_1_pts.InsertNextPoint(0.05, 0.05, 0.0)
spiral_1_pts.InsertNextPoint(0.05, 0.45, 0.0)
spiral_1_pts.InsertNextPoint(0.45, 0.45, 0.0)
spiral_1_pts.InsertNextPoint(0.45, 0.10, 0.0)
spiral_1_pts.InsertNextPoint(0.10, 0.10, 0.0)
spiral_1_pts.InsertNextPoint(0.10, 0.40, 0.0)
spiral_1_pts.InsertNextPoint(0.40, 0.40, 0.0)
spiral_1_pts.InsertNextPoint(0.40, 0.15, 0.0)
spiral_1_pts.InsertNextPoint(0.15, 0.15, 0.0)
spiral_1_pts.InsertNextPoint(0.15, 0.35, 0.0)
spiral_1_pts.InsertNextPoint(0.35, 0.35, 0.0)
spiral_1_pts.InsertNextPoint(0.35, 0.20, 0.0)
spiral_1_pts.InsertNextPoint(0.20, 0.20, 0.0)
spiral_1_pts.InsertNextPoint(0.20, 0.30, 0.0)
spiral_1_pts.InsertNextPoint(0.30, 0.30, 0.0)
spiral_1_pts.InsertNextPoint(0.30, 0.25, 0.0)
spiral_1_pd.SetPoints(spiral_1_pts)
spiral_1_pd.InsertNextCell(VTK_POLY_LINE, 16, list(range(16)))

spiral_1_colors = vtkUnsignedCharArray()
spiral_1_colors.SetNumberOfComponents(4)
spiral_1_colors.SetNumberOfTuples(1)
spiral_1_colors.SetTuple4(0, 255, 0, 0, 255)

spiral_1_lw = vtkFloatArray()
spiral_1_lw.SetNumberOfComponents(1)
spiral_1_lw.SetName("LineWidth")
spiral_1_lw.InsertNextValue(3.5)
spiral_1_pd.GetFieldData().AddArray(spiral_1_lw)

spiral_1_st = vtkIntArray()
spiral_1_st.SetNumberOfComponents(1)
spiral_1_st.SetName("StippleType")
spiral_1_st.InsertNextValue(vtkPen.DASH_DOT_DOT_LINE)
spiral_1_pd.GetFieldData().AddArray(spiral_1_st)

spiral_1_item = vtkPolyDataItem()
spiral_1_item.SetPolyData(spiral_1_pd)
spiral_1_item.SetMappedColors(spiral_1_colors)
spiral_1_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
spiral_1_item.SetVisible(True)

# Spiral 2 — top-left, green, dash, width 2.5
# vp [0.0, 0.5, 0.5, 1.0]: affine maps [0..1] to [0..0.5] x [0.5..1.0]
spiral_2_pd = vtkPolyData()
spiral_2_pd.Allocate(50)
spiral_2_pts = vtkPoints()
spiral_2_pts.InsertNextPoint(0.05, 0.55, 0.0)
spiral_2_pts.InsertNextPoint(0.05, 0.95, 0.0)
spiral_2_pts.InsertNextPoint(0.45, 0.95, 0.0)
spiral_2_pts.InsertNextPoint(0.45, 0.60, 0.0)
spiral_2_pts.InsertNextPoint(0.10, 0.60, 0.0)
spiral_2_pts.InsertNextPoint(0.10, 0.90, 0.0)
spiral_2_pts.InsertNextPoint(0.40, 0.90, 0.0)
spiral_2_pts.InsertNextPoint(0.40, 0.65, 0.0)
spiral_2_pts.InsertNextPoint(0.15, 0.65, 0.0)
spiral_2_pts.InsertNextPoint(0.15, 0.85, 0.0)
spiral_2_pts.InsertNextPoint(0.35, 0.85, 0.0)
spiral_2_pts.InsertNextPoint(0.35, 0.70, 0.0)
spiral_2_pts.InsertNextPoint(0.20, 0.70, 0.0)
spiral_2_pts.InsertNextPoint(0.20, 0.80, 0.0)
spiral_2_pts.InsertNextPoint(0.30, 0.80, 0.0)
spiral_2_pts.InsertNextPoint(0.30, 0.75, 0.0)
spiral_2_pd.SetPoints(spiral_2_pts)
spiral_2_pd.InsertNextCell(VTK_POLY_LINE, 16, list(range(16)))

spiral_2_colors = vtkUnsignedCharArray()
spiral_2_colors.SetNumberOfComponents(4)
spiral_2_colors.SetNumberOfTuples(1)
spiral_2_colors.SetTuple4(0, 0, 255, 0, 255)

spiral_2_lw = vtkFloatArray()
spiral_2_lw.SetNumberOfComponents(1)
spiral_2_lw.SetName("LineWidth")
spiral_2_lw.InsertNextValue(2.5)
spiral_2_pd.GetFieldData().AddArray(spiral_2_lw)

spiral_2_st = vtkIntArray()
spiral_2_st.SetNumberOfComponents(1)
spiral_2_st.SetName("StippleType")
spiral_2_st.InsertNextValue(vtkPen.DASH_LINE)
spiral_2_pd.GetFieldData().AddArray(spiral_2_st)

spiral_2_item = vtkPolyDataItem()
spiral_2_item.SetPolyData(spiral_2_pd)
spiral_2_item.SetMappedColors(spiral_2_colors)
spiral_2_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
spiral_2_item.SetVisible(True)

# Spiral 3 — top-right, blue, dash-dot, width 1.5
# vp [0.5, 1.0, 0.5, 1.0]: affine maps [0..1] to [0.5..1.0] x [0.5..1.0]
spiral_3_pd = vtkPolyData()
spiral_3_pd.Allocate(50)
spiral_3_pts = vtkPoints()
spiral_3_pts.InsertNextPoint(0.55, 0.55, 0.0)
spiral_3_pts.InsertNextPoint(0.55, 0.95, 0.0)
spiral_3_pts.InsertNextPoint(0.95, 0.95, 0.0)
spiral_3_pts.InsertNextPoint(0.95, 0.60, 0.0)
spiral_3_pts.InsertNextPoint(0.60, 0.60, 0.0)
spiral_3_pts.InsertNextPoint(0.60, 0.90, 0.0)
spiral_3_pts.InsertNextPoint(0.90, 0.90, 0.0)
spiral_3_pts.InsertNextPoint(0.90, 0.65, 0.0)
spiral_3_pts.InsertNextPoint(0.65, 0.65, 0.0)
spiral_3_pts.InsertNextPoint(0.65, 0.85, 0.0)
spiral_3_pts.InsertNextPoint(0.85, 0.85, 0.0)
spiral_3_pts.InsertNextPoint(0.85, 0.70, 0.0)
spiral_3_pts.InsertNextPoint(0.70, 0.70, 0.0)
spiral_3_pts.InsertNextPoint(0.70, 0.80, 0.0)
spiral_3_pts.InsertNextPoint(0.80, 0.80, 0.0)
spiral_3_pts.InsertNextPoint(0.80, 0.75, 0.0)
spiral_3_pd.SetPoints(spiral_3_pts)
spiral_3_pd.InsertNextCell(VTK_POLY_LINE, 16, list(range(16)))

spiral_3_colors = vtkUnsignedCharArray()
spiral_3_colors.SetNumberOfComponents(4)
spiral_3_colors.SetNumberOfTuples(1)
spiral_3_colors.SetTuple4(0, 0, 0, 255, 255)

spiral_3_lw = vtkFloatArray()
spiral_3_lw.SetNumberOfComponents(1)
spiral_3_lw.SetName("LineWidth")
spiral_3_lw.InsertNextValue(1.5)
spiral_3_pd.GetFieldData().AddArray(spiral_3_lw)

spiral_3_st = vtkIntArray()
spiral_3_st.SetNumberOfComponents(1)
spiral_3_st.SetName("StippleType")
spiral_3_st.InsertNextValue(vtkPen.DASH_DOT_LINE)
spiral_3_pd.GetFieldData().AddArray(spiral_3_st)

spiral_3_item = vtkPolyDataItem()
spiral_3_item.SetPolyData(spiral_3_pd)
spiral_3_item.SetMappedColors(spiral_3_colors)
spiral_3_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
spiral_3_item.SetVisible(True)

# Spiral 4 — bottom-right, magenta, solid, width 0.5
# vp [0.5, 1.0, 0.0, 0.5]: affine maps [0..1] to [0.5..1.0] x [0..0.5]
spiral_4_pd = vtkPolyData()
spiral_4_pd.Allocate(50)
spiral_4_pts = vtkPoints()
spiral_4_pts.InsertNextPoint(0.55, 0.05, 0.0)
spiral_4_pts.InsertNextPoint(0.55, 0.45, 0.0)
spiral_4_pts.InsertNextPoint(0.95, 0.45, 0.0)
spiral_4_pts.InsertNextPoint(0.95, 0.10, 0.0)
spiral_4_pts.InsertNextPoint(0.60, 0.10, 0.0)
spiral_4_pts.InsertNextPoint(0.60, 0.40, 0.0)
spiral_4_pts.InsertNextPoint(0.90, 0.40, 0.0)
spiral_4_pts.InsertNextPoint(0.90, 0.15, 0.0)
spiral_4_pts.InsertNextPoint(0.65, 0.15, 0.0)
spiral_4_pts.InsertNextPoint(0.65, 0.35, 0.0)
spiral_4_pts.InsertNextPoint(0.85, 0.35, 0.0)
spiral_4_pts.InsertNextPoint(0.85, 0.20, 0.0)
spiral_4_pts.InsertNextPoint(0.70, 0.20, 0.0)
spiral_4_pts.InsertNextPoint(0.70, 0.30, 0.0)
spiral_4_pts.InsertNextPoint(0.80, 0.30, 0.0)
spiral_4_pts.InsertNextPoint(0.80, 0.25, 0.0)
spiral_4_pd.SetPoints(spiral_4_pts)
spiral_4_pd.InsertNextCell(VTK_POLY_LINE, 16, list(range(16)))

spiral_4_colors = vtkUnsignedCharArray()
spiral_4_colors.SetNumberOfComponents(4)
spiral_4_colors.SetNumberOfTuples(1)
spiral_4_colors.SetTuple4(0, 255, 0, 255, 255)

spiral_4_lw = vtkFloatArray()
spiral_4_lw.SetNumberOfComponents(1)
spiral_4_lw.SetName("LineWidth")
spiral_4_lw.InsertNextValue(0.5)
spiral_4_pd.GetFieldData().AddArray(spiral_4_lw)

spiral_4_st = vtkIntArray()
spiral_4_st.SetNumberOfComponents(1)
spiral_4_st.SetName("StippleType")
spiral_4_st.InsertNextValue(vtkPen.SOLID_LINE)
spiral_4_pd.GetFieldData().AddArray(spiral_4_st)

spiral_4_item = vtkPolyDataItem()
spiral_4_item.SetPolyData(spiral_4_pd)
spiral_4_item.SetMappedColors(spiral_4_colors)
spiral_4_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
spiral_4_item.SetVisible(True)

width = 400
height = 400

# Interactive area
area = vtkInteractiveArea()
draw_area_bounds = vtkRectd(0.0, 0.0, 1.0, 1.0)
screen_geometry = vtkRecti(0, 0, width, height)

area.GetDrawAreaItem().AddItem(spiral_1_item)
area.GetDrawAreaItem().AddItem(spiral_2_item)
area.GetDrawAreaItem().AddItem(spiral_3_item)
area.GetDrawAreaItem().AddItem(spiral_4_item)

area.SetDrawAreaBounds(draw_area_bounds)
area.SetGeometry(screen_geometry)
area.SetFillViewport(False)
area.SetShowGrid(False)

area.GetAxis(vtkAxis.LEFT).SetVisible(False)
area.GetAxis(vtkAxis.LEFT).SetMargins(0, 0)
area.GetAxis(vtkAxis.RIGHT).SetVisible(False)
area.GetAxis(vtkAxis.RIGHT).SetMargins(0, 0)
area.GetAxis(vtkAxis.BOTTOM).SetVisible(False)
area.GetAxis(vtkAxis.BOTTOM).SetMargins(0, 0)
area.GetAxis(vtkAxis.TOP).SetVisible(False)
area.GetAxis(vtkAxis.TOP).SetMargins(0, 0)

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polydata item draw hints")
render_window.SetMultiSamples(0)
render_window.SetSize(width, height)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
context_actor = vtkContextActor()
context_actor.GetScene().SetRenderer(renderer)
context_actor.GetScene().AddItem(area)
renderer.AddActor(context_actor)

interactor.Initialize()
interactor.Start()
