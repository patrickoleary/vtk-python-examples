#!/usr/bin/env python

# Demonstrate vtkBandedPolyDataContourFilter with 8 renderers showing
# combinations of cell orientation (CCW/CW), fill type (quad, triangles,
# strip), positive/negative scalars, and index/value scalar modes.
# Each case is shrunk for visibility.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Inputs: 8 polydata objects ---
# Each has 4 points at (0,0,0), (1,0,0), (1,1,0), (0,1,0)
# with vertices, lines, fill cells, and scalars.
# Cases 0-3: index mode; Cases 4-7: value mode.

# Case 0: index, CCW, quad, factor=100
points_0 = vtkPoints()
points_0.InsertNextPoint(0, 0, 0)
points_0.InsertNextPoint(1, 0, 0)
points_0.InsertNextPoint(1, 1, 0)
points_0.InsertNextPoint(0, 1, 0)

verts_0 = vtkCellArray()
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(0)
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(1)
verts_0.InsertNextCell(2)
verts_0.InsertCellPoint(2)
verts_0.InsertCellPoint(3)

lines_0 = vtkCellArray()
lines_0.InsertNextCell(2)
lines_0.InsertCellPoint(0)
lines_0.InsertCellPoint(1)
lines_0.InsertNextCell(2)
lines_0.InsertCellPoint(1)
lines_0.InsertCellPoint(2)
lines_0.InsertNextCell(3)
lines_0.InsertCellPoint(2)
lines_0.InsertCellPoint(3)
lines_0.InsertCellPoint(0)

polys_0 = vtkCellArray()
polys_0.InsertNextCell(4)
polys_0.InsertCellPoint(0)
polys_0.InsertCellPoint(1)
polys_0.InsertCellPoint(2)
polys_0.InsertCellPoint(3)

scalars_0 = vtkDoubleArray()
scalars_0.InsertNextValue(0.0)
scalars_0.InsertNextValue(50.0)
scalars_0.InsertNextValue(150.0)
scalars_0.InsertNextValue(100.0)

poly_data_0 = vtkPolyData()
poly_data_0.SetPoints(points_0)
poly_data_0.SetVerts(verts_0)
poly_data_0.SetLines(lines_0)
poly_data_0.SetPolys(polys_0)
poly_data_0.GetPointData().SetScalars(scalars_0)

# Case 1: index, CW, triangles, factor=100
points_1 = vtkPoints()
points_1.InsertNextPoint(0, 0, 0)
points_1.InsertNextPoint(1, 0, 0)
points_1.InsertNextPoint(1, 1, 0)
points_1.InsertNextPoint(0, 1, 0)

verts_1 = vtkCellArray()
verts_1.InsertNextCell(1)
verts_1.InsertCellPoint(0)
verts_1.InsertNextCell(1)
verts_1.InsertCellPoint(1)
verts_1.InsertNextCell(2)
verts_1.InsertCellPoint(3)
verts_1.InsertCellPoint(2)

lines_1 = vtkCellArray()
lines_1.InsertNextCell(2)
lines_1.InsertCellPoint(1)
lines_1.InsertCellPoint(0)
lines_1.InsertNextCell(2)
lines_1.InsertCellPoint(2)
lines_1.InsertCellPoint(1)
lines_1.InsertNextCell(3)
lines_1.InsertCellPoint(0)
lines_1.InsertCellPoint(3)
lines_1.InsertCellPoint(2)

strips_1 = vtkCellArray()
strips_1.InsertNextCell(3)
strips_1.InsertCellPoint(3)
strips_1.InsertCellPoint(1)
strips_1.InsertCellPoint(0)
strips_1.InsertNextCell(3)
strips_1.InsertCellPoint(2)
strips_1.InsertCellPoint(1)
strips_1.InsertCellPoint(3)

