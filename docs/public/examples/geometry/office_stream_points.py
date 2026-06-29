#!/usr/bin/env python

# Demonstrate vtkStructuredGridGeometryFilter extracting office
# geometry (tables, filing cabinets, bookshelves, window, inlet,
# outlet) and vtkStreamTracer with cone glyphs for airflow.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOLegacy import vtkStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Read office data
reader = vtkStructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "office.binary.vtk"))
reader.Update()

length = reader.GetOutput().GetLength()
max_velocity = reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
max_time = 35.0 * length / max_velocity

# Table 1
table_1 = vtkStructuredGridGeometryFilter()
table_1.SetInputConnection(reader.GetOutputPort())
table_1.SetExtent(11, 15, 7, 9, 8, 8)
map_table_1 = vtkPolyDataMapper()
map_table_1.SetInputConnection(table_1.GetOutputPort())
map_table_1.ScalarVisibilityOff()
table_1_actor = vtkActor()
table_1_actor.SetMapper(map_table_1)
table_1_actor.GetProperty().SetColor(0.59, 0.427, 0.392)

# Table 2
table_2 = vtkStructuredGridGeometryFilter()
table_2.SetInputConnection(reader.GetOutputPort())
table_2.SetExtent(11, 15, 10, 12, 8, 8)
map_table_2 = vtkPolyDataMapper()
map_table_2.SetInputConnection(table_2.GetOutputPort())
map_table_2.ScalarVisibilityOff()
table_2_actor = vtkActor()
table_2_actor.SetMapper(map_table_2)
table_2_actor.GetProperty().SetColor(0.59, 0.427, 0.392)

# Filing cabinet 1
filing_cabinet_1 = vtkStructuredGridGeometryFilter()
filing_cabinet_1.SetInputConnection(reader.GetOutputPort())
filing_cabinet_1.SetExtent(15, 15, 7, 9, 0, 8)
map_filing_cabinet_1 = vtkPolyDataMapper()
map_filing_cabinet_1.SetInputConnection(filing_cabinet_1.GetOutputPort())
map_filing_cabinet_1.ScalarVisibilityOff()
filing_cabinet_1_actor = vtkActor()
filing_cabinet_1_actor.SetMapper(map_filing_cabinet_1)
filing_cabinet_1_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

# Filing cabinet 2
filing_cabinet_2 = vtkStructuredGridGeometryFilter()
filing_cabinet_2.SetInputConnection(reader.GetOutputPort())
filing_cabinet_2.SetExtent(15, 15, 10, 12, 0, 8)
map_filing_cabinet_2 = vtkPolyDataMapper()
map_filing_cabinet_2.SetInputConnection(filing_cabinet_2.GetOutputPort())
map_filing_cabinet_2.ScalarVisibilityOff()
filing_cabinet_2_actor = vtkActor()
filing_cabinet_2_actor.SetMapper(map_filing_cabinet_2)
filing_cabinet_2_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

# Bookshelf 1
bookshelf_1_top = vtkStructuredGridGeometryFilter()
bookshelf_1_top.SetInputConnection(reader.GetOutputPort())
bookshelf_1_top.SetExtent(13, 13, 0, 4, 0, 11)
map_bookshelf_1_top = vtkPolyDataMapper()
map_bookshelf_1_top.SetInputConnection(bookshelf_1_top.GetOutputPort())
map_bookshelf_1_top.ScalarVisibilityOff()
bookshelf_1_top_actor = vtkActor()
bookshelf_1_top_actor.SetMapper(map_bookshelf_1_top)
bookshelf_1_top_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_1_bottom = vtkStructuredGridGeometryFilter()
bookshelf_1_bottom.SetInputConnection(reader.GetOutputPort())
bookshelf_1_bottom.SetExtent(20, 20, 0, 4, 0, 11)
map_bookshelf_1_bottom = vtkPolyDataMapper()
map_bookshelf_1_bottom.SetInputConnection(bookshelf_1_bottom.GetOutputPort())
map_bookshelf_1_bottom.ScalarVisibilityOff()
bookshelf_1_bottom_actor = vtkActor()
bookshelf_1_bottom_actor.SetMapper(map_bookshelf_1_bottom)
bookshelf_1_bottom_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_1_front = vtkStructuredGridGeometryFilter()
bookshelf_1_front.SetInputConnection(reader.GetOutputPort())
bookshelf_1_front.SetExtent(13, 20, 0, 0, 0, 11)
map_bookshelf_1_front = vtkPolyDataMapper()
map_bookshelf_1_front.SetInputConnection(bookshelf_1_front.GetOutputPort())
map_bookshelf_1_front.ScalarVisibilityOff()
bookshelf_1_front_actor = vtkActor()
bookshelf_1_front_actor.SetMapper(map_bookshelf_1_front)
bookshelf_1_front_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_1_back = vtkStructuredGridGeometryFilter()
bookshelf_1_back.SetInputConnection(reader.GetOutputPort())
bookshelf_1_back.SetExtent(13, 20, 4, 4, 0, 11)
map_bookshelf_1_back = vtkPolyDataMapper()
map_bookshelf_1_back.SetInputConnection(bookshelf_1_back.GetOutputPort())
map_bookshelf_1_back.ScalarVisibilityOff()
bookshelf_1_back_actor = vtkActor()
bookshelf_1_back_actor.SetMapper(map_bookshelf_1_back)
bookshelf_1_back_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_1_lhs = vtkStructuredGridGeometryFilter()
bookshelf_1_lhs.SetInputConnection(reader.GetOutputPort())
bookshelf_1_lhs.SetExtent(13, 20, 0, 4, 0, 0)
map_bookshelf_1_lhs = vtkPolyDataMapper()
map_bookshelf_1_lhs.SetInputConnection(bookshelf_1_lhs.GetOutputPort())
map_bookshelf_1_lhs.ScalarVisibilityOff()
bookshelf_1_lhs_actor = vtkActor()
bookshelf_1_lhs_actor.SetMapper(map_bookshelf_1_lhs)
bookshelf_1_lhs_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_1_rhs = vtkStructuredGridGeometryFilter()
bookshelf_1_rhs.SetInputConnection(reader.GetOutputPort())
bookshelf_1_rhs.SetExtent(13, 20, 0, 4, 11, 11)
map_bookshelf_1_rhs = vtkPolyDataMapper()
map_bookshelf_1_rhs.SetInputConnection(bookshelf_1_rhs.GetOutputPort())
map_bookshelf_1_rhs.ScalarVisibilityOff()
bookshelf_1_rhs_actor = vtkActor()
bookshelf_1_rhs_actor.SetMapper(map_bookshelf_1_rhs)
bookshelf_1_rhs_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

