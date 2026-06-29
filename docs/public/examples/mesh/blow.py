#!/usr/bin/env python

# Blow-molding simulation showing ten time steps of parison deformation.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkConnectivityFilter,
    vtkContourFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
ivory_black = (0.161, 0.141, 0.129)
alice_blue = (0.941, 0.973, 1.000)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "blow.vtk")

# Lookup table: color the parison by thickness
lut = vtkLookupTable()
lut.SetHueRange(0.0, 0.66667)

# Grid layout: 2 columns x 5 rows = 10 frames
grid_cols = 2
grid_rows = 5
renderer_size_x = 750
renderer_size_y = 400
scale = 0.5

# --- Frame 0 ---
reader_0 = vtkDataSetReader()
reader_0.SetFileName(file_name)
reader_0.SetScalarsName("thickness0")
reader_0.SetVectorsName("displacement0")
reader_0.Update()

warp_0 = vtkWarpVector()
warp_0.SetInputData(reader_0.GetUnstructuredGridOutput())

mold_connect_0 = vtkConnectivityFilter()
mold_connect_0.SetInputConnection(warp_0.GetOutputPort())
mold_connect_0.SetExtractionModeToSpecifiedRegions()
mold_connect_0.AddSpecifiedRegion(0)
mold_connect_0.AddSpecifiedRegion(1)

mold_geom_0 = vtkGeometryFilter()
mold_geom_0.SetInputConnection(mold_connect_0.GetOutputPort())

mold_mapper_0 = vtkDataSetMapper()
mold_mapper_0.SetInputConnection(mold_geom_0.GetOutputPort())
mold_mapper_0.ScalarVisibilityOff()

mold_actor_0 = vtkActor()
mold_actor_0.SetMapper(mold_mapper_0)
mold_actor_0.GetProperty().SetColor(ivory_black)
mold_actor_0.GetProperty().SetRepresentationToWireframe()

parison_connect_0 = vtkConnectivityFilter()
parison_connect_0.SetInputConnection(warp_0.GetOutputPort())
parison_connect_0.SetExtractionModeToSpecifiedRegions()
parison_connect_0.AddSpecifiedRegion(2)

parison_geom_0 = vtkGeometryFilter()
parison_geom_0.SetInputConnection(parison_connect_0.GetOutputPort())

parison_normals_0 = vtkPolyDataNormals()
parison_normals_0.SetInputConnection(parison_geom_0.GetOutputPort())
parison_normals_0.SetFeatureAngle(60)

parison_mapper_0 = vtkPolyDataMapper()
parison_mapper_0.SetInputConnection(parison_normals_0.GetOutputPort())
parison_mapper_0.SetLookupTable(lut)
parison_mapper_0.SetScalarRange(0.12, 1.0)

parison_actor_0 = vtkActor()
parison_actor_0.SetMapper(parison_mapper_0)

contour_0 = vtkContourFilter()
contour_0.SetInputConnection(parison_connect_0.GetOutputPort())
contour_0.SetValue(0, 0.5)

contour_mapper_0 = vtkPolyDataMapper()
contour_mapper_0.SetInputConnection(contour_0.GetOutputPort())

contour_actor_0 = vtkActor()
contour_actor_0.SetMapper(contour_mapper_0)

ren_0 = vtkRenderer()
ren_0.AddActor(mold_actor_0)
ren_0.AddActor(parison_actor_0)
ren_0.AddActor(contour_actor_0)
ren_0.SetBackground(alice_blue)
ren_0.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_0.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_0.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_0.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_0.SetViewport(0.0, 0.8, 0.5, 1.0)

# --- Frame 1 ---
reader_1 = vtkDataSetReader()
reader_1.SetFileName(file_name)
reader_1.SetScalarsName("thickness1")
reader_1.SetVectorsName("displacement1")
reader_1.Update()

