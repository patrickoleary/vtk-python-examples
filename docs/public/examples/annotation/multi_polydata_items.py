#!/usr/bin/env python

# Display multiple polydata items in a 2D context using vtkPolyDataItem.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_POLY_LINE,
    VTK_TRIANGLE,
    vtkCellArray,
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
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkPolyDataItem

# Line polydata
line_pd = vtkPolyData()
line_pts = vtkPoints()
line_pts.InsertNextPoint(0.5, 0.5, 0.0)
line_pts.InsertNextPoint(0.0, 1.0, 0.0)
line_pd.SetPoints(line_pts)
line_cells = vtkCellArray()
line_cells.InsertNextCell(2)
line_cells.InsertCellPoint(0)
line_cells.InsertCellPoint(1)
line_pd.SetLines(line_cells)

line_colors = vtkUnsignedCharArray()
line_colors.SetNumberOfComponents(4)
line_colors.SetNumberOfTuples(1)
line_colors.SetTuple4(0, 255, 0, 0, 255)

line_item = vtkPolyDataItem()
line_item.SetPolyData(line_pd)
line_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
line_item.SetMappedColors(line_colors)
line_item.SetVisible(True)

# Triangle polydata
tri_pd = vtkPolyData()
tri_pts = vtkPoints()
tri_pts.InsertNextPoint(0.5, 0.0, 0.0)
tri_pts.InsertNextPoint(0.75, 0.5, 0.0)
tri_pts.InsertNextPoint(1.0, 0.0, 0.0)
tri_pd.SetPoints(tri_pts)
tri_cells = vtkCellArray()
tri_cells.InsertNextCell(3)
tri_cells.InsertCellPoint(0)
tri_cells.InsertCellPoint(1)
tri_cells.InsertCellPoint(2)
tri_pd.SetPolys(tri_cells)

tri_colors = vtkUnsignedCharArray()
tri_colors.SetNumberOfComponents(4)
tri_colors.SetNumberOfTuples(1)
tri_colors.SetTuple4(0, 0, 255, 0, 255)

tri_item = vtkPolyDataItem()
tri_item.SetPolyData(tri_pd)
tri_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
tri_item.SetMappedColors(tri_colors)
tri_item.SetVisible(True)

# Line strip (spiral) polydata
spiral_pd = vtkPolyData()
spiral_pts = vtkPoints()
spiral_pts.InsertNextPoint(0.1, 0.1, 0.0)
spiral_pts.InsertNextPoint(0.1, 0.4, 0.0)
spiral_pts.InsertNextPoint(0.4, 0.4, 0.0)
spiral_pts.InsertNextPoint(0.4, 0.2, 0.0)
spiral_pts.InsertNextPoint(0.2, 0.2, 0.0)
spiral_pts.InsertNextPoint(0.2, 0.3, 0.0)
spiral_pts.InsertNextPoint(0.3, 0.3, 0.0)
spiral_pd.SetPoints(spiral_pts)
spiral_cells = vtkCellArray()
spiral_cells.InsertNextCell(7)
spiral_cells.InsertCellPoint(0)
spiral_cells.InsertCellPoint(1)
spiral_cells.InsertCellPoint(2)
spiral_cells.InsertCellPoint(3)
spiral_cells.InsertCellPoint(4)
spiral_cells.InsertCellPoint(5)
spiral_cells.InsertCellPoint(6)
spiral_pd.SetLines(spiral_cells)

spiral_colors = vtkUnsignedCharArray()
spiral_colors.SetNumberOfComponents(4)
spiral_colors.SetNumberOfTuples(1)
spiral_colors.SetTuple4(0, 0, 0, 255, 255)

spiral_item = vtkPolyDataItem()
spiral_item.SetPolyData(spiral_pd)
spiral_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
spiral_item.SetMappedColors(spiral_colors)
spiral_item.SetVisible(True)

# Mixed polydata
mixed_pd = vtkPolyData()
mixed_pd.Allocate(50)
mixed_pts = vtkPoints()
mixed_pts.InsertNextPoint(0.6, 0.6, 0.0)
mixed_pts.InsertNextPoint(0.75, 0.6, 0.0)
mixed_pts.InsertNextPoint(0.9, 0.6, 0.0)
mixed_pts.InsertNextPoint(0.6, 0.75, 0.0)
mixed_pts.InsertNextPoint(0.75, 0.75, 0.0)
mixed_pts.InsertNextPoint(0.9, 0.75, 0.0)
mixed_pts.InsertNextPoint(0.6, 0.9, 0.0)
mixed_pts.InsertNextPoint(0.75, 0.9, 0.0)
mixed_pts.InsertNextPoint(0.9, 0.9, 0.0)
mixed_pd.SetPoints(mixed_pts)
mixed_pd.InsertNextCell(VTK_POLY_LINE, 3, [3, 6, 7])
mixed_pd.InsertNextCell(VTK_POLY_LINE, 2, [8, 5])
mixed_pd.InsertNextCell(VTK_TRIANGLE, 3, [5, 2, 1])
mixed_pd.InsertNextCell(VTK_POLY_LINE, 3, [1, 4, 5])
mixed_pd.InsertNextCell(VTK_TRIANGLE, 3, [0, 3, 4])

mixed_colors = vtkUnsignedCharArray()
mixed_colors.SetNumberOfComponents(4)
mixed_colors.SetNumberOfTuples(5)
mixed_colors.SetTuple4(0, 255, 0, 0, 255)
mixed_colors.SetTuple4(1, 0, 255, 0, 255)
mixed_colors.SetTuple4(2, 0, 0, 255, 255)
mixed_colors.SetTuple4(3, 255, 255, 0, 255)
mixed_colors.SetTuple4(4, 0, 255, 255, 255)

mixed_item = vtkPolyDataItem()
mixed_item.SetPolyData(mixed_pd)
mixed_item.SetScalarMode(VTK_SCALAR_MODE_USE_CELL_DATA)
mixed_item.SetMappedColors(mixed_colors)
mixed_item.SetVisible(True)

width = 400
height = 400

# Interactive area
area = vtkInteractiveArea()
draw_area_bounds = vtkRectd(0.0, 0.0, 1.0, 1.0)

vp = [0.0500000007451, 0.949999988079, 0.259999990463, 0.860000014305]
screen_geometry = vtkRecti(
    int(vp[0] * width), int(vp[2] * height),
    int((vp[1] - vp[0]) * width), int((vp[3] - vp[2]) * height))

area.GetDrawAreaItem().AddItem(line_item)
area.GetDrawAreaItem().AddItem(tri_item)
area.GetDrawAreaItem().AddItem(spiral_item)
area.GetDrawAreaItem().AddItem(mixed_item)

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
render_window.SetWindowName("multi polydata items")
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
