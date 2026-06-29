#!/usr/bin/env python

# Demonstrate vtkGreedyTerrainDecimation on DEM terrain data with a
# lookup table for elevation coloring.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersHybrid import vtkGreedyTerrainDecimation
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Lookup table
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

# Decimate the terrain
deci = vtkGreedyTerrainDecimation()
deci.SetInputConnection(dem_reader.GetOutputPort())
deci.BoundaryVertexDeletionOn()
deci.SetErrorMeasureToNumberOfTriangles()
deci.SetNumberOfTriangles(5000)

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(deci.GetOutputPort())
normals.SetFeatureAngle(60)
normals.ConsistencyOn()
normals.SplittingOff()

# Mapper
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(lut)

actor = vtkLODActor()
actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("greedy terrain decimation")

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