scalars_1 = vtkDoubleArray()
scalars_1.InsertNextValue(0.0)
scalars_1.InsertNextValue(50.0)
scalars_1.InsertNextValue(150.0)
scalars_1.InsertNextValue(100.0)

poly_data_1 = vtkPolyData()
poly_data_1.SetPoints(points_1)
poly_data_1.SetVerts(verts_1)
poly_data_1.SetLines(lines_1)
poly_data_1.SetStrips(strips_1)
poly_data_1.GetPointData().SetScalars(scalars_1)

# Case 2: index, CCW, quad, factor=-100
points_2 = vtkPoints()
points_2.InsertNextPoint(0, 0, 0)
points_2.InsertNextPoint(1, 0, 0)
points_2.InsertNextPoint(1, 1, 0)
points_2.InsertNextPoint(0, 1, 0)

verts_2 = vtkCellArray()
verts_2.InsertNextCell(1)
verts_2.InsertCellPoint(0)
verts_2.InsertNextCell(1)
verts_2.InsertCellPoint(1)
verts_2.InsertNextCell(2)
verts_2.InsertCellPoint(2)
verts_2.InsertCellPoint(3)

lines_2 = vtkCellArray()
lines_2.InsertNextCell(2)
lines_2.InsertCellPoint(0)
lines_2.InsertCellPoint(1)
lines_2.InsertNextCell(2)
lines_2.InsertCellPoint(1)
lines_2.InsertCellPoint(2)
lines_2.InsertNextCell(3)
lines_2.InsertCellPoint(2)
lines_2.InsertCellPoint(3)
lines_2.InsertCellPoint(0)

polys_2 = vtkCellArray()
polys_2.InsertNextCell(4)
polys_2.InsertCellPoint(0)
polys_2.InsertCellPoint(1)
polys_2.InsertCellPoint(2)
polys_2.InsertCellPoint(3)

scalars_2 = vtkDoubleArray()
scalars_2.InsertNextValue(0.0)
scalars_2.InsertNextValue(-50.0)
scalars_2.InsertNextValue(-150.0)
scalars_2.InsertNextValue(-100.0)

poly_data_2 = vtkPolyData()
poly_data_2.SetPoints(points_2)
poly_data_2.SetVerts(verts_2)
poly_data_2.SetLines(lines_2)
poly_data_2.SetPolys(polys_2)
poly_data_2.GetPointData().SetScalars(scalars_2)

# Case 3: index, CW, strip, factor=-100
points_3 = vtkPoints()
points_3.InsertNextPoint(0, 0, 0)
points_3.InsertNextPoint(1, 0, 0)
points_3.InsertNextPoint(1, 1, 0)
points_3.InsertNextPoint(0, 1, 0)

verts_3 = vtkCellArray()
verts_3.InsertNextCell(1)
verts_3.InsertCellPoint(0)
verts_3.InsertNextCell(1)
verts_3.InsertCellPoint(1)
verts_3.InsertNextCell(2)
verts_3.InsertCellPoint(3)
verts_3.InsertCellPoint(2)

lines_3 = vtkCellArray()
lines_3.InsertNextCell(2)
lines_3.InsertCellPoint(1)
lines_3.InsertCellPoint(0)
lines_3.InsertNextCell(2)
lines_3.InsertCellPoint(2)
lines_3.InsertCellPoint(1)
lines_3.InsertNextCell(3)
lines_3.InsertCellPoint(0)
lines_3.InsertCellPoint(3)
lines_3.InsertCellPoint(2)

strips_3 = vtkCellArray()
strips_3.InsertNextCell(4)
strips_3.InsertCellPoint(2)
strips_3.InsertCellPoint(3)
strips_3.InsertCellPoint(1)
strips_3.InsertCellPoint(0)

scalars_3 = vtkDoubleArray()
scalars_3.InsertNextValue(0.0)
scalars_3.InsertNextValue(-50.0)
scalars_3.InsertNextValue(-150.0)
scalars_3.InsertNextValue(-100.0)