warp_1 = vtkWarpVector()
warp_1.SetInputData(reader_1.GetUnstructuredGridOutput())

mold_connect_1 = vtkConnectivityFilter()
mold_connect_1.SetInputConnection(warp_1.GetOutputPort())
mold_connect_1.SetExtractionModeToSpecifiedRegions()
mold_connect_1.AddSpecifiedRegion(0)
mold_connect_1.AddSpecifiedRegion(1)

mold_geom_1 = vtkGeometryFilter()
mold_geom_1.SetInputConnection(mold_connect_1.GetOutputPort())

mold_mapper_1 = vtkDataSetMapper()
mold_mapper_1.SetInputConnection(mold_geom_1.GetOutputPort())
mold_mapper_1.ScalarVisibilityOff()

mold_actor_1 = vtkActor()
mold_actor_1.SetMapper(mold_mapper_1)
mold_actor_1.GetProperty().SetColor(ivory_black)
mold_actor_1.GetProperty().SetRepresentationToWireframe()

parison_connect_1 = vtkConnectivityFilter()
parison_connect_1.SetInputConnection(warp_1.GetOutputPort())
parison_connect_1.SetExtractionModeToSpecifiedRegions()
parison_connect_1.AddSpecifiedRegion(2)

parison_geom_1 = vtkGeometryFilter()
parison_geom_1.SetInputConnection(parison_connect_1.GetOutputPort())

parison_normals_1 = vtkPolyDataNormals()
parison_normals_1.SetInputConnection(parison_geom_1.GetOutputPort())
parison_normals_1.SetFeatureAngle(60)

parison_mapper_1 = vtkPolyDataMapper()
parison_mapper_1.SetInputConnection(parison_normals_1.GetOutputPort())
parison_mapper_1.SetLookupTable(lut)
parison_mapper_1.SetScalarRange(0.12, 1.0)

parison_actor_1 = vtkActor()
parison_actor_1.SetMapper(parison_mapper_1)

contour_1 = vtkContourFilter()
contour_1.SetInputConnection(parison_connect_1.GetOutputPort())
contour_1.SetValue(0, 0.5)

contour_mapper_1 = vtkPolyDataMapper()
contour_mapper_1.SetInputConnection(contour_1.GetOutputPort())

contour_actor_1 = vtkActor()
contour_actor_1.SetMapper(contour_mapper_1)

ren_1 = vtkRenderer()
ren_1.AddActor(mold_actor_1)
ren_1.AddActor(parison_actor_1)
ren_1.AddActor(contour_actor_1)
ren_1.SetBackground(alice_blue)
ren_1.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_1.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_1.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_1.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_1.SetViewport(0.5, 0.8, 1.0, 1.0)

# --- Frame 2 ---
reader_2 = vtkDataSetReader()
reader_2.SetFileName(file_name)
reader_2.SetScalarsName("thickness2")
reader_2.SetVectorsName("displacement2")
reader_2.Update()

warp_2 = vtkWarpVector()
warp_2.SetInputData(reader_2.GetUnstructuredGridOutput())

mold_connect_2 = vtkConnectivityFilter()
mold_connect_2.SetInputConnection(warp_2.GetOutputPort())
mold_connect_2.SetExtractionModeToSpecifiedRegions()
mold_connect_2.AddSpecifiedRegion(0)
mold_connect_2.AddSpecifiedRegion(1)

mold_geom_2 = vtkGeometryFilter()
mold_geom_2.SetInputConnection(mold_connect_2.GetOutputPort())

mold_mapper_2 = vtkDataSetMapper()
mold_mapper_2.SetInputConnection(mold_geom_2.GetOutputPort())
mold_mapper_2.ScalarVisibilityOff()

mold_actor_2 = vtkActor()
mold_actor_2.SetMapper(mold_mapper_2)
mold_actor_2.GetProperty().SetColor(ivory_black)
mold_actor_2.GetProperty().SetRepresentationToWireframe()

