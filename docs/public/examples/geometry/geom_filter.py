#!/usr/bin/env python

# Demonstrate vtkGeometryFilter on structured grid, poly data,
# unstructured grid, and rectilinear grid with extent/point/cell
# clipping options.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import vtkRectilinearGridReader
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read PLOT3D structured grid
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()
output = pl3d.GetOutput().GetBlock(0)

# Structured grid - full surface
gf = vtkGeometryFilter()
gf.SetInputData(output)

g_mapper = vtkPolyDataMapper()
g_mapper.SetInputConnection(gf.GetOutputPort())
g_mapper.SetScalarRange(output.GetScalarRange())

g_actor = vtkActor()
g_actor.SetMapper(g_mapper)

# Structured grid with clipping
gf_2 = vtkGeometryFilter()
gf_2.SetInputData(output)
gf_2.ExtentClippingOn()
gf_2.SetExtent(10, 17, -6, 6, 23, 37)
gf_2.PointClippingOn()
gf_2.SetPointMinimum(0)
gf_2.SetPointMaximum(10000)
gf_2.CellClippingOn()
gf_2.SetCellMinimum(0)
gf_2.SetCellMaximum(7500)

g2_mapper = vtkPolyDataMapper()
g2_mapper.SetInputConnection(gf_2.GetOutputPort())
g2_mapper.SetScalarRange(output.GetScalarRange())

g2_actor = vtkActor()
g2_actor.SetMapper(g2_mapper)
g2_actor.AddPosition(0, 15, 0)

# Poly data surface
gf_3 = vtkGeometryFilter()
gf_3.SetInputConnection(gf.GetOutputPort())

g3_mapper = vtkPolyDataMapper()
g3_mapper.SetInputConnection(gf_3.GetOutputPort())
g3_mapper.SetScalarRange(output.GetScalarRange())

g3_actor = vtkActor()
g3_actor.SetMapper(g3_mapper)
g3_actor.AddPosition(0, 0, 15)

# Poly data with clipping
gf_4 = vtkGeometryFilter()
gf_4.SetInputConnection(gf_2.GetOutputPort())
gf_4.ExtentClippingOn()
gf_4.SetExtent(10, 17, -6, 6, 23, 37)
gf_4.PointClippingOn()
gf_4.SetPointMinimum(0)
gf_4.SetPointMaximum(10000)
gf_4.CellClippingOn()
gf_4.SetCellMinimum(0)
gf_4.SetCellMaximum(7500)

g4_mapper = vtkPolyDataMapper()
g4_mapper.SetInputConnection(gf_4.GetOutputPort())
g4_mapper.SetScalarRange(output.GetScalarRange())

g4_actor = vtkActor()
g4_actor.SetMapper(g4_mapper)
g4_actor.AddPosition(0, 15, 15)

# Unstructured grid surface
s = vtkSphere()
s.SetCenter(output.GetCenter())
s.SetRadius(100.0)

eg = vtkExtractGeometry()
eg.SetInputData(output)
eg.SetImplicitFunction(s)

gf_5 = vtkGeometryFilter()
gf_5.SetInputConnection(eg.GetOutputPort())

g5_mapper = vtkPolyDataMapper()
g5_mapper.SetInputConnection(gf_5.GetOutputPort())
g5_mapper.SetScalarRange(output.GetScalarRange())

g5_actor = vtkActor()
g5_actor.SetMapper(g5_mapper)
g5_actor.AddPosition(0, 0, 30)

# Unstructured grid with clipping
gf_6 = vtkGeometryFilter()
gf_6.SetInputConnection(eg.GetOutputPort())
gf_6.ExtentClippingOn()
gf_6.SetExtent(10, 17, -6, 6, 23, 37)
gf_6.PointClippingOn()
gf_6.SetPointMinimum(0)
gf_6.SetPointMaximum(10000)
gf_6.CellClippingOn()
gf_6.SetCellMinimum(0)
gf_6.SetCellMaximum(7500)

g6_mapper = vtkPolyDataMapper()
g6_mapper.SetInputConnection(gf_6.GetOutputPort())
g6_mapper.SetScalarRange(output.GetScalarRange())

g6_actor = vtkActor()
g6_actor.SetMapper(g6_mapper)
g6_actor.AddPosition(0, 15, 30)

# Rectilinear grid surface
rgrid_reader = vtkRectilinearGridReader()
rgrid_reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
rgrid_reader.Update()

gf_7 = vtkGeometryFilter()
gf_7.SetInputConnection(rgrid_reader.GetOutputPort())

g7_mapper = vtkPolyDataMapper()
g7_mapper.SetInputConnection(gf_7.GetOutputPort())
g7_mapper.SetScalarRange(rgrid_reader.GetOutput().GetScalarRange())

g7_actor = vtkActor()
g7_actor.SetMapper(g7_mapper)
g7_actor.SetScale(3, 3, 3)

# Rectilinear grid with clipping
gf_8 = vtkGeometryFilter()
gf_8.SetInputConnection(rgrid_reader.GetOutputPort())
gf_8.ExtentClippingOn()
gf_8.SetExtent(0, 1, -2, 2, 0, 4)
gf_8.PointClippingOn()
gf_8.SetPointMinimum(0)
gf_8.SetPointMaximum(10000)
gf_8.CellClippingOn()
gf_8.SetCellMinimum(0)
gf_8.SetCellMaximum(7500)

g8_mapper = vtkPolyDataMapper()
g8_mapper.SetInputConnection(gf_8.GetOutputPort())
g8_mapper.SetScalarRange(rgrid_reader.GetOutput().GetScalarRange())

g8_actor = vtkActor()
g8_actor.SetMapper(g8_mapper)
g8_actor.SetScale(3, 3, 3)
g8_actor.AddPosition(0, 15, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(g_actor)
renderer.AddActor(g2_actor)
renderer.AddActor(g3_actor)
renderer.AddActor(g4_actor)
renderer.AddActor(g5_actor)
renderer.AddActor(g6_actor)
renderer.AddActor(g7_actor)
renderer.AddActor(g8_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(340, 550)
render_window.AddRenderer(renderer)
render_window.SetWindowName("geom filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(84, 174)
cam.SetFocalPoint(5.22824, 6.09412, 35.9813)
cam.SetPosition(100.052, 62.875, 102.818)
cam.SetViewUp(-0.307455, -0.464269, 0.830617)

interactor.Initialize()
interactor.Start()