poly_data_3 = vtkPolyData()
poly_data_3.SetPoints(points_3)
poly_data_3.SetVerts(verts_3)
poly_data_3.SetLines(lines_3)
poly_data_3.SetStrips(strips_3)
poly_data_3.GetPointData().SetScalars(scalars_3)

# Case 4: value, CCW, quad, factor=100
points_4 = vtkPoints()
points_4.InsertNextPoint(0, 0, 0)
points_4.InsertNextPoint(1, 0, 0)
points_4.InsertNextPoint(1, 1, 0)
points_4.InsertNextPoint(0, 1, 0)

verts_4 = vtkCellArray()
verts_4.InsertNextCell(1)
verts_4.InsertCellPoint(0)
verts_4.InsertNextCell(1)
verts_4.InsertCellPoint(1)
verts_4.InsertNextCell(2)
verts_4.InsertCellPoint(2)
verts_4.InsertCellPoint(3)

lines_4 = vtkCellArray()
lines_4.InsertNextCell(2)
lines_4.InsertCellPoint(0)
lines_4.InsertCellPoint(1)
lines_4.InsertNextCell(2)
lines_4.InsertCellPoint(1)
lines_4.InsertCellPoint(2)
lines_4.InsertNextCell(3)
lines_4.InsertCellPoint(2)
lines_4.InsertCellPoint(3)
lines_4.InsertCellPoint(0)

polys_4 = vtkCellArray()
polys_4.InsertNextCell(4)
polys_4.InsertCellPoint(0)
polys_4.InsertCellPoint(1)
polys_4.InsertCellPoint(2)
polys_4.InsertCellPoint(3)

scalars_4 = vtkDoubleArray()
scalars_4.InsertNextValue(0.0)
scalars_4.InsertNextValue(50.0)
scalars_4.InsertNextValue(150.0)
scalars_4.InsertNextValue(100.0)

poly_data_4 = vtkPolyData()
poly_data_4.SetPoints(points_4)
poly_data_4.SetVerts(verts_4)
poly_data_4.SetLines(lines_4)
poly_data_4.SetPolys(polys_4)
poly_data_4.GetPointData().SetScalars(scalars_4)

# Case 5: value, CW, triangles, factor=100
points_5 = vtkPoints()
points_5.InsertNextPoint(0, 0, 0)
points_5.InsertNextPoint(1, 0, 0)
points_5.InsertNextPoint(1, 1, 0)
points_5.InsertNextPoint(0, 1, 0)

verts_5 = vtkCellArray()
verts_5.InsertNextCell(1)
verts_5.InsertCellPoint(0)
verts_5.InsertNextCell(1)
verts_5.InsertCellPoint(1)
verts_5.InsertNextCell(2)
verts_5.InsertCellPoint(3)
verts_5.InsertCellPoint(2)

lines_5 = vtkCellArray()
lines_5.InsertNextCell(2)
lines_5.InsertCellPoint(1)
lines_5.InsertCellPoint(0)
lines_5.InsertNextCell(2)
lines_5.InsertCellPoint(2)
lines_5.InsertCellPoint(1)
lines_5.InsertNextCell(3)
lines_5.InsertCellPoint(0)
lines_5.InsertCellPoint(3)
lines_5.InsertCellPoint(2)

strips_5 = vtkCellArray()
strips_5.InsertNextCell(3)
strips_5.InsertCellPoint(3)
strips_5.InsertCellPoint(1)
strips_5.InsertCellPoint(0)
strips_5.InsertNextCell(3)
strips_5.InsertCellPoint(2)
strips_5.InsertCellPoint(1)
strips_5.InsertCellPoint(3)

scalars_5 = vtkDoubleArray()
scalars_5.InsertNextValue(0.0)
scalars_5.InsertNextValue(50.0)
scalars_5.InsertNextValue(150.0)
scalars_5.InsertNextValue(100.0)

