#!/usr/bin/env python

# Demonstrate vtkProjectedTerrainPath projecting paths onto DEM terrain data
# using the hug projection mode.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersHybrid import vtkProjectedTerrainPath
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Lookup table for elevation coloring
lut = vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)

# Read DEM data
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

# Convert to geometry and warp by elevation
surface = vtkImageDataGeometryFilter()
surface.SetInputConnection(dem_reader.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(surface.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)

normals = vtkPolyDataNormals()
normals.SetInputConnection(warp.GetOutputPort())
normals.SetFeatureAngle(60)
normals.SplittingOff()

dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(lut)

dem_actor = vtkLODActor()
dem_actor.SetMapper(dem_mapper)

# Create terrain paths
pts = vtkPoints()
pts.InsertNextPoint(562669, 5.1198e+006, 1992.77)
pts.InsertNextPoint(562801, 5.11618e+006, 2534.97)
pts.InsertNextPoint(562913, 5.11157e+006, 1911.1)
pts.InsertNextPoint(559849, 5.11083e+006, 1681.34)
pts.InsertNextPoint(562471, 5.11633e+006, 2593.57)
pts.InsertNextPoint(563223, 5.11616e+006, 2598.31)
pts.InsertNextPoint(566579, 5.11127e+006, 1697.83)
pts.InsertNextPoint(569000, 5.11127e+006, 1697.83)

lines = vtkCellArray()
lines.InsertNextCell(3)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertNextCell(5)
lines.InsertCellPoint(3)
lines.InsertCellPoint(4)
lines.InsertCellPoint(5)
lines.InsertCellPoint(6)
lines.InsertCellPoint(7)

terrain_paths = vtkPolyData()
terrain_paths.SetPoints(pts)
terrain_paths.SetLines(lines)

# Project paths onto terrain
projected_paths = vtkProjectedTerrainPath()
projected_paths.SetInputData(terrain_paths)
projected_paths.SetSourceConnection(dem_reader.GetOutputPort())
projected_paths.SetHeightOffset(25)
projected_paths.SetHeightTolerance(5)
projected_paths.SetProjectionModeToNonOccluded()
projected_paths.SetProjectionModeToHug()

path_mapper = vtkPolyDataMapper()
path_mapper.SetInputConnection(projected_paths.GetOutputPort())

paths_actor = vtkActor()
paths_actor.SetMapper(path_mapper)
paths_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.AddActor(paths_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("projected terrain path")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetDesiredUpdateRate(5)

# Scene
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().SetPosition(-99900, -21354, 131801)
renderer.GetActiveCamera().SetFocalPoint(41461, 41461, 2815)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