parison_connect_2 = vtkConnectivityFilter()
parison_connect_2.SetInputConnection(warp_2.GetOutputPort())
parison_connect_2.SetExtractionModeToSpecifiedRegions()
parison_connect_2.AddSpecifiedRegion(2)

parison_geom_2 = vtkGeometryFilter()
parison_geom_2.SetInputConnection(parison_connect_2.GetOutputPort())

parison_normals_2 = vtkPolyDataNormals()
parison_normals_2.SetInputConnection(parison_geom_2.GetOutputPort())
parison_normals_2.SetFeatureAngle(60)

parison_mapper_2 = vtkPolyDataMapper()
parison_mapper_2.SetInputConnection(parison_normals_2.GetOutputPort())
parison_mapper_2.SetLookupTable(lut)
parison_mapper_2.SetScalarRange(0.12, 1.0)

parison_actor_2 = vtkActor()
parison_actor_2.SetMapper(parison_mapper_2)

contour_2 = vtkContourFilter()
contour_2.SetInputConnection(parison_connect_2.GetOutputPort())
contour_2.SetValue(0, 0.5)

contour_mapper_2 = vtkPolyDataMapper()
contour_mapper_2.SetInputConnection(contour_2.GetOutputPort())

contour_actor_2 = vtkActor()
contour_actor_2.SetMapper(contour_mapper_2)

ren_2 = vtkRenderer()
ren_2.AddActor(mold_actor_2)
ren_2.AddActor(parison_actor_2)
ren_2.AddActor(contour_actor_2)
ren_2.SetBackground(alice_blue)
ren_2.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_2.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_2.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_2.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_2.SetViewport(0.0, 0.6, 0.5, 0.8)

# --- Frame 3 ---
reader_3 = vtkDataSetReader()
reader_3.SetFileName(file_name)
reader_3.SetScalarsName("thickness3")
reader_3.SetVectorsName("displacement3")
reader_3.Update()

warp_3 = vtkWarpVector()
warp_3.SetInputData(reader_3.GetUnstructuredGridOutput())

mold_connect_3 = vtkConnectivityFilter()
mold_connect_3.SetInputConnection(warp_3.GetOutputPort())
mold_connect_3.SetExtractionModeToSpecifiedRegions()
mold_connect_3.AddSpecifiedRegion(0)
mold_connect_3.AddSpecifiedRegion(1)

mold_geom_3 = vtkGeometryFilter()
mold_geom_3.SetInputConnection(mold_connect_3.GetOutputPort())

mold_mapper_3 = vtkDataSetMapper()
mold_mapper_3.SetInputConnection(mold_geom_3.GetOutputPort())
mold_mapper_3.ScalarVisibilityOff()

mold_actor_3 = vtkActor()
mold_actor_3.SetMapper(mold_mapper_3)
mold_actor_3.GetProperty().SetColor(ivory_black)
mold_actor_3.GetProperty().SetRepresentationToWireframe()

parison_connect_3 = vtkConnectivityFilter()
parison_connect_3.SetInputConnection(warp_3.GetOutputPort())
parison_connect_3.SetExtractionModeToSpecifiedRegions()
parison_connect_3.AddSpecifiedRegion(2)

parison_geom_3 = vtkGeometryFilter()
parison_geom_3.SetInputConnection(parison_connect_3.GetOutputPort())

parison_normals_3 = vtkPolyDataNormals()
parison_normals_3.SetInputConnection(parison_geom_3.GetOutputPort())
parison_normals_3.SetFeatureAngle(60)

parison_mapper_3 = vtkPolyDataMapper()
parison_mapper_3.SetInputConnection(parison_normals_3.GetOutputPort())
parison_mapper_3.SetLookupTable(lut)
parison_mapper_3.SetScalarRange(0.12, 1.0)

parison_actor_3 = vtkActor()
parison_actor_3.SetMapper(parison_mapper_3)

