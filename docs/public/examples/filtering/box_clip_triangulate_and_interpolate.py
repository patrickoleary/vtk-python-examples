#!/usr/bin/env python

# Test vtkBoxClipDataSet triangulation and interpolation on hexahedra,
# quads, and lines with scalar data. A 6x2 grid of viewports shows
# axis-aligned and oriented box clips with and without clipped output.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    vtkCellArray,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Build hex ---
hex_pts = vtkPoints()
hex_pts.InsertNextPoint(-0.5, -0.5, -0.5)
hex_pts.InsertNextPoint(0.5, -0.5, -0.5)
hex_pts.InsertNextPoint(0.5, 0.5, -0.5)
hex_pts.InsertNextPoint(-0.5, 0.5, -0.5)
hex_pts.InsertNextPoint(-0.5, -0.5, 0.5)
hex_pts.InsertNextPoint(0.5, -0.5, 0.5)
hex_pts.InsertNextPoint(0.5, 0.5, 0.5)
hex_pts.InsertNextPoint(-0.5, 0.5, 0.5)

hex_cells = vtkCellArray()
hex_cells.InsertNextCell(8, [0, 1, 2, 3, 4, 5, 6, 7])

hex_data = vtkDoubleArray()
hex_data.SetName("data")
hex_data.SetNumberOfTuples(8)
for i, v in enumerate([0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0]):
    hex_data.SetValue(i, v)

hex_ug = vtkUnstructuredGrid()
hex_ug.SetPoints(hex_pts)
hex_ug.SetCells(VTK_HEXAHEDRON, hex_cells)
hex_ug.GetPointData().SetScalars(hex_data)

# --- Build quad ---
quad_pts = vtkPoints()
quad_pts.InsertNextPoint(-0.5, -0.5, 0.0)
quad_pts.InsertNextPoint(0.5, -0.5, 0.0)
quad_pts.InsertNextPoint(0.5, 0.5, 0.0)
quad_pts.InsertNextPoint(-0.5, 0.5, 0.0)

quad_cells = vtkCellArray()
quad_cells.InsertNextCell(4, [0, 1, 2, 3])

quad_data = vtkDoubleArray()
quad_data.SetName("data")
quad_data.SetNumberOfTuples(4)
for i, v in enumerate([0.0, 0.0, 1.0, 1.0]):
    quad_data.SetValue(i, v)

quad_pd = vtkPolyData()
quad_pd.SetPoints(quad_pts)
quad_pd.SetPolys(quad_cells)
quad_pd.GetPointData().SetScalars(quad_data)

# --- Build line ---
line_pts = vtkPoints()
line_pts.InsertNextPoint(0.0, -0.5, 0.0)
line_pts.InsertNextPoint(0.0, -0.25, 0.0)
line_pts.InsertNextPoint(0.0, 0.25, 0.0)
line_pts.InsertNextPoint(0.0, 0.25, 0.0)

line_cells = vtkCellArray()
line_cells.InsertNextCell(4, [0, 1, 2, 3])

line_data = vtkDoubleArray()
line_data.SetName("data")
line_data.SetNumberOfTuples(4)
for i, v in enumerate([0.0, 1.0, 1.0, 1.0]):
    line_data.SetValue(i, v)

line_pd = vtkPolyData()
line_pd.SetPoints(line_pts)
line_pd.SetLines(line_cells)
line_pd.GetPointData().SetScalars(line_data)

neg_x = [-1.0, 0.0, 0.0]
neg_y = [0.0, -1.0, 0.0]
neg_z = [0.0, 0.0, -1.0]
pos_x = [1.0, 0.0, 0.0]
pos_y = [0.0, 1.0, 0.0]
pos_z = [0.0, 0.0, 1.0]

# --- Col 0, Row 0: hex, axis-aligned, no clipped output ---
clip_0_0 = vtkBoxClipDataSet()
clip_0_0.SetInputData(hex_ug)
clip_0_0.SetBoxClip(0.0, 1.0, -1.0, 1.0, -1.0, 1.0)

