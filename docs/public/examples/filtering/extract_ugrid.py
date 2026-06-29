#!/usr/bin/env python

# Demonstrate vtkExtractUnstructuredGrid extracting a cell range from
# a blow-molding dataset, with connectivity filtering and warp vector
# visualization.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkConnectivityFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractUnstructuredGrid
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

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read blow-molding dataset
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
reader.SetScalarsName("thickness9")
reader.SetVectorsName("displacement9")

cast_to_ugrid = vtkCastToConcrete()
cast_to_ugrid.SetInputConnection(reader.GetOutputPort())
cast_to_ugrid.Update()

# Warp with displacement vectors
warp = vtkWarpVector()
warp.SetInputData(cast_to_ugrid.GetUnstructuredGridOutput())

# Extract mold from mesh using connectivity
connect = vtkConnectivityFilter()
connect.SetInputConnection(warp.GetOutputPort())
connect.SetExtractionModeToSpecifiedRegions()
connect.AddSpecifiedRegion(0)
connect.AddSpecifiedRegion(1)

mold_mapper = vtkDataSetMapper()
mold_mapper.SetInputConnection(reader.GetOutputPort())
mold_mapper.ScalarVisibilityOff()

mold_actor = vtkActor()
mold_actor.SetMapper(mold_mapper)
mold_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
mold_actor.GetProperty().SetRepresentationToWireframe()

# Extract parison from mesh using connectivity
connect_2 = vtkConnectivityFilter()
connect_2.SetInputConnection(warp.GetOutputPort())
connect_2.SetExtractionModeToSpecifiedRegions()
connect_2.AddSpecifiedRegion(2)

extract_grid = vtkExtractUnstructuredGrid()
extract_grid.SetInputConnection(connect_2.GetOutputPort())
extract_grid.CellClippingOn()
extract_grid.SetCellMinimum(0)
extract_grid.SetCellMaximum(23)

parison = vtkGeometryFilter()
parison.SetInputConnection(extract_grid.GetOutputPort())

normals = vtkPolyDataNormals()
normals.SetInputConnection(parison.GetOutputPort())
normals.SetFeatureAngle(60)

lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.0, 0.66667)

parison_mapper = vtkPolyDataMapper()
parison_mapper.SetInputConnection(normals.GetOutputPort())
parison_mapper.SetLookupTable(lookup_table)
parison_mapper.SetScalarRange(0.12, 1.0)

parison_actor = vtkActor()
parison_actor.SetMapper(parison_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(parison_actor)
renderer.AddActor(mold_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(500, 380)
render_window.SetWindowName("extract ugrid")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(60)
renderer.GetActiveCamera().Roll(-90)
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