# Bookshelf 2
bookshelf_2_top = vtkStructuredGridGeometryFilter()
bookshelf_2_top.SetInputConnection(reader.GetOutputPort())
bookshelf_2_top.SetExtent(13, 13, 15, 19, 0, 11)
map_bookshelf_2_top = vtkPolyDataMapper()
map_bookshelf_2_top.SetInputConnection(bookshelf_2_top.GetOutputPort())
map_bookshelf_2_top.ScalarVisibilityOff()
bookshelf_2_top_actor = vtkActor()
bookshelf_2_top_actor.SetMapper(map_bookshelf_2_top)
bookshelf_2_top_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_2_bottom = vtkStructuredGridGeometryFilter()
bookshelf_2_bottom.SetInputConnection(reader.GetOutputPort())
bookshelf_2_bottom.SetExtent(20, 20, 15, 19, 0, 11)
map_bookshelf_2_bottom = vtkPolyDataMapper()
map_bookshelf_2_bottom.SetInputConnection(bookshelf_2_bottom.GetOutputPort())
map_bookshelf_2_bottom.ScalarVisibilityOff()
bookshelf_2_bottom_actor = vtkActor()
bookshelf_2_bottom_actor.SetMapper(map_bookshelf_2_bottom)
bookshelf_2_bottom_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_2_front = vtkStructuredGridGeometryFilter()
bookshelf_2_front.SetInputConnection(reader.GetOutputPort())
bookshelf_2_front.SetExtent(13, 20, 15, 15, 0, 11)
map_bookshelf_2_front = vtkPolyDataMapper()
map_bookshelf_2_front.SetInputConnection(bookshelf_2_front.GetOutputPort())
map_bookshelf_2_front.ScalarVisibilityOff()
bookshelf_2_front_actor = vtkActor()
bookshelf_2_front_actor.SetMapper(map_bookshelf_2_front)
bookshelf_2_front_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_2_back = vtkStructuredGridGeometryFilter()
bookshelf_2_back.SetInputConnection(reader.GetOutputPort())
bookshelf_2_back.SetExtent(13, 20, 19, 19, 0, 11)
map_bookshelf_2_back = vtkPolyDataMapper()
map_bookshelf_2_back.SetInputConnection(bookshelf_2_back.GetOutputPort())
map_bookshelf_2_back.ScalarVisibilityOff()
bookshelf_2_back_actor = vtkActor()
bookshelf_2_back_actor.SetMapper(map_bookshelf_2_back)
bookshelf_2_back_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_2_lhs = vtkStructuredGridGeometryFilter()
bookshelf_2_lhs.SetInputConnection(reader.GetOutputPort())
bookshelf_2_lhs.SetExtent(13, 20, 15, 19, 0, 0)
map_bookshelf_2_lhs = vtkPolyDataMapper()
map_bookshelf_2_lhs.SetInputConnection(bookshelf_2_lhs.GetOutputPort())
map_bookshelf_2_lhs.ScalarVisibilityOff()
bookshelf_2_lhs_actor = vtkActor()
bookshelf_2_lhs_actor.SetMapper(map_bookshelf_2_lhs)
bookshelf_2_lhs_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