poly_data_5 = vtkPolyData()
poly_data_5.SetPoints(points_5)
poly_data_5.SetVerts(verts_5)
poly_data_5.SetLines(lines_5)
poly_data_5.SetStrips(strips_5)
poly_data_5.GetPointData().SetScalars(scalars_5)

# Case 6: value, CCW, quad, factor=-100
points_6 = vtkPoints()
points_6.InsertNextPoint(0, 0, 0)
points_6.InsertNextPoint(1, 0, 0)
points_6.InsertNextPoint(1, 1, 0)
points_6.InsertNextPoint(0, 1, 0)

verts_6 = vtkCellArray()
verts_6.InsertNextCell(1)
verts_6.InsertCellPoint(0)
verts_6.InsertNextCell(1)
verts_6.InsertCellPoint(1)
verts_6.InsertNextCell(2)
verts_6.InsertCellPoint(2)
verts_6.InsertCellPoint(3)

lines_6 = vtkCellArray()
lines_6.InsertNextCell(2)
lines_6.InsertCellPoint(0)
lines_6.InsertCellPoint(1)
lines_6.InsertNextCell(2)
lines_6.InsertCellPoint(1)
lines_6.InsertCellPoint(2)
lines_6.InsertNextCell(3)
lines_6.InsertCellPoint(2)
lines_6.InsertCellPoint(3)
lines_6.InsertCellPoint(0)

polys_6 = vtkCellArray()
polys_6.InsertNextCell(4)
polys_6.InsertCellPoint(0)
polys_6.InsertCellPoint(1)
polys_6.InsertCellPoint(2)
polys_6.InsertCellPoint(3)

scalars_6 = vtkDoubleArray()
scalars_6.InsertNextValue(0.0)
scalars_6.InsertNextValue(-50.0)
scalars_6.InsertNextValue(-150.0)
scalars_6.InsertNextValue(-100.0)

poly_data_6 = vtkPolyData()
poly_data_6.SetPoints(points_6)
poly_data_6.SetVerts(verts_6)
poly_data_6.SetLines(lines_6)
poly_data_6.SetPolys(polys_6)
poly_data_6.GetPointData().SetScalars(scalars_6)

# Case 7: value, CW, strip, factor=-100
points_7 = vtkPoints()
points_7.InsertNextPoint(0, 0, 0)
points_7.InsertNextPoint(1, 0, 0)
points_7.InsertNextPoint(1, 1, 0)
points_7.InsertNextPoint(0, 1, 0)

verts_7 = vtkCellArray()
verts_7.InsertNextCell(1)
verts_7.InsertCellPoint(0)
verts_7.InsertNextCell(1)
verts_7.InsertCellPoint(1)
verts_7.InsertNextCell(2)
verts_7.InsertCellPoint(3)
verts_7.InsertCellPoint(2)

lines_7 = vtkCellArray()
lines_7.InsertNextCell(2)
lines_7.InsertCellPoint(1)
lines_7.InsertCellPoint(0)
lines_7.InsertNextCell(2)
lines_7.InsertCellPoint(2)
lines_7.InsertCellPoint(1)
lines_7.InsertNextCell(3)
lines_7.InsertCellPoint(0)
lines_7.InsertCellPoint(3)
lines_7.InsertCellPoint(2)

strips_7 = vtkCellArray()
strips_7.InsertNextCell(4)
strips_7.InsertCellPoint(2)
strips_7.InsertCellPoint(3)
strips_7.InsertCellPoint(1)
strips_7.InsertCellPoint(0)

scalars_7 = vtkDoubleArray()
scalars_7.InsertNextValue(0.0)
scalars_7.InsertNextValue(-50.0)
scalars_7.InsertNextValue(-150.0)
scalars_7.InsertNextValue(-100.0)