contour_3 = vtkContourFilter()
contour_3.SetInputConnection(parison_connect_3.GetOutputPort())
contour_3.SetValue(0, 0.5)

contour_mapper_3 = vtkPolyDataMapper()
contour_mapper_3.SetInputConnection(contour_3.GetOutputPort())

contour_actor_3 = vtkActor()
contour_actor_3.SetMapper(contour_mapper_3)

ren_3 = vtkRenderer()
ren_3.AddActor(mold_actor_3)
ren_3.AddActor(parison_actor_3)
ren_3.AddActor(contour_actor_3)
ren_3.SetBackground(alice_blue)
ren_3.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_3.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_3.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_3.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_3.SetViewport(0.5, 0.6, 1.0, 0.8)

# --- Frame 4 ---
reader_4 = vtkDataSetReader()
reader_4.SetFileName(file_name)
reader_4.SetScalarsName("thickness4")
reader_4.SetVectorsName("displacement4")
reader_4.Update()

warp_4 = vtkWarpVector()
warp_4.SetInputData(reader_4.GetUnstructuredGridOutput())

mold_connect_4 = vtkConnectivityFilter()
mold_connect_4.SetInputConnection(warp_4.GetOutputPort())
mold_connect_4.SetExtractionModeToSpecifiedRegions()
mold_connect_4.AddSpecifiedRegion(0)
mold_connect_4.AddSpecifiedRegion(1)

mold_geom_4 = vtkGeometryFilter()
mold_geom_4.SetInputConnection(mold_connect_4.GetOutputPort())

mold_mapper_4 = vtkDataSetMapper()
mold_mapper_4.SetInputConnection(mold_geom_4.GetOutputPort())
mold_mapper_4.ScalarVisibilityOff()

mold_actor_4 = vtkActor()
mold_actor_4.SetMapper(mold_mapper_4)
mold_actor_4.GetProperty().SetColor(ivory_black)
mold_actor_4.GetProperty().SetRepresentationToWireframe()

parison_connect_4 = vtkConnectivityFilter()
parison_connect_4.SetInputConnection(warp_4.GetOutputPort())
parison_connect_4.SetExtractionModeToSpecifiedRegions()
parison_connect_4.AddSpecifiedRegion(2)

parison_geom_4 = vtkGeometryFilter()
parison_geom_4.SetInputConnection(parison_connect_4.GetOutputPort())

parison_normals_4 = vtkPolyDataNormals()
parison_normals_4.SetInputConnection(parison_geom_4.GetOutputPort())
parison_normals_4.SetFeatureAngle(60)

parison_mapper_4 = vtkPolyDataMapper()
parison_mapper_4.SetInputConnection(parison_normals_4.GetOutputPort())
parison_mapper_4.SetLookupTable(lut)
parison_mapper_4.SetScalarRange(0.12, 1.0)

parison_actor_4 = vtkActor()
parison_actor_4.SetMapper(parison_mapper_4)

contour_4 = vtkContourFilter()
contour_4.SetInputConnection(parison_connect_4.GetOutputPort())
contour_4.SetValue(0, 0.5)

contour_mapper_4 = vtkPolyDataMapper()
contour_mapper_4.SetInputConnection(contour_4.GetOutputPort())

contour_actor_4 = vtkActor()
contour_actor_4.SetMapper(contour_mapper_4)

ren_4 = vtkRenderer()
ren_4.AddActor(mold_actor_4)
ren_4.AddActor(parison_actor_4)
ren_4.AddActor(contour_actor_4)
ren_4.SetBackground(alice_blue)
ren_4.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_4.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_4.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_4.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_4.SetViewport(0.0, 0.4, 0.5, 0.6)

# --- Frame 5 ---
reader_5 = vtkDataSetReader()
reader_5.SetFileName(file_name)
reader_5.SetScalarsName("thickness5")
reader_5.SetVectorsName("displacement5")
reader_5.Update()