bookshelf_2_rhs = vtkStructuredGridGeometryFilter()
bookshelf_2_rhs.SetInputConnection(reader.GetOutputPort())
bookshelf_2_rhs.SetExtent(13, 20, 15, 19, 11, 11)
map_bookshelf_2_rhs = vtkPolyDataMapper()
map_bookshelf_2_rhs.SetInputConnection(bookshelf_2_rhs.GetOutputPort())
map_bookshelf_2_rhs.ScalarVisibilityOff()
bookshelf_2_rhs_actor = vtkActor()
bookshelf_2_rhs_actor.SetMapper(map_bookshelf_2_rhs)
bookshelf_2_rhs_actor.GetProperty().SetColor(0.8, 0.8, 0.6)

# Window
window_geom = vtkStructuredGridGeometryFilter()
window_geom.SetInputConnection(reader.GetOutputPort())
window_geom.SetExtent(20, 20, 6, 13, 10, 13)
map_window = vtkPolyDataMapper()
map_window.SetInputConnection(window_geom.GetOutputPort())
map_window.ScalarVisibilityOff()
window_actor = vtkActor()
window_actor.SetMapper(map_window)
window_actor.GetProperty().SetColor(0.3, 0.3, 0.5)

# Outlet
outlet = vtkStructuredGridGeometryFilter()
outlet.SetInputConnection(reader.GetOutputPort())
outlet.SetExtent(0, 0, 9, 10, 14, 16)
map_outlet = vtkPolyDataMapper()
map_outlet.SetInputConnection(outlet.GetOutputPort())
map_outlet.ScalarVisibilityOff()
outlet_actor = vtkActor()
outlet_actor.SetMapper(map_outlet)
outlet_actor.GetProperty().SetColor(0, 0, 0)

# Inlet
inlet = vtkStructuredGridGeometryFilter()
inlet.SetInputConnection(reader.GetOutputPort())
inlet.SetExtent(0, 0, 9, 10, 0, 6)
map_inlet = vtkPolyDataMapper()
map_inlet.SetInputConnection(inlet.GetOutputPort())
map_inlet.ScalarVisibilityOff()
inlet_actor = vtkActor()
inlet_actor.SetMapper(map_inlet)
inlet_actor.GetProperty().SetColor(0, 0, 0)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
map_outline = vtkPolyDataMapper()
map_outline.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(map_outline)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Stream tracer with cone glyphs
streamer = vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(0.1, 2.1, 0.5)
streamer.SetMaximumPropagation(500)
streamer.SetInitialIntegrationStep(0.2)
streamer.SetIntegrationDirectionToForward()

cone = vtkConeSource()
cone.SetResolution(8)

cones = vtkGlyph3D()
cones.SetInputConnection(streamer.GetOutputPort())
cones.SetSourceConnection(cone.GetOutputPort())
cones.SetScaleFactor(0.5)
cones.SetInputArrayToProcess(1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "vectors")
cones.SetScaleModeToScaleByVector()

map_cones = vtkPolyDataMapper()
map_cones.SetInputConnection(cones.GetOutputPort())
map_cones.SetScalarRange(reader.GetOutput().GetScalarRange())

cones_actor = vtkActor()
cones_actor.SetMapper(map_cones)

# Add all actors
renderer.AddActor(table_1_actor)
renderer.AddActor(table_2_actor)
renderer.AddActor(filing_cabinet_1_actor)
renderer.AddActor(filing_cabinet_2_actor)
renderer.AddActor(bookshelf_1_top_actor)
renderer.AddActor(bookshelf_1_bottom_actor)
renderer.AddActor(bookshelf_1_front_actor)
renderer.AddActor(bookshelf_1_back_actor)
renderer.AddActor(bookshelf_1_lhs_actor)
renderer.AddActor(bookshelf_1_rhs_actor)
renderer.AddActor(bookshelf_2_top_actor)
renderer.AddActor(bookshelf_2_bottom_actor)
renderer.AddActor(bookshelf_2_front_actor)
renderer.AddActor(bookshelf_2_back_actor)
renderer.AddActor(bookshelf_2_lhs_actor)
renderer.AddActor(bookshelf_2_rhs_actor)
renderer.AddActor(window_actor)
renderer.AddActor(outlet_actor)
renderer.AddActor(inlet_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cones_actor)

renderer.SetBackground(0.4, 0.4, 0.5)

camera = vtkCamera()
camera.SetClippingRange(0.7724, 39)
camera.SetFocalPoint(1.14798, 3.08416, 2.47187)
camera.SetPosition(-2.64683, -3.55525, 3.55848)
camera.SetViewUp(0.0511273, 0.132773, 0.989827)
camera.SetViewAngle(15.5033)
renderer.SetActiveCamera(camera)

render_window.SetSize(500, 300)
render_window.SetWindowName("office stream points")

render_window.Render()
interactor.Start()