poly_data_7 = vtkPolyData()
poly_data_7.SetPoints(points_7)
poly_data_7.SetVerts(verts_7)
poly_data_7.SetLines(lines_7)
poly_data_7.SetStrips(strips_7)
poly_data_7.GetPointData().SetScalars(scalars_7)

# --- Filters ---
# Cases 0-3: index mode; Cases 4-7: value mode
value_range_0 = poly_data_0.GetPointData().GetScalars().GetRange()
banded_contour_0 = vtkBandedPolyDataContourFilter()
banded_contour_0.SetInputData(poly_data_0)
banded_contour_0.GenerateValues(5, value_range_0[0], value_range_0[1])
banded_contour_0.GenerateContourEdgesOff()
banded_contour_0.SetScalarModeToIndex()
banded_contour_0.Update()

shrink_0 = vtkShrinkFilter()
shrink_0.SetShrinkFactor(0.90)
shrink_0.SetInputConnection(banded_contour_0.GetOutputPort())

value_range_1 = poly_data_1.GetPointData().GetScalars().GetRange()
banded_contour_1 = vtkBandedPolyDataContourFilter()
banded_contour_1.SetInputData(poly_data_1)
banded_contour_1.GenerateValues(5, value_range_1[0], value_range_1[1])
banded_contour_1.GenerateContourEdgesOff()
banded_contour_1.SetScalarModeToIndex()
banded_contour_1.Update()

shrink_1 = vtkShrinkFilter()
shrink_1.SetShrinkFactor(0.90)
shrink_1.SetInputConnection(banded_contour_1.GetOutputPort())

value_range_2 = poly_data_2.GetPointData().GetScalars().GetRange()
banded_contour_2 = vtkBandedPolyDataContourFilter()
banded_contour_2.SetInputData(poly_data_2)
banded_contour_2.GenerateValues(5, value_range_2[0], value_range_2[1])
banded_contour_2.GenerateContourEdgesOff()
banded_contour_2.SetScalarModeToIndex()
banded_contour_2.Update()

shrink_2 = vtkShrinkFilter()
shrink_2.SetShrinkFactor(0.90)
shrink_2.SetInputConnection(banded_contour_2.GetOutputPort())

value_range_3 = poly_data_3.GetPointData().GetScalars().GetRange()
banded_contour_3 = vtkBandedPolyDataContourFilter()
banded_contour_3.SetInputData(poly_data_3)
banded_contour_3.GenerateValues(5, value_range_3[0], value_range_3[1])
banded_contour_3.GenerateContourEdgesOff()
banded_contour_3.SetScalarModeToIndex()
banded_contour_3.Update()

shrink_3 = vtkShrinkFilter()
shrink_3.SetShrinkFactor(0.90)
shrink_3.SetInputConnection(banded_contour_3.GetOutputPort())

value_range_4 = poly_data_4.GetPointData().GetScalars().GetRange()
banded_contour_4 = vtkBandedPolyDataContourFilter()
banded_contour_4.SetInputData(poly_data_4)
banded_contour_4.GenerateValues(5, value_range_4[0], value_range_4[1])
banded_contour_4.GenerateContourEdgesOff()
banded_contour_4.SetScalarModeToValue()
banded_contour_4.Update()

shrink_4 = vtkShrinkFilter()
shrink_4.SetShrinkFactor(0.90)
shrink_4.SetInputConnection(banded_contour_4.GetOutputPort())

value_range_5 = poly_data_5.GetPointData().GetScalars().GetRange()
banded_contour_5 = vtkBandedPolyDataContourFilter()
banded_contour_5.SetInputData(poly_data_5)
banded_contour_5.GenerateValues(5, value_range_5[0], value_range_5[1])
banded_contour_5.GenerateContourEdgesOff()
banded_contour_5.SetScalarModeToValue()
banded_contour_5.Update()

shrink_5 = vtkShrinkFilter()
shrink_5.SetShrinkFactor(0.90)
shrink_5.SetInputConnection(banded_contour_5.GetOutputPort())