warp_5 = vtkWarpVector()
warp_5.SetInputData(reader_5.GetUnstructuredGridOutput())

mold_connect_5 = vtkConnectivityFilter()
mold_connect_5.SetInputConnection(warp_5.GetOutputPort())
mold_connect_5.SetExtractionModeToSpecifiedRegions()
mold_connect_5.AddSpecifiedRegion(0)
mold_connect_5.AddSpecifiedRegion(1)

mold_geom_5 = vtkGeometryFilter()
mold_geom_5.SetInputConnection(mold_connect_5.GetOutputPort())

mold_mapper_5 = vtkDataSetMapper()
mold_mapper_5.SetInputConnection(mold_geom_5.GetOutputPort())
mold_mapper_5.ScalarVisibilityOff()

mold_actor_5 = vtkActor()
mold_actor_5.SetMapper(mold_mapper_5)
mold_actor_5.GetProperty().SetColor(ivory_black)
mold_actor_5.GetProperty().SetRepresentationToWireframe()

parison_connect_5 = vtkConnectivityFilter()
parison_connect_5.SetInputConnection(warp_5.GetOutputPort())
parison_connect_5.SetExtractionModeToSpecifiedRegions()
parison_connect_5.AddSpecifiedRegion(2)

parison_geom_5 = vtkGeometryFilter()
parison_geom_5.SetInputConnection(parison_connect_5.GetOutputPort())

parison_normals_5 = vtkPolyDataNormals()
parison_normals_5.SetInputConnection(parison_geom_5.GetOutputPort())
parison_normals_5.SetFeatureAngle(60)

parison_mapper_5 = vtkPolyDataMapper()
parison_mapper_5.SetInputConnection(parison_normals_5.GetOutputPort())
parison_mapper_5.SetLookupTable(lut)
parison_mapper_5.SetScalarRange(0.12, 1.0)

parison_actor_5 = vtkActor()
parison_actor_5.SetMapper(parison_mapper_5)

contour_5 = vtkContourFilter()
contour_5.SetInputConnection(parison_connect_5.GetOutputPort())
contour_5.SetValue(0, 0.5)

contour_mapper_5 = vtkPolyDataMapper()
contour_mapper_5.SetInputConnection(contour_5.GetOutputPort())

contour_actor_5 = vtkActor()
contour_actor_5.SetMapper(contour_mapper_5)

ren_5 = vtkRenderer()
ren_5.AddActor(mold_actor_5)
ren_5.AddActor(parison_actor_5)
ren_5.AddActor(contour_actor_5)
ren_5.SetBackground(alice_blue)
ren_5.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_5.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_5.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_5.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_5.SetViewport(0.5, 0.4, 1.0, 0.6)

# --- Frame 6 ---
reader_6 = vtkDataSetReader()
reader_6.SetFileName(file_name)
reader_6.SetScalarsName("thickness6")
reader_6.SetVectorsName("displacement6")
reader_6.Update()

warp_6 = vtkWarpVector()
warp_6.SetInputData(reader_6.GetUnstructuredGridOutput())

mold_connect_6 = vtkConnectivityFilter()
mold_connect_6.SetInputConnection(warp_6.GetOutputPort())
mold_connect_6.SetExtractionModeToSpecifiedRegions()
mold_connect_6.AddSpecifiedRegion(0)
mold_connect_6.AddSpecifiedRegion(1)

mold_geom_6 = vtkGeometryFilter()
mold_geom_6.SetInputConnection(mold_connect_6.GetOutputPort())

mold_mapper_6 = vtkDataSetMapper()
mold_mapper_6.SetInputConnection(mold_geom_6.GetOutputPort())
mold_mapper_6.ScalarVisibilityOff()

mold_actor_6 = vtkActor()
mold_actor_6.SetMapper(mold_mapper_6)
mold_actor_6.GetProperty().SetColor(ivory_black)
mold_actor_6.GetProperty().SetRepresentationToWireframe()