surface_0_0 = vtkDataSetSurfaceFilter()
surface_0_0.SetInputConnection(clip_0_0.GetOutputPort(0))

mapper_0_0 = vtkPolyDataMapper()
mapper_0_0.SetInputConnection(surface_0_0.GetOutputPort())
mapper_0_0.InterpolateScalarsBeforeMappingOn()

actor_0_0 = vtkActor()
actor_0_0.SetMapper(mapper_0_0)

renderer_0_0 = vtkRenderer()
renderer_0_0.AddActor(actor_0_0)
renderer_0_0.SetViewport(0.0 / 6, 0.0 / 2, 1.0 / 6, 1.0 / 2)

# --- Col 0, Row 1: hex, axis-aligned, with clipped output ---
clip_0_1 = vtkBoxClipDataSet()
clip_0_1.SetInputData(hex_ug)
clip_0_1.GenerateClippedOutputOn()
clip_0_1.SetBoxClip(0.0, 1.0, -1.0, 1.0, -1.0, 1.0)

surface_0_1_in = vtkDataSetSurfaceFilter()
surface_0_1_in.SetInputConnection(clip_0_1.GetOutputPort(0))

mapper_0_1_in = vtkPolyDataMapper()
mapper_0_1_in.SetInputConnection(surface_0_1_in.GetOutputPort())
mapper_0_1_in.InterpolateScalarsBeforeMappingOn()

actor_0_1_in = vtkActor()
actor_0_1_in.SetMapper(mapper_0_1_in)

surface_0_1_out = vtkDataSetSurfaceFilter()
surface_0_1_out.SetInputConnection(clip_0_1.GetOutputPort(1))

mapper_0_1_out = vtkPolyDataMapper()
mapper_0_1_out.SetInputConnection(surface_0_1_out.GetOutputPort())

actor_0_1_out = vtkActor()
actor_0_1_out.SetMapper(mapper_0_1_out)

renderer_0_1 = vtkRenderer()
renderer_0_1.AddActor(actor_0_1_in)
renderer_0_1.AddActor(actor_0_1_out)
renderer_0_1.SetViewport(0.0 / 6, 1.0 / 2, 1.0 / 6, 2.0 / 2)