value_range_6 = poly_data_6.GetPointData().GetScalars().GetRange()
banded_contour_6 = vtkBandedPolyDataContourFilter()
banded_contour_6.SetInputData(poly_data_6)
banded_contour_6.GenerateValues(5, value_range_6[0], value_range_6[1])
banded_contour_6.GenerateContourEdgesOff()
banded_contour_6.SetScalarModeToValue()
banded_contour_6.Update()

shrink_6 = vtkShrinkFilter()
shrink_6.SetShrinkFactor(0.90)
shrink_6.SetInputConnection(banded_contour_6.GetOutputPort())

value_range_7 = poly_data_7.GetPointData().GetScalars().GetRange()
banded_contour_7 = vtkBandedPolyDataContourFilter()
banded_contour_7.SetInputData(poly_data_7)
banded_contour_7.GenerateValues(5, value_range_7[0], value_range_7[1])
banded_contour_7.GenerateContourEdgesOff()
banded_contour_7.SetScalarModeToValue()
banded_contour_7.Update()

shrink_7 = vtkShrinkFilter()
shrink_7.SetShrinkFactor(0.90)
shrink_7.SetInputConnection(banded_contour_7.GetOutputPort())

# --- Mappers ---
mapper_0 = vtkDataSetMapper()
mapper_0.SetInputConnection(shrink_0.GetOutputPort())
mapper_0.SetScalarModeToUseCellData()
mapper_0.SetScalarRange(banded_contour_0.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(shrink_1.GetOutputPort())
mapper_1.SetScalarModeToUseCellData()
mapper_1.SetScalarRange(banded_contour_1.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(shrink_2.GetOutputPort())
mapper_2.SetScalarModeToUseCellData()
mapper_2.SetScalarRange(banded_contour_2.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(shrink_3.GetOutputPort())
mapper_3.SetScalarModeToUseCellData()
mapper_3.SetScalarRange(banded_contour_3.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_4 = vtkDataSetMapper()
mapper_4.SetInputConnection(shrink_4.GetOutputPort())
mapper_4.SetScalarModeToUseCellData()
mapper_4.SetScalarRange(banded_contour_4.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_5 = vtkDataSetMapper()
mapper_5.SetInputConnection(shrink_5.GetOutputPort())
mapper_5.SetScalarModeToUseCellData()
mapper_5.SetScalarRange(banded_contour_5.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_6 = vtkDataSetMapper()
mapper_6.SetInputConnection(shrink_6.GetOutputPort())
mapper_6.SetScalarModeToUseCellData()
mapper_6.SetScalarRange(banded_contour_6.GetOutput().GetCellData().GetArray("Scalars").GetRange())

mapper_7 = vtkDataSetMapper()
mapper_7.SetInputConnection(shrink_7.GetOutputPort())
mapper_7.SetScalarModeToUseCellData()
mapper_7.SetScalarRange(banded_contour_7.GetOutput().GetCellData().GetArray("Scalars").GetRange())

# --- Actors ---
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)

actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)

actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)

# --- Renderers ---
# Viewports: index cases at x=[0..0.5], value cases at x=[0.5..1.0]
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.5, 0.25, 1.0)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.0, 0.0, 0.25, 0.5)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.25, 0.5, 0.5, 1.0)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.25, 0.0, 0.5, 0.5)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(0.5, 0.5, 0.75, 1.0)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(0.5, 0.0, 0.75, 0.5)

renderer_6 = vtkRenderer()
renderer_6.AddViewProp(actor_6)
renderer_6.SetViewport(0.75, 0.5, 1.0, 1.0)

renderer_7 = vtkRenderer()
renderer_7.AddViewProp(actor_7)
renderer_7.SetViewport(0.75, 0.0, 1.0, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetSize(400, 200)
render_window.SetWindowName("banded contour orientations")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