parison_connect_6 = vtkConnectivityFilter()
parison_connect_6.SetInputConnection(warp_6.GetOutputPort())
parison_connect_6.SetExtractionModeToSpecifiedRegions()
parison_connect_6.AddSpecifiedRegion(2)

parison_geom_6 = vtkGeometryFilter()
parison_geom_6.SetInputConnection(parison_connect_6.GetOutputPort())

parison_normals_6 = vtkPolyDataNormals()
parison_normals_6.SetInputConnection(parison_geom_6.GetOutputPort())
parison_normals_6.SetFeatureAngle(60)

parison_mapper_6 = vtkPolyDataMapper()
parison_mapper_6.SetInputConnection(parison_normals_6.GetOutputPort())
parison_mapper_6.SetLookupTable(lut)
parison_mapper_6.SetScalarRange(0.12, 1.0)

parison_actor_6 = vtkActor()
parison_actor_6.SetMapper(parison_mapper_6)

contour_6 = vtkContourFilter()
contour_6.SetInputConnection(parison_connect_6.GetOutputPort())
contour_6.SetValue(0, 0.5)

contour_mapper_6 = vtkPolyDataMapper()
contour_mapper_6.SetInputConnection(contour_6.GetOutputPort())

contour_actor_6 = vtkActor()
contour_actor_6.SetMapper(contour_mapper_6)

ren_6 = vtkRenderer()
ren_6.AddActor(mold_actor_6)
ren_6.AddActor(parison_actor_6)
ren_6.AddActor(contour_actor_6)
ren_6.SetBackground(alice_blue)
ren_6.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_6.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_6.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_6.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_6.SetViewport(0.0, 0.2, 0.5, 0.4)

# --- Frame 7 ---
reader_7 = vtkDataSetReader()
reader_7.SetFileName(file_name)
reader_7.SetScalarsName("thickness7")
reader_7.SetVectorsName("displacement7")
reader_7.Update()

warp_7 = vtkWarpVector()
warp_7.SetInputData(reader_7.GetUnstructuredGridOutput())

mold_connect_7 = vtkConnectivityFilter()
mold_connect_7.SetInputConnection(warp_7.GetOutputPort())
mold_connect_7.SetExtractionModeToSpecifiedRegions()
mold_connect_7.AddSpecifiedRegion(0)
mold_connect_7.AddSpecifiedRegion(1)

mold_geom_7 = vtkGeometryFilter()
mold_geom_7.SetInputConnection(mold_connect_7.GetOutputPort())

mold_mapper_7 = vtkDataSetMapper()
mold_mapper_7.SetInputConnection(mold_geom_7.GetOutputPort())
mold_mapper_7.ScalarVisibilityOff()

mold_actor_7 = vtkActor()
mold_actor_7.SetMapper(mold_mapper_7)
mold_actor_7.GetProperty().SetColor(ivory_black)
mold_actor_7.GetProperty().SetRepresentationToWireframe()

parison_connect_7 = vtkConnectivityFilter()
parison_connect_7.SetInputConnection(warp_7.GetOutputPort())
parison_connect_7.SetExtractionModeToSpecifiedRegions()
parison_connect_7.AddSpecifiedRegion(2)

parison_geom_7 = vtkGeometryFilter()
parison_geom_7.SetInputConnection(parison_connect_7.GetOutputPort())

parison_normals_7 = vtkPolyDataNormals()
parison_normals_7.SetInputConnection(parison_geom_7.GetOutputPort())
parison_normals_7.SetFeatureAngle(60)

parison_mapper_7 = vtkPolyDataMapper()
parison_mapper_7.SetInputConnection(parison_normals_7.GetOutputPort())
parison_mapper_7.SetLookupTable(lut)
parison_mapper_7.SetScalarRange(0.12, 1.0)