# --- Col 1, Row 0: hex, oriented, no clipped output ---
clip_1_0 = vtkBoxClipDataSet()
clip_1_0.SetInputData(hex_ug)
clip_1_0.SetBoxClip(neg_x, [0.0, -1.0, -1.0], neg_y, [0.0, -1.0, -1.0], neg_z, [0.0, -1.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_1_0 = vtkDataSetSurfaceFilter()
surface_1_0.SetInputConnection(clip_1_0.GetOutputPort(0))

mapper_1_0 = vtkPolyDataMapper()
mapper_1_0.SetInputConnection(surface_1_0.GetOutputPort())
mapper_1_0.InterpolateScalarsBeforeMappingOn()

actor_1_0 = vtkActor()
actor_1_0.SetMapper(mapper_1_0)

renderer_1_0 = vtkRenderer()
renderer_1_0.AddActor(actor_1_0)
renderer_1_0.SetViewport(1.0 / 6, 0.0 / 2, 2.0 / 6, 1.0 / 2)

# --- Col 1, Row 1: hex, oriented, with clipped output ---
clip_1_1 = vtkBoxClipDataSet()
clip_1_1.SetInputData(hex_ug)
clip_1_1.GenerateClippedOutputOn()
clip_1_1.SetBoxClip(neg_x, [0.0, -1.0, -1.0], neg_y, [0.0, -1.0, -1.0], neg_z, [0.0, -1.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_1_1_in = vtkDataSetSurfaceFilter()
surface_1_1_in.SetInputConnection(clip_1_1.GetOutputPort(0))

mapper_1_1_in = vtkPolyDataMapper()
mapper_1_1_in.SetInputConnection(surface_1_1_in.GetOutputPort())
mapper_1_1_in.InterpolateScalarsBeforeMappingOn()

actor_1_1_in = vtkActor()
actor_1_1_in.SetMapper(mapper_1_1_in)

surface_1_1_out = vtkDataSetSurfaceFilter()
surface_1_1_out.SetInputConnection(clip_1_1.GetOutputPort(1))

mapper_1_1_out = vtkPolyDataMapper()
mapper_1_1_out.SetInputConnection(surface_1_1_out.GetOutputPort())

actor_1_1_out = vtkActor()
actor_1_1_out.SetMapper(mapper_1_1_out)

renderer_1_1 = vtkRenderer()
renderer_1_1.AddActor(actor_1_1_in)
renderer_1_1.AddActor(actor_1_1_out)
renderer_1_1.SetViewport(1.0 / 6, 1.0 / 2, 2.0 / 6, 2.0 / 2)

# --- Col 2, Row 0: quad, axis-aligned, no clipped output ---
clip_2_0 = vtkBoxClipDataSet()
clip_2_0.SetInputData(quad_pd)
clip_2_0.SetBoxClip(0.0, 1.0, -1.0, 1.0, -1.0, 1.0)

surface_2_0 = vtkDataSetSurfaceFilter()
surface_2_0.SetInputConnection(clip_2_0.GetOutputPort(0))

mapper_2_0 = vtkPolyDataMapper()
mapper_2_0.SetInputConnection(surface_2_0.GetOutputPort())
mapper_2_0.InterpolateScalarsBeforeMappingOn()

actor_2_0 = vtkActor()
actor_2_0.SetMapper(mapper_2_0)

renderer_2_0 = vtkRenderer()
renderer_2_0.AddActor(actor_2_0)
renderer_2_0.SetViewport(2.0 / 6, 0.0 / 2, 3.0 / 6, 1.0 / 2)

# --- Col 2, Row 1: quad, axis-aligned, with clipped output ---
clip_2_1 = vtkBoxClipDataSet()
clip_2_1.SetInputData(quad_pd)
clip_2_1.GenerateClippedOutputOn()
clip_2_1.SetBoxClip(0.0, 1.0, -1.0, 1.0, -1.0, 1.0)

surface_2_1_in = vtkDataSetSurfaceFilter()
surface_2_1_in.SetInputConnection(clip_2_1.GetOutputPort(0))

mapper_2_1_in = vtkPolyDataMapper()
mapper_2_1_in.SetInputConnection(surface_2_1_in.GetOutputPort())
mapper_2_1_in.InterpolateScalarsBeforeMappingOn()

actor_2_1_in = vtkActor()
actor_2_1_in.SetMapper(mapper_2_1_in)

surface_2_1_out = vtkDataSetSurfaceFilter()
surface_2_1_out.SetInputConnection(clip_2_1.GetOutputPort(1))

mapper_2_1_out = vtkPolyDataMapper()
mapper_2_1_out.SetInputConnection(surface_2_1_out.GetOutputPort())

actor_2_1_out = vtkActor()
actor_2_1_out.SetMapper(mapper_2_1_out)

renderer_2_1 = vtkRenderer()
renderer_2_1.AddActor(actor_2_1_in)
renderer_2_1.AddActor(actor_2_1_out)
renderer_2_1.SetViewport(2.0 / 6, 1.0 / 2, 3.0 / 6, 2.0 / 2)

# --- Col 3, Row 0: quad, oriented, no clipped output ---
clip_3_0 = vtkBoxClipDataSet()
clip_3_0.SetInputData(quad_pd)
clip_3_0.SetBoxClip(neg_x, [0.0, -1.0, -1.0], neg_y, [0.0, -1.0, -1.0], neg_z, [0.0, -1.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_3_0 = vtkDataSetSurfaceFilter()
surface_3_0.SetInputConnection(clip_3_0.GetOutputPort(0))

mapper_3_0 = vtkPolyDataMapper()
mapper_3_0.SetInputConnection(surface_3_0.GetOutputPort())
mapper_3_0.InterpolateScalarsBeforeMappingOn()

actor_3_0 = vtkActor()
actor_3_0.SetMapper(mapper_3_0)

renderer_3_0 = vtkRenderer()
renderer_3_0.AddActor(actor_3_0)
renderer_3_0.SetViewport(3.0 / 6, 0.0 / 2, 4.0 / 6, 1.0 / 2)

# --- Col 3, Row 1: quad, oriented, with clipped output ---
clip_3_1 = vtkBoxClipDataSet()
clip_3_1.SetInputData(quad_pd)
clip_3_1.GenerateClippedOutputOn()
clip_3_1.SetBoxClip(neg_x, [0.0, -1.0, -1.0], neg_y, [0.0, -1.0, -1.0], neg_z, [0.0, -1.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_3_1_in = vtkDataSetSurfaceFilter()
surface_3_1_in.SetInputConnection(clip_3_1.GetOutputPort(0))

mapper_3_1_in = vtkPolyDataMapper()
mapper_3_1_in.SetInputConnection(surface_3_1_in.GetOutputPort())
mapper_3_1_in.InterpolateScalarsBeforeMappingOn()

actor_3_1_in = vtkActor()
actor_3_1_in.SetMapper(mapper_3_1_in)

surface_3_1_out = vtkDataSetSurfaceFilter()
surface_3_1_out.SetInputConnection(clip_3_1.GetOutputPort(1))

mapper_3_1_out = vtkPolyDataMapper()
mapper_3_1_out.SetInputConnection(surface_3_1_out.GetOutputPort())

actor_3_1_out = vtkActor()
actor_3_1_out.SetMapper(mapper_3_1_out)

renderer_3_1 = vtkRenderer()
renderer_3_1.AddActor(actor_3_1_in)
renderer_3_1.AddActor(actor_3_1_out)
renderer_3_1.SetViewport(3.0 / 6, 1.0 / 2, 4.0 / 6, 2.0 / 2)

# --- Col 4, Row 0: line, axis-aligned, no clipped output ---
clip_4_0 = vtkBoxClipDataSet()
clip_4_0.SetInputData(line_pd)
clip_4_0.SetBoxClip(-1.0, 1.0, 0.0, 1.0, -1.0, 1.0)

surface_4_0 = vtkDataSetSurfaceFilter()
surface_4_0.SetInputConnection(clip_4_0.GetOutputPort(0))

mapper_4_0 = vtkPolyDataMapper()
mapper_4_0.SetInputConnection(surface_4_0.GetOutputPort())
mapper_4_0.InterpolateScalarsBeforeMappingOn()

actor_4_0 = vtkActor()
actor_4_0.SetMapper(mapper_4_0)

renderer_4_0 = vtkRenderer()
renderer_4_0.AddActor(actor_4_0)
renderer_4_0.SetViewport(4.0 / 6, 0.0 / 2, 5.0 / 6, 1.0 / 2)

# --- Col 4, Row 1: line, axis-aligned, with clipped output ---
clip_4_1 = vtkBoxClipDataSet()
clip_4_1.SetInputData(line_pd)
clip_4_1.GenerateClippedOutputOn()
clip_4_1.SetBoxClip(-1.0, 1.0, 0.0, 1.0, -1.0, 1.0)

surface_4_1_in = vtkDataSetSurfaceFilter()
surface_4_1_in.SetInputConnection(clip_4_1.GetOutputPort(0))

mapper_4_1_in = vtkPolyDataMapper()
mapper_4_1_in.SetInputConnection(surface_4_1_in.GetOutputPort())
mapper_4_1_in.InterpolateScalarsBeforeMappingOn()

actor_4_1_in = vtkActor()
actor_4_1_in.SetMapper(mapper_4_1_in)

surface_4_1_out = vtkDataSetSurfaceFilter()
surface_4_1_out.SetInputConnection(clip_4_1.GetOutputPort(1))

mapper_4_1_out = vtkPolyDataMapper()
mapper_4_1_out.SetInputConnection(surface_4_1_out.GetOutputPort())

actor_4_1_out = vtkActor()
actor_4_1_out.SetMapper(mapper_4_1_out)

renderer_4_1 = vtkRenderer()
renderer_4_1.AddActor(actor_4_1_in)
renderer_4_1.AddActor(actor_4_1_out)
renderer_4_1.SetViewport(4.0 / 6, 1.0 / 2, 5.0 / 6, 2.0 / 2)

# --- Col 5, Row 0: line, oriented, no clipped output ---
clip_5_0 = vtkBoxClipDataSet()
clip_5_0.SetInputData(line_pd)
clip_5_0.SetBoxClip(neg_x, [-1.0, 0.0, -1.0], neg_y, [-1.0, 0.0, -1.0], neg_z, [-1.0, 0.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_5_0 = vtkDataSetSurfaceFilter()
surface_5_0.SetInputConnection(clip_5_0.GetOutputPort(0))

mapper_5_0 = vtkPolyDataMapper()
mapper_5_0.SetInputConnection(surface_5_0.GetOutputPort())
mapper_5_0.InterpolateScalarsBeforeMappingOn()

actor_5_0 = vtkActor()
actor_5_0.SetMapper(mapper_5_0)

renderer_5_0 = vtkRenderer()
renderer_5_0.AddActor(actor_5_0)
renderer_5_0.SetViewport(5.0 / 6, 0.0 / 2, 6.0 / 6, 1.0 / 2)

# --- Col 5, Row 1: line, oriented, with clipped output ---
clip_5_1 = vtkBoxClipDataSet()
clip_5_1.SetInputData(line_pd)
clip_5_1.GenerateClippedOutputOn()
clip_5_1.SetBoxClip(neg_x, [-1.0, 0.0, -1.0], neg_y, [-1.0, 0.0, -1.0], neg_z, [-1.0, 0.0, -1.0],
                     pos_x, [1.0, 1.0, 1.0], pos_y, [1.0, 1.0, 1.0], pos_z, [1.0, 1.0, 1.0])

surface_5_1_in = vtkDataSetSurfaceFilter()
surface_5_1_in.SetInputConnection(clip_5_1.GetOutputPort(0))

mapper_5_1_in = vtkPolyDataMapper()
mapper_5_1_in.SetInputConnection(surface_5_1_in.GetOutputPort())
mapper_5_1_in.InterpolateScalarsBeforeMappingOn()

actor_5_1_in = vtkActor()
actor_5_1_in.SetMapper(mapper_5_1_in)

surface_5_1_out = vtkDataSetSurfaceFilter()
surface_5_1_out.SetInputConnection(clip_5_1.GetOutputPort(1))

mapper_5_1_out = vtkPolyDataMapper()
mapper_5_1_out.SetInputConnection(surface_5_1_out.GetOutputPort())

actor_5_1_out = vtkActor()
actor_5_1_out.SetMapper(mapper_5_1_out)

renderer_5_1 = vtkRenderer()
renderer_5_1.AddActor(actor_5_1_in)
renderer_5_1.AddActor(actor_5_1_out)
renderer_5_1.SetViewport(5.0 / 6, 1.0 / 2, 6.0 / 6, 2.0 / 2)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0_0)
render_window.AddRenderer(renderer_0_1)
render_window.AddRenderer(renderer_1_0)
render_window.AddRenderer(renderer_1_1)
render_window.AddRenderer(renderer_2_0)
render_window.AddRenderer(renderer_2_1)
render_window.AddRenderer(renderer_3_0)
render_window.AddRenderer(renderer_3_1)
render_window.AddRenderer(renderer_4_0)
render_window.AddRenderer(renderer_4_1)
render_window.AddRenderer(renderer_5_0)
render_window.AddRenderer(renderer_5_1)
render_window.SetSize(600, 400)
render_window.SetWindowName("box clip triangulate and interpolate")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