parison_actor_7 = vtkActor()
parison_actor_7.SetMapper(parison_mapper_7)

contour_7 = vtkContourFilter()
contour_7.SetInputConnection(parison_connect_7.GetOutputPort())
contour_7.SetValue(0, 0.5)

contour_mapper_7 = vtkPolyDataMapper()
contour_mapper_7.SetInputConnection(contour_7.GetOutputPort())

contour_actor_7 = vtkActor()
contour_actor_7.SetMapper(contour_mapper_7)

ren_7 = vtkRenderer()
ren_7.AddActor(mold_actor_7)
ren_7.AddActor(parison_actor_7)
ren_7.AddActor(contour_actor_7)
ren_7.SetBackground(alice_blue)
ren_7.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_7.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_7.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_7.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_7.SetViewport(0.5, 0.2, 1.0, 0.4)

# --- Frame 8 ---
reader_8 = vtkDataSetReader()
reader_8.SetFileName(file_name)
reader_8.SetScalarsName("thickness8")
reader_8.SetVectorsName("displacement8")
reader_8.Update()

warp_8 = vtkWarpVector()
warp_8.SetInputData(reader_8.GetUnstructuredGridOutput())

mold_connect_8 = vtkConnectivityFilter()
mold_connect_8.SetInputConnection(warp_8.GetOutputPort())
mold_connect_8.SetExtractionModeToSpecifiedRegions()
mold_connect_8.AddSpecifiedRegion(0)
mold_connect_8.AddSpecifiedRegion(1)

mold_geom_8 = vtkGeometryFilter()
mold_geom_8.SetInputConnection(mold_connect_8.GetOutputPort())

mold_mapper_8 = vtkDataSetMapper()
mold_mapper_8.SetInputConnection(mold_geom_8.GetOutputPort())
mold_mapper_8.ScalarVisibilityOff()

mold_actor_8 = vtkActor()
mold_actor_8.SetMapper(mold_mapper_8)
mold_actor_8.GetProperty().SetColor(ivory_black)
mold_actor_8.GetProperty().SetRepresentationToWireframe()

parison_connect_8 = vtkConnectivityFilter()
parison_connect_8.SetInputConnection(warp_8.GetOutputPort())
parison_connect_8.SetExtractionModeToSpecifiedRegions()
parison_connect_8.AddSpecifiedRegion(2)

parison_geom_8 = vtkGeometryFilter()
parison_geom_8.SetInputConnection(parison_connect_8.GetOutputPort())

parison_normals_8 = vtkPolyDataNormals()
parison_normals_8.SetInputConnection(parison_geom_8.GetOutputPort())
parison_normals_8.SetFeatureAngle(60)

parison_mapper_8 = vtkPolyDataMapper()
parison_mapper_8.SetInputConnection(parison_normals_8.GetOutputPort())
parison_mapper_8.SetLookupTable(lut)
parison_mapper_8.SetScalarRange(0.12, 1.0)

parison_actor_8 = vtkActor()
parison_actor_8.SetMapper(parison_mapper_8)

contour_8 = vtkContourFilter()
contour_8.SetInputConnection(parison_connect_8.GetOutputPort())
contour_8.SetValue(0, 0.5)

contour_mapper_8 = vtkPolyDataMapper()
contour_mapper_8.SetInputConnection(contour_8.GetOutputPort())

contour_actor_8 = vtkActor()
contour_actor_8.SetMapper(contour_mapper_8)

ren_8 = vtkRenderer()
ren_8.AddActor(mold_actor_8)
ren_8.AddActor(parison_actor_8)
ren_8.AddActor(contour_actor_8)
ren_8.SetBackground(alice_blue)
ren_8.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_8.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_8.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_8.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_8.SetViewport(0.0, 0.0, 0.5, 0.2)

# --- Frame 9 ---
reader_9 = vtkDataSetReader()
reader_9.SetFileName(file_name)
reader_9.SetScalarsName("thickness9")
reader_9.SetVectorsName("displacement9")
reader_9.Update()

warp_9 = vtkWarpVector()
warp_9.SetInputData(reader_9.GetUnstructuredGridOutput())

mold_connect_9 = vtkConnectivityFilter()
mold_connect_9.SetInputConnection(warp_9.GetOutputPort())
mold_connect_9.SetExtractionModeToSpecifiedRegions()
mold_connect_9.AddSpecifiedRegion(0)
mold_connect_9.AddSpecifiedRegion(1)

mold_geom_9 = vtkGeometryFilter()
mold_geom_9.SetInputConnection(mold_connect_9.GetOutputPort())

mold_mapper_9 = vtkDataSetMapper()
mold_mapper_9.SetInputConnection(mold_geom_9.GetOutputPort())
mold_mapper_9.ScalarVisibilityOff()

mold_actor_9 = vtkActor()
mold_actor_9.SetMapper(mold_mapper_9)
mold_actor_9.GetProperty().SetColor(ivory_black)
mold_actor_9.GetProperty().SetRepresentationToWireframe()

parison_connect_9 = vtkConnectivityFilter()
parison_connect_9.SetInputConnection(warp_9.GetOutputPort())
parison_connect_9.SetExtractionModeToSpecifiedRegions()
parison_connect_9.AddSpecifiedRegion(2)

parison_geom_9 = vtkGeometryFilter()
parison_geom_9.SetInputConnection(parison_connect_9.GetOutputPort())

parison_normals_9 = vtkPolyDataNormals()
parison_normals_9.SetInputConnection(parison_geom_9.GetOutputPort())
parison_normals_9.SetFeatureAngle(60)

parison_mapper_9 = vtkPolyDataMapper()
parison_mapper_9.SetInputConnection(parison_normals_9.GetOutputPort())
parison_mapper_9.SetLookupTable(lut)
parison_mapper_9.SetScalarRange(0.12, 1.0)

parison_actor_9 = vtkActor()
parison_actor_9.SetMapper(parison_mapper_9)

contour_9 = vtkContourFilter()
contour_9.SetInputConnection(parison_connect_9.GetOutputPort())
contour_9.SetValue(0, 0.5)

contour_mapper_9 = vtkPolyDataMapper()
contour_mapper_9.SetInputConnection(contour_9.GetOutputPort())

contour_actor_9 = vtkActor()
contour_actor_9.SetMapper(contour_mapper_9)

ren_9 = vtkRenderer()
ren_9.AddActor(mold_actor_9)
ren_9.AddActor(parison_actor_9)
ren_9.AddActor(contour_actor_9)
ren_9.SetBackground(alice_blue)
ren_9.GetActiveCamera().SetPosition(50.973277, 12.298821, 29.102547)
ren_9.GetActiveCamera().SetFocalPoint(0.141547, 12.298821, -0.245166)
ren_9.GetActiveCamera().SetViewUp(-0.500000, 0.000000, 0.866025)
ren_9.GetActiveCamera().SetClippingRange(36.640827, 78.614680)
ren_9.SetViewport(0.5, 0.0, 1.0, 0.2)

# Window: display all ten frames in a 2x5 grid
render_window = vtkRenderWindow()
render_window.AddRenderer(ren_0)
render_window.AddRenderer(ren_1)
render_window.AddRenderer(ren_2)
render_window.AddRenderer(ren_3)
render_window.AddRenderer(ren_4)
render_window.AddRenderer(ren_5)
render_window.AddRenderer(ren_6)
render_window.AddRenderer(ren_7)
render_window.AddRenderer(ren_8)
render_window.AddRenderer(ren_9)
render_window.SetWindowName("blow")
render_window.SetMultiSamples(0)
render_window.SetSize(
    int(renderer_size_x * grid_cols * scale),
    int(renderer_size_y * grid_rows * scale),
)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
